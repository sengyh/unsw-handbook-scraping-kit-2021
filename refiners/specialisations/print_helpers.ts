import * as specialisations from '../../data/json/raw/specialisations.json';

const explore_specs = (): void => {

  for (const [key, val]  of Object.entries(specialisations)) {
    if (key === 'default') continue;
    const spec_code: string = key;
    const spec_structure: any = val.structure;
    for (const [key, val] of Object.entries(spec_structure)) {
      if (key === 'default') continue;
      console.log(key);
    }
  }

  return;
}



explore_specs();