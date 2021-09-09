import * as programs from '../../data/json/raw/programs.json';
import * as _ from 'lodash';
import { process_any_course_str } from '../specialisations/spec_element_helper';
import { process_structure } from './process_program_structure';
import { ProcessedPrograms, ProcessedProgram, ProcessedProgramStructure } from '../custom_types';
import * as fs from 'fs';

const process_programs = (): void => {
  let processed_programs: ProcessedPrograms = {};
  for (let [key, val] of Object.entries(programs)) {
    if (key === 'default') continue;
    const program_code: string = key;
    const program_attrs: any = val;
    const processed_program: ProcessedProgram = construct_refined_program(program_code, program_attrs);
    processed_programs = {...processed_programs, ...{[program_code]: processed_program}}
  }
  //console.log(JSON.stringify(processed_programs, null, 2));
  fs.writeFileSync('../../data/json/refined_programs.json', JSON.stringify(processed_programs, null, 2));
  return;
}

const construct_refined_program = (program_code: string, program_attrs: any): ProcessedProgram => {
  const program_structure: any = program_attrs.structure;
  const processed_program_structure: ProcessedProgramStructure = process_structure(program_structure);
  const intake_period: string[] = process_intake_period(program_attrs.intake_period);
  const duration: number = process_duration(program_attrs['typical_duration:']);
  const award_type: string = process_award_type(program_attrs['award_type']);
  const refined_program: ProcessedProgram = {
    'code': program_code,
    'name': program_attrs.name,
    'uoc': program_attrs.uoc,
    'overview': program_attrs.overview,
    'double_degrees': program_attrs.double_degrees,
    'program_duration': duration,
    ...processed_program_structure,
    'faculty': program_attrs.faculty,
    'campus': program_attrs.campus,
    'intake_period': intake_period,
    'academic_calendar': program_attrs['academic_calendar'],
    'award': program_attrs['award(s)'],
    'award_type': award_type
  }
  return refined_program;
}

const process_intake_period = (term_str: string): string[] => {
  let refined_terms: string[] = [];
  if (term_str === "" || term_str === undefined) return refined_terms;
  refined_terms = term_str.split(", ").map(elem => {
    elem = elem.replace("Term ", "T");
    elem = elem.replace("Semester ", "S");
    return elem;
  }).sort();
  return refined_terms;
}

const process_duration = (typical_duration: string): number => {
  const td_arr: string[] = typical_duration.replaceAll(/[^0-9\-.]/gm, '').split('-')
  let duration: number = 0;
  if (td_arr.length === 2) {
    duration = Math.ceil(parseFloat(td_arr[1]));
  } else {
    duration = Math.ceil(parseFloat(td_arr[0]))
  }
  return duration;
}

const process_award_type = (awardt_str: string): string => {
  if (awardt_str === undefined) return "";
  return awardt_str;
}

process_programs();