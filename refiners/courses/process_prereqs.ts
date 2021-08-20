import * as _ from "lodash";
import { parse } from "path/posix";
import { start } from "repl";
import split_raw_prereq_str from "./split_raw_prereq_str";
import * as courses from '../../data/json/raw/courses.json';
import { parse_wam_req, parse_uoc_req, parse_lvl_req, parse_sub_req, parse_prog_req, parse_spec_req, clean_course_group_str, find_all_valid_courses_from_cg, construct_unlocked_by_arr, replace_with_bool_symbols} from './prereq_section_helpers'
import { replace } from "lodash";

export type Prereq = {
  equivalent_courses: string[];
  exclusion_courses: string[]; 
  unlocked_by: string[];
  unlocks: string[];
  other_requirements: {
    uoc?: number;
    wam?: number;
    subject?: string;
    level?: number;
    specialisations?: string[];
    programs?: string[];
    corequisites?: string[];
    all_found_courses?: string[];
    course_group_boolean?: string;
    raw_str?: string;
  };
}

const process_prereq = (prereq_str: string, curr_course: string, exclusion_courses: string[], equivalent_courses: string[]): Prereq => {
  let prereq_obj: Prereq = initialise_prereq_obj(prereq_str, exclusion_courses, equivalent_courses);
  //console.log(curr_course);
  if (prereq_str === 'None' || prereq_str === '') return prereq_obj;

  const [prereq_section, coreq_section, excl_section, equiv_section, misc_section]: string[] = split_raw_prereq_str(prereq_str);

  prereq_obj = process_preq_section(prereq_section, curr_course, prereq_obj);
  prereq_obj = process_creq_section(coreq_section, prereq_obj);
  prereq_obj.exclusion_courses = process_excl_section(excl_section, exclusion_courses);
  prereq_obj.equivalent_courses = process_equiv_section(equiv_section, equivalent_courses);

  //console.log(JSON.stringify(prereq_obj, null, 2));
  return prereq_obj;
}

const process_preq_section = (preq_section: string, curr_course: string, prereq_obj: Prereq): Prereq => {
  const preq_str = clean_string(preq_section);
  // maybe get all found codes into an all list, use this to fill unlocks
  let course_group_pattern: RegExp = /([a-z]{4}\/)*[\[(]*[a-z]{4}?[0-9]{4}.*[ /(,][a-z]{4}[0-9]{4}[\])]*(\/\d{4})*/gmi;
  let course_group_match = preq_str.match(course_group_pattern);
  // either has multiple courses in prereq, just one or none at all
  if (course_group_match) {
    let course_group: string = course_group_match[0];
    // heavily processed course_group, removed inconsistensies, tokenised and interpreted (implied) course relationships 
    course_group = clean_course_group_str(course_group);
    // NOTE: use all_valid_courses to build 'unlocks' attribute
    const all_valid_courses: string[] = find_all_valid_courses_from_cg(course_group);
    prereq_obj.other_requirements.all_found_courses = all_valid_courses;
    // time for the fucked up bit
    // create course group boolean expression, swap 'AND' and 'OR' with respective symbols
    let cg_bool_str: string = replace_with_bool_symbols(course_group);
    prereq_obj.other_requirements.course_group_boolean = cg_bool_str;

    const unlocked_by_prereqs: string[] = construct_unlocked_by_arr(course_group); 
    prereq_obj.unlocked_by = unlocked_by_prereqs;

  } else {
    // check non course group prereq strs for existence of one course
      // if found assign to unlocked_by attr
      // also check if course is currently offered before inserting into all_found_courses
    const one_course_filter: RegExp = /(^[a-z]{4}[0-9]{4})| [\(]?([a-z]{4}[0-9]{4})[-,\)]?| ([a-z]{4}[0-9]{4})$/gmi;
    const one_course_match = preq_str.match(one_course_filter)
    if (one_course_match){
      const one_prereq: string = _.trim(one_course_match[0], ' -,()').toUpperCase();
      if (one_prereq in courses) {
        prereq_obj.unlocked_by = [one_prereq];
        prereq_obj.other_requirements.all_found_courses = [one_prereq];
      }
    }
  }

  // note to self: everything below is pretty much a done deal
  // do not return for your sanity
  let wam_str = parse_wam_req(preq_str);
  if (wam_str !== "") {
    const wam_req: number = parseInt(wam_str);
    prereq_obj.other_requirements.wam = wam_req;
  }
  let uoc_str = parse_uoc_req(preq_str);
  if (uoc_str !== "") {
    const uoc_req: number = parseInt(uoc_str);
    if (uoc_req > 12 || (uoc_req === 12 && preq_str.match(/^12UOC/g))) {
      prereq_obj.other_requirements.uoc = uoc_req;
      const lvl_req: number = parse_lvl_req(preq_str);
      if (lvl_req > 0) {
        prereq_obj.other_requirements.level = lvl_req;
      }
    }
    const sub_req: string = parse_sub_req(preq_str);
    if (sub_req !== "") {
      prereq_obj.other_requirements.subject = sub_req;
    }
  }
  let prog_arr = parse_prog_req(preq_str);
  if (prog_arr.length > 0) {
    prereq_obj.other_requirements.programs = prog_arr;
  }
  prereq_obj = parse_spec_req(preq_str, prereq_obj);
  return prereq_obj;
}

const process_creq_section = (creq_section: string, prereq_obj: Prereq): Prereq => {
  if (creq_section === "") return prereq_obj;

  //console.log(prereq_obj.other_requirements.raw_str);
  //console.log(prereq_obj.other_requirements.all_found_courses);

  const creq_str = clean_string(creq_section);
  let course_group_pattern: RegExp = /([a-z]{4}\/)*[\[(]*[a-z]{4}?[0-9]{4}.*[ /(,][a-z]{4}[0-9]{4}[\])]*(\/\d{4})*/gmi;
  let course_group_match = creq_str.match(course_group_pattern);
  // check if there is a 'course group' (>=2 courses)
  if (course_group_match) {
    let course_group: string = course_group_match[0];
    course_group = clean_course_group_str(course_group);
    // todo: first check the coreq array with existing all_found_courses attribute, see if there are clashing attributes
      // if there are, pop from coreq array
    const unlocked_by_coreqs: string[] = construct_unlocked_by_arr(course_group); 
    const ub_coreqs_w_c: string[] = unlocked_by_coreqs.map(str => str + ' (c)');
    prereq_obj.other_requirements.corequisites = unlocked_by_coreqs;
    prereq_obj.unlocked_by = prereq_obj.unlocked_by.concat(ub_coreqs_w_c);

    const all_valid_courses: string[] = find_all_valid_courses_from_cg(course_group);
    if ('all_found_courses' in prereq_obj.other_requirements) {
      // iterate course group, insert if not already in array
      all_valid_courses.forEach(course => {
        if (!prereq_obj.other_requirements.all_found_courses?.includes(course)) {
          prereq_obj.other_requirements.all_found_courses?.push(course);
        }
      });
    } else {
      prereq_obj.other_requirements.all_found_courses = all_valid_courses;
    }
  } else {
    // one course only
    const one_course_filter: RegExp = /(^[a-z]{4}[0-9]{4})| [\(]?([a-z]{4}[0-9]{4})[-,\)]?| ([a-z]{4}[0-9]{4})$/gmi;
    const one_course_match = creq_str.match(one_course_filter);
    if (one_course_match) {
      const one_coreq: string = _.trim(one_course_match[0], ' -,()').toUpperCase();
      if (one_coreq in courses) {
        prereq_obj.other_requirements.corequisites = [one_coreq];
        // if single coreq course is not found in all_found_courses attribute, just insert into unlocked_by
        if (!prereq_obj.other_requirements.all_found_courses?.includes(one_coreq)) prereq_obj.unlocked_by.push(one_coreq + ' (c)');
        // insert single coreq course into all_found_courses if not found
        if ('all_found_courses' in prereq_obj.other_requirements) {
          if (!prereq_obj.other_requirements.all_found_courses?.includes(one_coreq)) prereq_obj.other_requirements.all_found_courses?.push(one_coreq);
        } else {
          prereq_obj.other_requirements.all_found_courses = [one_coreq];
        }
      }
    }
  }
  //console.log(prereq_obj.other_requirements.all_found_courses)
  //console.log(prereq_obj.unlocked_by);
  //console.log('\n\n')

  return prereq_obj;
}

// get course list, check if they are in courses.json, 
// check if course already exists inside exclusion_courses, if not append 
const process_excl_section = (excl_str: string, exclusion_courses: string[]): string[] => {
  if (excl_str === "") return exclusion_courses;
  const found_excl_courses: string[] = compile_course_list(excl_str, false);
  found_excl_courses.forEach(course => {
    if (!exclusion_courses.includes(course)) exclusion_courses.push(course);
  })
  return exclusion_courses;
}

const process_equiv_section = (equiv_str: string, equivalent_courses: string[]): string[] => {
  if (equiv_str === "" && equivalent_courses.length === 0) return equivalent_courses;
  const found_equiv_courses: string[] = compile_course_list(equiv_str, false);
  found_equiv_courses.forEach(course => {
    if (!equivalent_courses.includes(course)) equivalent_courses.push(course);
  })
  return equivalent_courses;
}

const compile_course_list = (cgroup_str: string, check_valid_course: boolean): string[] => {
  let compiled_courses: string[] = Array.from(cgroup_str.matchAll(/[a-z]{4}[0-9]{4}/gmi), ccode => ccode[0].toUpperCase());
  if (check_valid_course) compiled_courses = compiled_courses.filter(code => code in courses);
  return compiled_courses;
}

const clean_string = (str: string): string => {
  let cstr: string = _.trim(str, ',.;: ');
  cstr = cstr.replace(/ {2,}/g, ' ');
  cstr = cstr.replace(/ (and|or)$/gi, '');
  cstr = cstr.replace(/([0-9])(or|and)/gmi, "$1 $2");
  cstr = cstr.replaceAll(/([0-9]+)( *uoc| *units* of credits*)/gmi, '$1UOC'); // 422 matches
  return cstr;
}

const initialise_prereq_obj = (prereq_str: string, exclusion_courses: string[], equivalent_courses: string[]): Prereq => {
  let prereq_obj: Prereq = {
    'equivalent_courses': equivalent_courses,
    'exclusion_courses': exclusion_courses,
    'unlocked_by': [],
    'unlocks': [],
    'other_requirements': {
    }
  }
  if (prereq_str === "None" || prereq_str === "") return prereq_obj 
  if (prereq_str !== "") prereq_obj.other_requirements.raw_str = prereq_str;
  return prereq_obj;
}

export default process_prereq;