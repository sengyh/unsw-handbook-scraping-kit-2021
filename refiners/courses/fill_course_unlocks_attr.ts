import * as processed_courses from '../../data/json/refined_courses.json';
import type {ProcessedCourses, ProcessedCourse} from "../custom_types";
import * as _ from 'lodash';
import * as fs from 'fs';

const fill_unlocks_attr = (): void => {
  let all_processed_courses: ProcessedCourses = {..._.cloneDeep(processed_courses)};
  for (let [key, val] of Object.entries(all_processed_courses)) {
    if (key === 'default') continue;
    const curr_course_code: string = key;
    const attr: ProcessedCourse = val;
    if ('all_found_courses' in attr.other_requirements) {
      const all_valid_prereq_courses: string[] | undefined = attr.other_requirements.all_found_courses;
      all_valid_prereq_courses?.forEach(course => {
        let prereq_unlocks_arr: string[] = all_processed_courses[course].unlocks;
        if (!prereq_unlocks_arr.includes(course) && !all_processed_courses[course].exclusion_courses.includes(curr_course_code)) {
          all_processed_courses[course].unlocks.push(curr_course_code);
        }
      })
    }
  }
  //console.log(all_processed_courses['FINS1613']);
  delete all_processed_courses['default'];
  fs.writeFileSync('../../data/json/filled_unlocks.json', JSON.stringify(all_processed_courses, null, 2));
  return;
}

fill_unlocks_attr();