import {} from '../courses/prereq_section_helpers'
import type { SpecStructure, SpecStructBody, ProcessedStructBody, SubValKeyObj, Schools } from '../custom_types';
import {clean_course_group_str, construct_unlocked_by_arr} from '../courses/prereq_section_helpers';
import { extract_all_found_courses } from './spec_element_helper';
import * as _ from 'lodash';
import { min } from 'lodash';

export const process_spec_structure = (spec_structure: SpecStructure): void => {
  let processed_structure_arr: ProcessedStructBody[] = [];
  for (let [key, val] of Object.entries(spec_structure)) {
    if (key === "default") continue;
    const struct_obj_title: string = key;
    const struct_obj_body: SpecStructBody = val;
    //const processed_struct_obj_elem: ProcessedStructBody = 
    construct_spec_element(struct_obj_title, struct_obj_body);
  }
  return;
}

const construct_spec_element = (title: string, body: SpecStructBody): void => { 
  // going to trust (lol) that the handbook ppl know their shit and that they did not leave any courses behind if the section already has courses. also, screw usyd.
  let new_body: SpecStructBody = _.cloneDeep(body);
  if (body.courses.length === 0 && body.description !== "") {
    const all_found_courses: string[] = extract_all_found_courses(body);
    new_body.courses = all_found_courses;
  }
  // get min uoc if there are courses but no uoc entry
  let new_uoc: string = "";
  let min_uoc: string = "";
  let max_uoc: string = "";
  if (new_body.courses.length > 0 && new_body.uoc === "") {
    min_uoc = extract_min_uoc(new_body.description);
    max_uoc = extract_max_uoc(new_body.description);
    new_uoc = get_new_uoc(min_uoc, max_uoc);
    //console.log(_.trim(new_body.description, ' \n').split('\n')[0]);
    //console.log(new_uoc + '\n');
  }
  return;
}

const extract_min_uoc = (desc_str: string): string => {
  const first_line: string = _.trim(desc_str, ' \n').split('\n')[0];
  const min_uoc_pattern: RegExp = /must (take|complete)( a minimum of| at least)? [0-9]+ uoc/gmi;
  let min_uoc: string = "";
  const min_uoc_match = first_line.match(min_uoc_pattern);
  if (!first_line.match(/^if/gmi) && min_uoc_match) {
    min_uoc = min_uoc_match[0].replace(/[^\d]/gm, '');
  }
  return min_uoc;
}

const extract_max_uoc = (desc_str: string): string => {
  const first_line: string = _.trim(desc_str, ' \n').split('\n')[0];
  const max_uoc_pattern: RegExp = /( up to| a maximum of) [0-9]+ uoc/gmi
  let max_uoc: string = "";
  const max_uoc_match = first_line.match(max_uoc_pattern);
  if (max_uoc_match) {
    max_uoc = max_uoc_match[0].replace(/[^\d]/gm, '');
  }
  return max_uoc;
}

const get_new_uoc = (min_uoc: string, max_uoc: string): string => {
  let new_uoc: string = "";
  if (max_uoc !== "") {
    if (min_uoc !== "" ) {
      if (min_uoc === max_uoc) {
        new_uoc = min_uoc;
      } else {
        new_uoc = min_uoc + '-' + max_uoc;
      }     
    } else {
      new_uoc = '0-' + max_uoc
    }
  } else {
    if (min_uoc !== "") {
      new_uoc = min_uoc;
    }
  }
  return new_uoc;
}