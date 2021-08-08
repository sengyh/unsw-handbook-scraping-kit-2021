import * as faculties from "../../data/json/raw/faculties.json";
import * as courses from "../../data/json/courses.json";
import _ from "lodash";
import * as fs from "fs";
import type { Courses, Course, Faculties } from "../custom_types";

const add_schools_to_facs = (): void => {
  let fac_name_abbr: {[key: string]: string} = {};
  let facs_dc: Faculties = _.cloneDeep(faculties)
  // build object showing relationship of faculty codes and full names
  for (let [key, val] of Object.entries(facs_dc)) { 
    if (key === 'default') continue;
    let f_val = val;
    fac_name_abbr = {...fac_name_abbr, ...{[f_val['name']]: key}};
    facs_dc[key] = {...facs_dc[key], ...{'schools': []}};  
  }
  delete facs_dc['default'];
  //console.log(fac_name_abbr)
  
  // fill schools array in faculty by traversing all courses
  for (let [key, val] of Object.entries(courses)) {
    if (key === 'default') continue;
    const c_fac = val['faculty'];
    if (c_fac === "") continue;
    const c_sch = val['school'];
    const fac_code = fac_name_abbr[c_fac];
    let fac_school_arr: any = facs_dc[fac_code]['schools'];
    if (!fac_school_arr.includes(c_sch) && c_sch !== "") {
      fac_school_arr.push(c_sch);
      facs_dc[fac_code]['schools'] = fac_school_arr;
    }
  }
  //console.log(JSON.stringify(facs_dc,null,2))
  fs.writeFileSync('../data/json/faculties_test.json', JSON.stringify(facs_dc,null,2));
  return;
}


add_schools_to_facs();