import type { SpecStructure, SpecStructBody, ProcessedStructBody, OtherInfoElem, ProcStructObj } from '../custom_types';
import { extract_all_found_courses, process_any_course_str, extract_min_uoc, extract_max_uoc, extract_uoc_range, get_new_uoc } from './spec_element_helper';
import * as _ from 'lodash';

export const process_spec_structure = (spec_structure: SpecStructure): ProcStructObj => {
  let course_structure_arr: ProcessedStructBody[] = [];
  let other_information_arr: OtherInfoElem[] = [];
  for (let [key, val] of Object.entries(spec_structure)) {
    if (key === "default") continue;
    const struct_obj_title: string = key;
    const struct_obj_body: SpecStructBody = val;
    const processed_struct_elem: ProcessedStructBody = construct_spec_element(struct_obj_title, struct_obj_body);
    if (processed_struct_elem.courses.length === 0 && processed_struct_elem.uoc === "") {
      const misc_info: OtherInfoElem = {
        name: processed_struct_elem.name, 
        description: processed_struct_elem.description
      };
      other_information_arr.push(misc_info);
    } else {
      course_structure_arr.push(processed_struct_elem);
    }
  }
  const processed_spec_structure_obj: ProcStructObj = {
    course_structure: course_structure_arr,
    more_information: other_information_arr
  };
  //console.log(JSON.stringify(processed_spec_structure_obj, null,2))
  return processed_spec_structure_obj;
}

export const construct_spec_element = (title: string, body: SpecStructBody): ProcessedStructBody => { 
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

  let processed_course_arr: string[] = [];
  new_body.courses.forEach(course_str => {
    let processed_course_str = process_any_course_str(course_str);
    if (processed_course_str.length === 0) {
      processed_course_arr.push(course_str);
    } else {
      processed_course_arr = processed_course_arr.concat(processed_course_str);
    }
  });
  new_body.courses = _.uniq(processed_course_arr);

  const processed_struct_body: ProcessedStructBody = {
    'name': title,
    'uoc': new_body.uoc,
    'description': new_body.description,
    'courses': new_body.courses
  }
  //console.log(JSON.stringify(processed_struct_body, null,2));
  return processed_struct_body;
}
