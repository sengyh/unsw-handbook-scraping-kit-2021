import * as courses from "../../data/json/raw/courses.json";
import process_prereq from "./process_prereqs";
import type {Courses, Course, ProcessedCourses, ProcessedCourse} from "../custom_types";
import type {Prereq} from "./process_prereqs";
import * as _ from "lodash";
import * as fs from "fs";

const process_all_courses = (): void => {
  let all_processed_courses: ProcessedCourses = {};
  for (let [key, val] of Object.entries(courses)) {
    if (key === 'default') continue;
    const code: string = key;
    const attr: Course = val;
    const processed_course: ProcessedCourse = construct_processed_course(code, attr);
    all_processed_courses = {...all_processed_courses, ...{[code]: processed_course}}
  }
  const all_pcourses_json: string = JSON.stringify(all_processed_courses, null, 2);
  fs.writeFileSync('../../data/json/test_refined_courses.json', all_pcourses_json);
  return;
}

const construct_processed_course = (code: string, attr: Course): ProcessedCourse => {
  const prereq_obj: Prereq = process_prereq(attr['prereqs'], code, attr['exclusion_courses'], attr['equivalent_courses']);
  const pc_obj: ProcessedCourse = {
    'name': attr.name,
    'uoc': process_uoc(attr['uoc']),
    'overview': attr.overview,
    'subject': extract_subject(code),
    'level': extract_level(code),
    'school': attr.school,
    'terms_available': process_offering_terms(attr['offering_terms'], attr['academic_calendar']),
    ...prereq_obj,
    'is_gen_ed': attr.is_gen_ed,
    'is_intro': attr.is_intro,
    'is_multi_term': attr.is_multi_term
  }
  return pc_obj;
}

// some 3+ courses have 'summer canberra' and i'm just not having it, treated as summer term
// 3+: T0,T1,T2,T3
// semester: S1, S2, SC
const process_offering_terms = (term_str: string, cal: string): string[] => {
  let refined_terms: string[] = [];
  if (term_str === "") return refined_terms;
  refined_terms = term_str.split(", ").map(elem => {
    elem = elem.replace("Term ", "T");
    elem = elem.replace("Summer Term", "T0");
    if (elem === "Summer Canberra" && cal === '3+') elem = elem.replace("Summer Canberra", "T0");
    elem = elem.replace("Summer Canberra", "S0");
    elem = elem.replace("Semester ", "S");
    return elem;
  }).sort()
  return refined_terms;
}

const process_uoc = (uoc: string): number => parseInt(uoc.replace('/\D/g', ''));

const extract_subject = (course_code: string): string => course_code.replace(/\d/g, '');

const extract_level = (course_code: string): number => parseInt(course_code.split('')[4]);


process_all_courses();