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

const process_prereq = (prereq_str: string, exclusion_courses: string[], equivalent_courses: string[]): Prereq => {
  let prereq_obj: Prereq = initialise_prereq_obj(prereq_str, exclusion_courses, equivalent_courses)
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

  prereq_obj = process_preq_section(prereq_section, prereq_obj);
  // prereq_obj = process_creq_section(coreq_section, prereq_obj);
  prereq_obj.exclusion_courses = process_excl_section(excl_section, exclusion_courses);
  prereq_obj.equivalent_courses = process_equiv_section(equiv_section, equivalent_courses);
  //if (prereq_obj.exclusion_courses.length > 0 || prereq_obj.equivalent_courses.length > 0) {
  //  console.log(JSON.stringify(prereq_obj, null, 2));
  //}
  console.log(JSON.stringify(prereq_obj, null, 2));
  return prereq_obj;
}

const process_preq_section = (preq_section: string, prereq_obj: Prereq): Prereq => {
  const preq_str = clean_string(preq_section);
  // maybe get all found codes into an all list, use this to fill unlocks
  // ci: boolean expression
  //process.stdout.write(preq_str + ' -');
  let course_group = preq_str.match(/[\[(]*[a-z]{4}[0-9]{4}.*[a-z]{4}[0-9]{4}[\])]*/gmi);
  //course_group?.forEach(str => console.log(str));
  // only one course group
  // if no course group, check for individual course

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

export default process_prereq;