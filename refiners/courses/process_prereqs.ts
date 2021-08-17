import * as _ from "lodash";
import { parse } from "path/posix";
import { start } from "repl";
import split_raw_prereq_str from "./split_raw_prereq_str";

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
  }
  let uoc_str = parse_uoc_req(preq_str);
  if (uoc_str !== "") {
    const uoc_req: number = parseInt(uoc_str);
    if (uoc_req > 12 || (uoc_req === 12 && preq_str.match(/^12UOC/g))) {
      //console.log(preq_str)
      const lvl_req: number = parse_lvl_req(preq_str);
      if (lvl_req > 0) {
        // make attribute
      }
    }
    const sub_req: string | null = parse_sub_req(preq_str);
    if (sub_req) {
      // make attr
    }
  }
  return;
}

// extract wam req: 16 back, 11 front
const parse_wam_req = (preq_str: string): string => {
  let wam_str: string = "";
  const wam_back_pattern: RegExp = /(wam.* \d{2}[ .,])|(wam.* \d{2}$)/gmi;
  const wam_front_pattern: RegExp = /([> ]\d{2}[+ ]*wam)|(^\d{2}[+]* *wam)/gmi;
  let wam_match = preq_str.match(wam_back_pattern);
  if (wam_match === null) wam_match = preq_str.match(wam_front_pattern);
  if (wam_match) {
    wam_str = wam_match[0];
    wam_str = wam_str.replace(/[^0-9]/gmi, '');
  }
  return wam_str;
}

const parse_uoc_req = (preq_str: string): string => {
  let uoc_str: string = "";
  const uoc_pattern: RegExp = /\d{2,}UOC/gm;
  let uoc_match = preq_str.match(uoc_pattern);
  if (uoc_match) {
    uoc_str = uoc_match[0];
    uoc_str = uoc_str.replace(/[^0-9]/gmi, '');
  }
  return uoc_str;
}

const parse_lvl_req = (preq_str: string): number => {
  const level_pattern: RegExp = /^\d{2,}UOC (or|in|at) level ([0-9])/gi;
  let level_req: number = -1;
  if (preq_str.match(level_pattern)) {
    level_req = parseInt(preq_str.replace(level_pattern, '$2'));
  }
  return level_req;
}

const parse_sub_req = (preq_str: string): string | null => {
  const sub_pattern = /\d{2,}UOC (or|in|at) (level [0-9] )*([a-z]{4} courses)/gmi;
  let sub_match = preq_str.match(sub_pattern)
  if (sub_match) {
    let sub_match_str: string = sub_match[0].replace(/ Level \d+/gmi, '');
    const sub_req: string = sub_match_str.replace(/\d{2,}UOC (or|in|at) ([a-z]{4}) courses/gmi, '$2').slice(0,4).toUpperCase();
    console.log(sub_req);
    return sub_req;
  }
  return null;
}


  // /([0-9]+)( *uoc| *units* of credits*)/gmi : 422 matches

  // /level *([0-9]+)/gmi : 158 matches

  // capture course group (has more than one course)
  // /[\[(]*[a-z]{4}[0-9]{4}.*[a-z]{4}[0-9]{4}[\])]*/gmi : 616 matches


export default process_prereq;