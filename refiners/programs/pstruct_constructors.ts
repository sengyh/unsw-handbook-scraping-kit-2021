import * as _ from 'lodash';
import type {ProcessedProgramStructure, ProcessedPCourseObj, SpecElem, OtherInfoElem, SpecStructure, SpecStructBody} from '../custom_types';
import { construct_spec_element } from "../specialisations/process_spec_structure";
import { process_any_course_str } from '../specialisations/spec_element_helper';

export const construct_refined_program_structure = (): ProcessedProgramStructure => {
  return {
    'core_structure_uoc': 0,
    'core_structure_desc': "",
    'core_specialisations': [],
    'optional_specialisations': [],
    'core_course_component': [],
    'misc_course_components': [],
    'more_information': [],
  }
}


export const construct_refined_spec_obj = (curr_obj_key: string, lv2_struct_obj: any): SpecElem => {
  let new_rspec_block: SpecElem = {
    name: "",
    description: "",
  }
  if (!('name' in lv2_struct_obj)) {
    new_rspec_block.name = curr_obj_key;
  } else {
    new_rspec_block.name = lv2_struct_obj.name;
  }
  new_rspec_block.description = lv2_struct_obj.requirements;
  const lv2_keys: string[] = Object.keys(lv2_struct_obj);
  lv2_keys.forEach(key => {
    const potential_spec_arr: any = lv2_struct_obj[key];
    if (Array.isArray(potential_spec_arr)) {
      new_rspec_block = {...new_rspec_block, ...{[key]: potential_spec_arr}}
    }
  })
  return new_rspec_block;
}

export const construct_refined_course_obj = (curr_obj_key: string, course_obj_org: any): ProcessedPCourseObj => {
  // so far all objects that contains course_groups have 'name' key, so just return obj
  if ('course_groups' in course_obj_org) {
    return {
      'name': curr_obj_key,
      'uoc': course_obj_org.uoc,
      'description': course_obj_org.requirements,
      'courses': [],
      'course_groups': course_obj_org.course_groups
    };
  }

  let refined_course_obj: ProcessedPCourseObj = {
    'name': curr_obj_key,
    'uoc': course_obj_org.uoc,
    'description': course_obj_org.requirements,
    'courses': course_obj_org.courses
  };
  
  // do not process any 'blocks' that contains program restrictions (e.g 'max lv1 uoc courses', 'excluded gen ed' and maturity requirements)
  // todo: refine them into 'misc info' block
  const misc_info_key_pattern: RegExp = /^(max|minimum and max|(level 1 uoc|level 1 maximum)|LANTITE)|rule|req|excl|maturity/gmi;
  if (curr_obj_key.match(misc_info_key_pattern)) return refined_course_obj;

  // course objs that do not match ^ are processed
  if (course_obj_org.courses.length === 0) {
    refined_course_obj = construct_spec_element(curr_obj_key, refined_course_obj);
    if (curr_obj_key.match(/minimum/gmi)) refined_course_obj.uoc = "";
  } else {
    let processed_course_arr: string[] = [];
    refined_course_obj.courses.forEach(course_str => {
      let processed_course_str = process_any_course_str(course_str);
      if (processed_course_str.length === 0) {
        processed_course_arr.push(course_str);
      } else {
        processed_course_arr = processed_course_arr.concat(processed_course_str);
      }
    });
    refined_course_obj.courses = _.uniq(processed_course_arr);
  }
  //console.log(JSON.stringify(refined_course_obj, null, 2));
  return refined_course_obj;
}