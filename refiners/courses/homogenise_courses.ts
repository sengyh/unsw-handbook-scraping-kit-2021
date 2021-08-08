import * as faculties from "../../data/json/raw/faculties.json";
import * as courses from "../../data/json/raw/courses.json";
import _ from "lodash";
import * as fs from "fs";
import type { Courses, Course, Faculties } from "../custom_types";

const fill_courses = (): Courses => {
  let courses_dc: any = _.cloneDeep(courses);
  let filled_courses: any = {};
  for (let [key, val] of Object.entries(courses_dc)){
    if (key === 'default') continue;
    let filled_course: Course = fill_empty_course_attrs(key, val);
    filled_courses = {...filled_courses, ...filled_course};
  }
  //fs.writeFileSync('../data/json/courses_test.json', JSON.stringify(filled_courses,null,2));
  return filled_courses;
}

// could expand upon this if 2022 hb is even more cooked
const fill_empty_course_attrs = (course_code: string, course_attrs: any): any => {
  let filled_course_attrs: any = _.cloneDeep(course_attrs);
  let nonexistent_attrs: string[] = ['campus', 'school', 'offering_terms'];
  nonexistent_attrs.forEach(n_attr => {
    if (!(n_attr in course_attrs)) {
      filled_course_attrs = {...filled_course_attrs, ...{[n_attr]: ""}};
    }
  })
  let filled_course: any = {[course_code]: filled_course_attrs};
  return filled_course;
}

fill_courses();