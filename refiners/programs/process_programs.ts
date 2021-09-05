import * as programs from '../../data/json/raw/programs.json';
import * as _ from 'lodash';
import { process_any_course_str } from '../specialisations/spec_element_helper';
import { process_structure } from './process_program_structure';

const process_programs = (): void => {
  for (let [key, val] of Object.entries(programs)) {
    if (key === 'default') continue;
    const program_code: string = key;
    const program_attrs: any = val;
    const program_structure: any = val.structure;
    console.log(program_code);
    process_structure(program_structure);
  }
  return;
}

const construct_refined_program = (): void => {
  
}

process_programs();