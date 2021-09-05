import type {ProcessedProgramStructure, ProcessedStructBody, SpecElem, OtherInfoElem} from '../custom_types';
import { construct_spec_element } from "../specialisations/process_spec_structure";


export const construct_refined_program_structure = (): ProcessedProgramStructure => {
  return {
    'core_structure_uoc': 0,
    'core_structure_desc': "",
    'core_specialisations': [],
    'optional_specialisations': [],
    'core_course_component': [],
    'more_courses': [],
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

export const construct_refined_course_obj = (curr_obj_key: string, course_obj_org: any): void => {
  
  if ('name' in course_obj_org) {
    if (curr_obj_key !== course_obj_org.name) console.log(curr_obj_key + ' - ' + course_obj_org.name)
  } else {
    console.log('not here')
  }
}