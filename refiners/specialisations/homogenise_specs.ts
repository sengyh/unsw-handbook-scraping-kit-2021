import * as specialisations from '../../data/json/raw/specialisations.json';
import type {ScrapedSpecialisations, ScrapedSpecialisation, SpecStructure, SpecStructBody} from '../custom_types';
import * as _ from 'lodash';
import * as fs from 'fs';

const homogenise_specialisations = (): void => {
  let raw_specs: ScrapedSpecialisations = _.cloneDeep(specialisations);
  for (let [key, val] of Object.entries(raw_specs)){
    if (key === 'default') continue;
    const spec_code: string = key;
    const spec_attrs: ScrapedSpecialisation = val;
    if (!('school' in spec_attrs)) {
      spec_attrs.school = "";
    }
    if (!('minimum_units_of_credit' in spec_attrs)) {
      spec_attrs.minimum_units_of_credit = "";
    }
  }
  delete raw_specs['default'];
  fs.writeFileSync('../../data/json/raw/specialisations2.json', JSON.stringify(raw_specs, null, 2))
  return;
}

homogenise_specialisations();