import * as courses from '../../data/json/refined_courses.json'
import type { SpecStructure, SpecStructBody, ProcessedStructBody } from '../custom_types';
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
  const course_pattern: RegExp = /[a-z]{4}[0-9]{4}/gmi;
  if (body.courses.length === 0 && body.description !== "") {
    const body_desc_arr: string[] = body.description.replaceAll(/\n{2,}/gm, '\n').split('\n').map(elem => _.trim(elem, ' *\t-,')).filter(elem => elem !== "");
    console.log(body_desc_arr);
  }
  return;
}
