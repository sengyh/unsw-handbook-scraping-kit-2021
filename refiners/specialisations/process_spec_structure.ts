import {} from '../courses/prereq_section_helpers'
import type { SpecStructure, SpecStructBody, ProcessedStructBody, SubValKeyObj, Schools } from '../custom_types';
import {clean_course_group_str, construct_unlocked_by_arr} from '../courses/prereq_section_helpers';
import { extract_all_found_courses, extract_min_uoc, extract_max_uoc, extract_uoc_range, get_new_uoc } from './spec_element_helper';
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
    new_body.courses = _.uniq(all_found_courses);
  }
  // get min uoc if there are courses but no uoc entry
  let new_uoc: string = "";
  if (new_body.courses.length > 0 && new_body.uoc === "") {
    const min_uoc: string = extract_min_uoc(new_body.description);
    const max_uoc: string = extract_max_uoc(new_body.description);
    new_uoc = get_new_uoc(min_uoc, max_uoc);
    if (new_uoc === "") new_uoc = extract_uoc_range(new_body.description);
    new_body.uoc = new_uoc;
  }
  const processed_struct_body: ProcessedStructBody = {
    'name': title,
    'uoc': new_body.uoc,
    'description': new_body.description,
    'courses': new_body.courses
  }
  console.log(JSON.stringify(processed_struct_body, null,2));
  return;
}
