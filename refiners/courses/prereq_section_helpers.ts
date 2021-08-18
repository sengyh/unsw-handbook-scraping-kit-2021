import * as programs from '../../data/json/raw/programs.json';
import * as ddegs from '../../data/json/raw/double_degrees.json';
import * as _ from "lodash";

// HELPERS
// extract wam req: 16 back, 11 front
export const parse_wam_req = (preq_str: string): string => {
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

// returns first uoc match cause it will always be the greatest (for now at least)
export const parse_uoc_req = (preq_str: string): string => {
  let uoc_str: string = "";
  const uoc_pattern: RegExp = /\d{2,}UOC/gm;
  let uoc_match = preq_str.match(uoc_pattern);
  if (uoc_match) {
    uoc_str = uoc_match[0];
    uoc_str = uoc_str.replace(/[^0-9]/gmi, '');
  }
  return uoc_str;
}

// only get lvl req if uoc req exists and is greater than 12 (unless 12 appears at start of line)
export const parse_lvl_req = (preq_str: string): number => {
  const level_pattern: RegExp = /^\d{2,}UOC (or|in|at) level ([0-9])/gi;
  let level_req: number = -1;
  if (preq_str.match(level_pattern)) {
    level_req = parseInt(preq_str.replace(level_pattern, '$2'));
  }
  return level_req;
}

// only get sub req if level req exists
export const parse_sub_req = (preq_str: string): string | null => {
  const sub_pattern = /\d{2,}UOC (or|in|at) (level [0-9] )*([a-z]{4} courses)/gmi;
  let sub_match = preq_str.match(sub_pattern)
  if (sub_match) {
    let sub_match_str: string = sub_match[0].replace(/ Level \d+/gmi, '');
    const sub_req: string = sub_match_str.replace(/\d{2,}UOC (or|in|at) ([a-z]{4}) courses/gmi, '$2').slice(0,4).toUpperCase();
    //console.log(sub_req);
    return sub_req;
  }
  return null;
}

// only gets programs which are currently offered
// pattern: if 'program' exists check for 4 digit sequence that aren't course codes
export const parse_prog_req = (preq_str: string): string[] => {
  let req_progs: string[] = [];
  let prog_code_pattern: RegExp = /([ ,(][0-9]{4}[, )])|([ ,][0-9]{4}$)|(^[0-9]{4})/gmi;
  if (preq_str.match(/program/gmi)) {
    let compiled_progs = Array.from(preq_str.matchAll(prog_code_pattern), pcode => _.trim(pcode[0], ' ,()'));
    req_progs = compiled_progs.filter(code => code in programs || code in ddegs);
  }
  return req_progs;
}
