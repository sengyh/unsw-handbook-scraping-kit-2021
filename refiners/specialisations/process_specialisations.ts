import * as specialisations from '../../data/json/raw/specialisations.json';
import type { Specialisation, ProcessedSpecialisation, ProcStructObj, ProcessedSpecialisations } from '../custom_types';
import { process_spec_structure } from './process_spec_structure';
import * as _ from 'lodash';
import * as fs from 'fs';

// run this file after homogenising specs
const process_specialisations = (): void => {
  let processed_specialisations: ProcessedSpecialisations = {};
  for (let [key, val] of Object.entries(specialisations)){
    if (key === 'default') continue;
    const spec_code: string = key;
    const spec_attrs: Specialisation = val;
    const processed_spec: ProcessedSpecialisation = construct_refined_spec(spec_attrs);
    processed_specialisations = {...processed_specialisations, ...{[spec_code]: processed_spec}};
  }
  //console.log(JSON.stringify(processed_specialisations, null, 2));
  fs.writeFileSync('../../data/json/refined_specialisations.json', JSON.stringify(processed_specialisations, null, 2));
  return;
}

const construct_refined_spec = (attrs: Specialisation): ProcessedSpecialisation => {
  const processed_struct_obj: ProcStructObj = process_spec_structure(attrs.structure);
  const refined_specialisation: ProcessedSpecialisation = {
    name: attrs.name,
    overview: attrs.overview,
    specialisation_type: attrs.specialisation_type,  
    uoc: process_uoc(attrs),
    ...processed_struct_obj,
    available_in_programs: attrs.available_in_programs,
    school: attrs.school,
    faculty: attrs.faculty
  }
  return refined_specialisation;
}

// the only specialisation that does not have a min uoc also has 0 uoc 
const process_uoc = (attr: Specialisation): number => {
  const uoc: string = attr.uoc;
  const min_uoc: string = attr.minimum_units_of_credit;
  if (uoc !== min_uoc && uoc === "0") return 0;
  return parseInt(uoc);
}

process_specialisations();