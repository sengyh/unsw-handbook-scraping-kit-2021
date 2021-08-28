import * as schools from '../../data/json/schools.json';
import * as subjects from '../../data/json/subjects.json';
import * as sub_val_name from '../../data/json/name_to_code/subject_val_key.json';
import type { SpecStructure, SpecStructBody, ProcessedStructBody, SubValKeyObj, Schools } from '../custom_types';
import {clean_course_group_str, construct_unlocked_by_arr} from '../courses/prereq_section_helpers';
import * as _ from 'lodash';

export const extract_all_found_courses = (body: SpecStructBody): string[] => {
  let all_found_courses: string[] = [];
  const course_pattern: RegExp = /[a-z]{4}[0-9]{4}(\/[0-9]{4})?/gmi;
  const course_group_pattern: RegExp = /([a-z]{4}\/)*[\[(]*[a-z]{4}?[0-9]{4}.*[ \/(,][a-z]{4}[0-9]{4}[\])]*(\/\d{4})*/gmi;
  // special edge case for exclusion of math stats courses
  if (body.description.match(/may not undertake|University of Sydney/gmi)) return [];
  // handles 'one of the following' case
  const one_of_arr: string[] = Array.from(body.description.matchAll(/one of the following: \n{1,}(- [a-z]{4}[0-9]{4}.*?\n{1,}){2,}(- [a-z]{4}[0-9]{4})?/gmi), match => match[0].replaceAll(/\n{1,}/gm, ' '));
  if (one_of_arr.length > 0) { 
    one_of_arr.forEach(elem => {
      const one_of_str_elem: string = Array.from(elem.matchAll(/[a-z]{4}[0-9]{4}/gmi), match => match[0]).join(' | ');
      all_found_courses.push(one_of_str_elem);
    })
  }
  const body_desc_arr: string[] = body.description.replaceAll(/\n{2,}/gm, '\n').split('\n').map(elem => _.trim(elem, ' *\t-,')).filter(elem => elem !== "");
  body_desc_arr.forEach(elem => {
    const course_match_arr: string[] = Array.from(elem.matchAll(course_pattern), elem => elem[0]);
    const cgroup_match = elem.match(course_group_pattern);
    // do not question the matches, it's there for a reason
    if (course_match_arr.length >= 2 && cgroup_match && !elem.match(/(is replaced by|note:|counted in-place)/gmi)) {
      if (cgroup_match[0].match(/ a prerequisite for /gmi)) {
        all_found_courses.push(course_match_arr[0]);
      } else {
        let cleaned_cg_str: string = clean_course_group_str(cgroup_match[0]);
        cleaned_cg_str = cleaned_cg_str.replaceAll(/([a-z]{4}[0-9]{4}) ([a-z]{4}[0-9]{4})/gmi, '$1 AND $2');
        if (cleaned_cg_str.match(/^\([a-z]{4}[0-9]{4} AND [a-z]{4}[0-9]{4}\)$/gmi)) cleaned_cg_str = _.trim(cleaned_cg_str, '()');
        all_found_courses = all_found_courses.concat([...new Set(construct_unlocked_by_arr(cleaned_cg_str))]);
      }  
    } else if (course_match_arr.length === 1) {
      // handles extra '/[0-9]{4}' case
      const one_course: string = clean_course_group_str(course_match_arr[0]).replace(/ OR /gm, ' | ');
      const re = new RegExp(one_course, "gm");
      let exists_in_afc: boolean = false;
      all_found_courses.forEach(elem => {if (elem.match(re)) exists_in_afc = true});
      if (!exists_in_afc) all_found_courses.push(one_course);
    } else {
      // handles all 'any XXX course' cases
      const processed_any_cstr: string[] = process_any_course_str(elem);
      all_found_courses = all_found_courses.concat(processed_any_cstr);
    }
  })  
  return all_found_courses;
}

export const process_any_course_str = (any_course_str: string): string[] => {
  // any level X SUB course
  // the design decision i made with sub_val (' | ' delimiter) will come back and bite me in the ass
  // too lazy to fix this, will come back to this later
  const level_w_sub_pattern: RegExp = /^any (level [0-9]) ([a-z ]+).*course/gmi
  let level_arr: string[] = Array.from(any_course_str.matchAll(level_w_sub_pattern), m => m[1]);
  const sub_arr: string[] = Array.from(any_course_str.matchAll(level_w_sub_pattern), m => _.trim(m[2]));
  if (level_arr.length === 1 && sub_arr.length === 1) {
    let course_code: string = "";
    const sv_name: SubValKeyObj = sub_val_name;
    const sub: string = sub_arr[0]
    if (sub in sv_name) {
      // TODO: edge case: ' | ' delimiter, need to split and apply to every element if exists
      course_code += sv_name[sub];
      course_code += level_arr[0].replace(/level /gmi, '') + '___';
      return [course_code];
    }
  }
  // any level X course
  const only_level_pattern: RegExp = /^any (level [0-9]) course$/gmi
  level_arr = Array.from(any_course_str.matchAll(only_level_pattern), m => m[1]);
  if (level_arr.length === 1) {
    let course_code = 'XXXX' + level_arr[0].replace(/level /gmi, '') + '___';
    return [course_code];
  }
  // any level X course offered by SCH
  const level_w_sch_pattern: RegExp = /^any (level [0-9]) course.*(School.*)/gmi;
  level_arr = Array.from(any_course_str.matchAll(level_w_sch_pattern), m => m[1]);
  let sch_arr = Array.from(any_course_str.matchAll(level_w_sch_pattern), m => m[2]);
  if (level_arr.length === 1 && sch_arr.length === 1) {
    const sch_obj: Schools = schools;
    const sch: string = sch_arr[0];
    if (sch in sch_obj) {
      const sch_subs: string[] = sch_obj[sch].subjects;
      const sch_course_codes: string[] = sch_subs.filter(sub => sub !== 'ENGG').map(sub => sub + level_arr[0].replace(/level /gmi, '') + '___');
      return sch_course_codes;
    }
  }
  // pattern already given 
  const course_pattern: RegExp = /[A-Z]{4}[0-9]{2}#{2}/gm;
  const course_pattern_match = any_course_str.match(course_pattern);
  if (course_pattern_match) return [course_pattern_match[0].replaceAll(/#/gm, '_')];

  return [];
}

export const extract_min_uoc = (desc_str: string): string => {
  const first_line: string = _.trim(desc_str, ' \n').split('\n')[0];
  const min_uoc_pattern: RegExp = /must (take|complete)( a minimum of| at least)? [0-9]+ uoc/gmi;
  let min_uoc: string = "";
  const min_uoc_match = first_line.match(min_uoc_pattern);
  if (!first_line.match(/^if/gmi) && min_uoc_match) {
    min_uoc = min_uoc_match[0].replace(/[^\d]/gm, '');
  }
  return min_uoc;
}

export const extract_max_uoc = (desc_str: string): string => {
  const first_line: string = _.trim(desc_str, ' \n').split('\n')[0];
  const max_uoc_pattern: RegExp = /( up to| a maximum of) [0-9]+ uoc/gmi;
  let max_uoc: string = "";
  const max_uoc_match = first_line.match(max_uoc_pattern);
  if (max_uoc_match) {
    max_uoc = max_uoc_match[0].replace(/[^\d]/gm, '');
  }
  return max_uoc;
}

export const extract_uoc_range = (desc_str: string): string => {
  let uoc_range: string = "";
  const uoc_range_pattern: RegExp = / [0-9]+- ?[0-9]+ UOC/gmi;
  const uoc_range_match = desc_str.match(uoc_range_pattern);
  if (uoc_range_match) uoc_range = uoc_range_match[0].replaceAll(/[a-z ]/gmi, '');
  return uoc_range;
}

export const get_new_uoc = (min_uoc: string, max_uoc: string): string => {
  let new_uoc: string = "";
  if (max_uoc !== "") {
    if (min_uoc !== "" ) {
      if (min_uoc === max_uoc) {
        new_uoc = min_uoc;
      } else {
        new_uoc = min_uoc + '-' + max_uoc;
      }     
    } else {
      new_uoc = '0-' + max_uoc;
    }
  } else {
    if (min_uoc !== "") {
      new_uoc = min_uoc;
    }
  }
  return new_uoc;
}