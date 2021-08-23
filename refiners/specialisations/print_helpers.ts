import * as specialisations from '../../data/json/raw/specialisations.json';
import type {ScrapedSpecialisation, SpecStructure, SpecStructBody} from '../custom_types';

const explore_specs = (): void => {
  for (const [key, val] of Object.entries(specialisations)) {
    if (key === 'default') continue;
    const spec_code: string = key;
    const spec: ScrapedSpecialisation = val;
    const spec_structure: SpecStructure = spec.structure;
    for (const [key, val] of Object.entries(spec_structure)) {
      if (key === 'default') continue;
      const struct_section_title: string = key;
      const struct_section_body: SpecStructBody = val; 
      //no_courses_in_struct_sect(spec_code, struct_section_title, struct_section_body);
      //no_uoc_in_struct_sect(spec_code, struct_section_title, struct_section_body);
      //dnc_have_courses(spec_code, struct_section_title, struct_section_body);
      //console.log(struct_section_body.description.replaceAll(/\n/gm, '\t\t'));
      console.log(struct_section_body.courses)
    }
  }
  return;
}

const no_courses_in_struct_sect = (spec_code: string, struct_section_title: string, struct_section_body: SpecStructBody): void => {
  if (struct_section_body.description.match(/[a-z]{4}[0-9]{4}/gmi) && struct_section_body.courses.length === 0) {
    console.log(spec_code + ': ' + struct_section_title);
    console.log('uoc: ' + struct_section_body.uoc)
    console.log(struct_section_body.description.replaceAll(/\n{2,}/gm, '\n'));
    console.log(struct_section_body.courses)
    console.log('\n')
  }
  return;
}

const no_uoc_in_struct_sect = (spec_code: string, struct_section_title: string, struct_section_body: SpecStructBody): void => {
  if (struct_section_body.uoc === "") {
    console.log(spec_code + ': ' + struct_section_title);
    console.log(struct_section_body.description.replaceAll(/\n{2,}/gm, '\n'));
    console.log(struct_section_body.courses)
    console.log('\n')
  }
  return;
}

const dnc_have_courses = (spec_code: string, struct_section_title: string, struct_section_body: SpecStructBody): void => {
  if (struct_section_body.courses.length > 0 && struct_section_body.description.match(/[a-z]{4}\d{4}/gmi)) {
    console.log(spec_code + ': ' + struct_section_title);
    console.log(struct_section_body.description.replaceAll(/\n{2,}/gm, '\n'));
    console.log(struct_section_body.courses)
    console.log('\n')
  }
  return;
}

// only case where this happens (ACCTA1: CAANZ/CPA Accreditation Requirements)
const title_only_in_struct_sect = (spec_code: string, struct_section_title: string, struct_section_body: SpecStructBody): void => {
  if (struct_section_body.uoc === "" && struct_section_body.description === "" && struct_section_body.courses.length === 0) {
    console.log(spec_code + ': ' + struct_section_title);
    console.log('\n')
  }
  return;
}

explore_specs();