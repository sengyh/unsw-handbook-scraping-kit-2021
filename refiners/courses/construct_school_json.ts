import * as courses from "../../data/json/courses.json";
import type { Course, School, Schools } from "../custom_types";
import * as fs from "fs";

const construct_school_json = (): void => {
  let all_schools: Schools = {};
  for (let [key, val] of Object.entries(courses)) {
    if (key === 'default') continue;
    const course: Course = val;
    const curr_sub_code = key.replace(/[0-9]/g, '');
    const curr_school_name = course['school'];
    if (Object.keys(all_schools).includes(curr_school_name)) {
      let subjects: string[] = all_schools[curr_school_name]['subjects'];
      if (!subjects.includes(curr_sub_code)) {
        subjects.push(curr_sub_code);
        subjects.sort();
      }
    } else {
      if (curr_school_name === "") continue;
      all_schools = {...all_schools, ...{[curr_school_name]: {'subjects': [curr_sub_code]}}};
    }
  }
  // would be nice if you figured out how to sort by keys...
  //console.log(JSON.stringify(all_schools, null, 2));
  fs.writeFileSync('../../data/json/schools.json', JSON.stringify(all_schools, null, 2));
  return;
}

construct_school_json();