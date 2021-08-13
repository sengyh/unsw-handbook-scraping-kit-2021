import * as courses from "../../data/json/raw/courses.json";
import process_prereq from "./process_prereqs";
import type {Courses, Course, ProcessedCourses, ProcessedCourse} from "../custom_types";
import type {Prereq} from "./process_prereqs";
import * as _ from "lodash";
import * as fs from "fs";

/*
  traverse courses
    uoc: remove 'Units of Credit', turn into num

*/
const process_course = (): void => {
  for (let [key, val] of Object.entries(courses)) {
    if (key === 'default') continue;
    const code: string = key;
    const attr: Course = val;
    const subject: string = extract_subject(code);
    const level: number = extract_level(code);
    const terms: string[] = process_offering_terms(attr['offering_terms'], attr['academic_calendar']);
    const uoc: number = process_uoc(attr['uoc']);  
    const prereq_obj: Prereq = process_prereq(attr['prereqs']);
  }
  return;
}

// 3+: summer - 0,1,2,3
// some 3+ courses have 'summer canberra' and i'm just not having it, treated as summer term
// semester: T0,T1,T2,T3
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



process_course();