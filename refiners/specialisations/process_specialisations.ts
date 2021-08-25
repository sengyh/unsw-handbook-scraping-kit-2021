import * as specialisations from '../../data/json/raw/specialisations.json';
import type { Specialisations, Specialisation, SpecStructure, SpecStructBody } from '../custom_types';
import { process_spec_structure } from './process_spec_structure';
import * as _ from 'lodash';
import * as fs from 'fs';

// run this file after homogenising specs
const process_specialisations = (): void => {
  //let raw_specs: Specialisations = _.cloneDeep(specialisations);
  for (let [key, val] of Object.entries(specialisations)){
    if (key === 'default') continue;
    const spec_code: string = key;
    const spec_attrs: Specialisation = val;
    const uoc: number = process_uoc(spec_attrs);
    //console.log(val.available_in_programs);
    process_spec_structure(spec_attrs.structure);
  }
  return;
}

const construct_refined_spec = (): void => {
  // school and mininum uoc could not exist, make them null (?)
}

// the only specialisation that does not have a min uoc also has 0 uoc 
const process_uoc = (attr: Specialisation): number => {
  const uoc: string = attr.uoc;
  const min_uoc: string = attr.minimum_units_of_credit;
  if (uoc !== min_uoc && uoc === "0") return 0;
  return parseInt(uoc);
}

process_specialisations();