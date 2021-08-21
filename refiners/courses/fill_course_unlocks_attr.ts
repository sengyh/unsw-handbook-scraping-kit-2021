import * as processed_courses from '../../data/json/refined_courses.json';
import type {ProcessedCourses, ProcessedCourse} from "../custom_types";
import * as _ from 'lodash';


const fill_unlocks_attr = (): void => {
  let all_processed_courses: ProcessedCourses = {..._.cloneDeep(processed_courses)};
  for (let [key, val] of Object.entries(all_processed_courses)) {
    if (key === 'default') continue;
    const code: string = key;
    const attr: ProcessedCourse = val;
    if ('all_found_courses' in attr.other_requirements) {
      console.log(attr.other_requirements.all_found_courses);
    }
  }
  return;
}

fill_unlocks_attr();