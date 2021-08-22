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
      if (struct_section_body.description.match(/[a-z]{4}[0-9]{4}/gmi) && struct_section_body.courses.length === 0) {
        console.log(spec_code + ': ' + struct_section_title);
        console.log('uoc: ' + struct_section_body.uoc)
        console.log(struct_section_body.description.replaceAll(/\n{2,}/gm, '\n'));
        console.log(struct_section_body.courses)
        console.log('\n')
      }
      //console.log(struct_section_body.description.replaceAll(/\n/gm, '  ###  '));
    }
  }
  return;
}

explore_specs();