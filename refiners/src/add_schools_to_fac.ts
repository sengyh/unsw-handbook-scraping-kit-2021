import * as faculties from "../../data/json/faculties.json";
import * as courses from "../../data/json/courses.json";
import _ from "lodash";
import * as fs from "fs";

type Courses = Record<string, Course>;
type ScrapedCourses = Record<string, ScrapedCourse>;
type ScrapedCourse = Partial<Course>;
type Course = {
  name: string;
  uoc: string;
  overview: string;
  prereqs: string;
  equivalent_courses: string[];
  exclusion_courses: string[];
  is_gen_ed: boolean;
  is_intro: boolean;
  is_multi_term: boolean;
  faculty: string;
  school: string;
  study_level: string;
  offering_terms: string;
  campus: string;
  academic_calendar: string;
  field_of_education: string;
};

type ProcessedCourse = {
  name: string;
  uoc: number;
  overview: string;
  school: string;
  terms_available: string[];
  equivalent_courses: string[];
  exclusion_courses: string[];
  
  // prereqs: courses (and or or), courses w wam reqs, degree wam reqs, programs

  unlocked_by: string[];
  unlocks: string[];
  is_intro: boolean;
  is_gen_ed: boolean;
  is_multi_term: boolean;
}

/*
  open fac file, deep copy
    add school attr
    fill non existent attrs (homogenise)
  create school json
    school -> subject
*/

const main = (): void => {
  const filled_courses: any = fill_courses();
  add_schools_to_facs(filled_courses);
  return;
}

const fill_courses = (): any => {
  let courses_dc: any = _.cloneDeep(courses);
  let filled_courses: any = {};
  for (let [key, val] of Object.entries(courses_dc)){
    let filled_course: any = fill_empty_course_attrs(key, val);
    filled_courses = {...filled_courses, ...filled_course};
  }
  delete filled_courses['default'];
  //fs.writeFileSync('../data/json/courses.json', JSON.stringify(filled_courses,null,2));
  return filled_courses;
}

const add_schools_to_facs = (filled_courses: any): void => {
  return;
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

main();