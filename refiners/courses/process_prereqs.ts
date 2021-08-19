import * as _ from "lodash";
import { parse } from "path/posix";
import { start } from "repl";
import split_raw_prereq_str from "./split_raw_prereq_str";
import * as courses from '../../data/json/raw/courses.json';
import { parse_wam_req, parse_uoc_req, parse_lvl_req, parse_sub_req, parse_prog_req, parse_spec_req } from './prereq_section_helpers'

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
  if (prereq_str === 'None' || prereq_str === '') {
    //console.log(JSON.stringify(prereq_obj, null, 2))
    return prereq_obj;
  } 
  const [prereq_section, coreq_section, excl_section, equiv_section, misc_section]: string[] = split_raw_prereq_str(prereq_str);
  //console.log(clean_string(prereq_section));
  //console.log(clean_string(coreq_section));
  //console.log(clean_string(excl_section));
  //console.log(clean_string(equiv_section));
  //console.log(clean_string(misc_section));

  prereq_obj = process_preq_section(prereq_section, curr_course, prereq_obj);
  // prereq_obj = process_creq_section(coreq_section, prereq_obj);
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
    //process.stdout.write(curr_course + ': \t');
    //course_group?.forEach(str => console.log(str));
    let course_group: string = course_group_match[0];
    course_group = clean_course_group_str(course_group);
    //console.log(course_group)
  } else {
    // check for one course
  }
  
  // only one course group
  // if no course group, check for individual course


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

const process_creq_section = (creq_str: string, prereq_obj: Prereq): Prereq => {
  if (creq_str === "") return prereq_obj;
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

const clean_course_group_str = (cgroup_str: string): string => {
  cgroup_str = cgroup_str.replace(/ (and)([a-z0-9])/gmi, ' $1 $2');
  cgroup_str = cgroup_str.replace(/(and)\/(or)/gmi, '$2');
  cgroup_str = cgroup_str.replace(/\. Highly recommended.*/gmi, '');
  cgroup_str = cgroup_str.replaceAll(/[,.] *(and|or)[,.]?/gmi, ' $1 ');
  cgroup_str = cgroup_str.replaceAll(/ ,/gmi, ',');
  cgroup_str = cgroup_str.replaceAll(/&/gmi, 'and');
  cgroup_str = cgroup_str.replaceAll(/\[/gmi, '(');
  cgroup_str = cgroup_str.replaceAll(/\]/gmi, ')');
  cgroup_str = cgroup_str.replaceAll(/;/gmi, ' and ');
  cgroup_str = cgroup_str.replaceAll(/([A-Z]{4}) ([0-9]{4})/gm, '$1$2');
  cgroup_str = cgroup_str.replaceAll(/ \)/gm, ')');
  // curr: / and|[( ]or|(([a-z]{4}\/)?[\(]?[a-z]{4}[0-9]{4}[\),]?)(([/][0-9]{4}[,]?)+|)|[&/]/gmi
  const tokenise: RegExp = / and|[( ]or|(([a-z]{4}\/)?[\(]?[a-z]{4}[0-9]{4}[\),]?)(([/][0-9]{4}[,]?)+|)|[&/]/gmi;
  const match_str_tokens: string[] = Array.from(cgroup_str.matchAll(tokenise), token => token[0].toUpperCase());
  let new_cgs: string = match_str_tokens.join(' ').replaceAll(/ {2,}/gm, ' ');
  new_cgs = new_cgs.replaceAll(/\) \(/gm, '), (')
  console.log(new_cgs)

  // if there is case where (or|and) is followed by (or|and), pick latter

  //console.log(cgroup_str)
  return cgroup_str;
}

const parse_course_slashes = (cgroup_str: string): string => {
  // filter cases with slashes but no sub code included, fill in code
  // /([a-z]{4}[0-9]{4})(\/[0-9]{4})+/gmi
  return "";
}

export default process_prereq;