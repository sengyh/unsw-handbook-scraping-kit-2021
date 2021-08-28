import {} from '../courses/prereq_section_helpers'
import type { SpecStructure, SpecStructBody, ProcessedStructBody, SubValKeyObj, Schools } from '../custom_types';
import {clean_course_group_str, construct_unlocked_by_arr} from '../courses/prereq_section_helpers';
import { extract_all_found_courses } from './spec_element_helper';
import * as _ from 'lodash';

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
  if (body.courses.length === 0 && body.description !== "") {
    const all_found_courses: string[] = extract_all_found_courses(body);
    console.log(body.description)
    console.log(all_found_courses)
    console.log('')
  }
  return;
}