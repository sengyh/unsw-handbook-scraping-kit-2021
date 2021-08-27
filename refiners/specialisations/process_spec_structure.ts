import * as courses from '../../data/json/refined_courses.json'
import {} from '../courses/prereq_section_helpers'
import type { SpecStructure, SpecStructBody, ProcessedStructBody } from '../custom_types';
import {clean_course_group_str, construct_unlocked_by_arr} from '../courses/prereq_section_helpers';
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
  const course_group_pattern: RegExp = /([a-z]{4}\/)*[\[(]*[a-z]{4}?[0-9]{4}.*[ \/(,][a-z]{4}[0-9]{4}[\])]*(\/\d{4})*/gmi;
  if (body.courses.length === 0 && body.description !== "" && !body.description.match(/University of Sydney/gmi)) {
    const body_desc_arr: string[] = body.description.replaceAll(/\n{2,}/gm, '\n').split('\n').map(elem => _.trim(elem, ' *\t-,')).filter(elem => elem !== "");
    body_desc_arr.forEach(elem => {
      const course_match_arr: string[] = Array.from(elem.matchAll(course_pattern), elem => elem[0]);
      const cgroup_match = elem.match(course_group_pattern)
      if (course_match_arr.length >= 2 && cgroup_match && !elem.match(/(is replaced by|note:|counted in-place)/gmi)) {
        if (cgroup_match[0].match(/ a prerequisite for /gmi)) {
          course_match_arr[0];
        } else {
          console.log(elem)
          let cleaned_cg_str: string = clean_course_group_str(cgroup_match[0]);
          cleaned_cg_str = cleaned_cg_str.replaceAll(/([a-z]{4}[0-9]{4}) ([a-z]{4}[0-9]{4})/gmi, '$1 AND $2');
          //console.log(cleaned_cg_str)
          if (cleaned_cg_str.match(/^\([a-z]{4}[0-9]{4} AND [a-z]{4}[0-9]{4}\)$/gmi)) cleaned_cg_str = _.trim(cleaned_cg_str, '()');
          console.log(construct_unlocked_by_arr(cleaned_cg_str))
          console.log('\n')
        }  
      }
    })
  }
  return;
}
