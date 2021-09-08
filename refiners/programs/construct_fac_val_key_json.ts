import * as faculties from "../../data/json/raw/faculties.json";
import * as courses from "../../data/json/raw/courses.json";
import _ from "lodash";
import * as fs from "fs";
import type { Courses, Course, Faculties } from "../custom_types";

const construct_fac_val_key_json = (): void => {
  let fac_name_abbr: {[key: string]: string} = {};
  let facs_dc: Faculties = _.cloneDeep(faculties);
  let fac_val_key = {}

  // build object showing relationship of faculty codes and full names
  for (let [fac_code, val] of Object.entries(facs_dc)) { 
    if (fac_code === 'default') continue;
    const fac_name = val.name;
    fac_name_abbr = {[fac_name]: fac_code};
    fac_val_key = {...fac_val_key, ...fac_name_abbr}
  }
  //console.log(JSON.stringify(fac_val_key, null, 2))
  fs.writeFileSync('../../data/json/name_to_code/fac_val_key.json', JSON.stringify(fac_val_key,null,2));
}

construct_fac_val_key_json();