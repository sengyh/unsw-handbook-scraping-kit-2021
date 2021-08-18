import * as _ from "lodash";
import { parse } from "path/posix";
import { start } from "repl";
import split_raw_prereq_str from "./split_raw_prereq_str";
import * as courses from '../../data/json/raw/courses.json';
import { parse_wam_req, parse_uoc_req, parse_lvl_req, parse_sub_req, parse_prog_req } from './prereq_section_helpers'


export type Prereq = {
  unlocked_by: string[];
  other_requirements: {
    uoc?: number;
    wam?: number;
    programs?: number[];
    specialisation?: string;
    raw_prereq?: string;
  };
}

const process_prereq = (prereq_str: string): Prereq => {
  let prereq_obj: Prereq = {unlocked_by: [], other_requirements: {}}
  if (prereq_str === 'None' || prereq_str === '') {
    //console.log("n/a")
    return prereq_obj;
  }
  const [prereq_section, coreq_section, excl_section, equiv_section, misc_section]: string[] = split_raw_prereq_str(prereq_str);
  //console.log(clean_string(prereq_section));
  //console.log(clean_string(coreq_section));
  //console.log(clean_string(excl_section));
  //console.log(clean_string(equiv_section));
  //console.log(clean_string(misc_section));

  process_preq_section(prereq_section);
  //process_creq_section(coreq_section);
  //process_excl_section(excl_section);
  //process_equiv_section(equiv_section);
  
  return prereq_obj;
}

const clean_string = (str: string): string => {
  let cstr: string = _.trim(str, ',.;: ');
  cstr = cstr.replace(/ {2,}/g, ' ');
  cstr = cstr.replace(/ (and|or)$/gi, '');
  cstr = cstr.replace(/([0-9])(or|and)/gmi, "$1 $2");
  cstr = cstr.replaceAll(/([0-9]+)( *uoc| *units* of credits*)/gmi, '$1UOC'); // 422 matches
  return cstr;
}

const process_preq_section = (preq_section: string): void => {
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
    // make attribute
  }
  let uoc_str = parse_uoc_req(preq_str);
  if (uoc_str !== "") {
    const uoc_req: number = parseInt(uoc_str);
    if (uoc_req > 12 || (uoc_req === 12 && preq_str.match(/^12UOC/g))) {
      const lvl_req: number = parse_lvl_req(preq_str);
      if (lvl_req > 0) {
        // make attribute
      }
    }
    const sub_req: string | null = parse_sub_req(preq_str);
    if (sub_req) {
      // make attribute
    }
  }
  let prog_arr = parse_prog_req(preq_str);
  return;
}

const process_creq_section = (creq_str: string): void => {
  return;
}

// get course list, check if they are in courses.json, 
// check if course already exists inside exclusion_courses, if not append 
const process_excl_section = (excl_str: string): void => {
  if (excl_str === "") return;
  console.log(excl_str);
  compile_course_list(excl_str);
  return;
}

const process_equiv_section = (equiv_str: string): void => {
  return;
}

const compile_course_list = (cgroup_str: string): string[] => {
  let compiled_courses: string[] = Array.from(cgroup_str.matchAll(/[a-z]{4}[0-9]{4}/gmi), ccode => ccode[0].toUpperCase());
  //compiled_courses = compiled_courses.filter(code => code in courses);
  console.log(compiled_courses)
  return compiled_courses;
}

export default process_prereq;