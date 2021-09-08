import * as courses from "../../data/json/raw/courses.json";
import * as subjects from "../../data/json/subjects.json";
import * as faculties from "../../data/json/faculties.json";
import * as fs from "fs";
import * as _ from "lodash";
import { keys } from "lodash";

 const main = (): void => {
  //get_calendar_terms();
  //print_all_attrs();
  //list_all_subjects();
  print_all_sub_sch_fac();
  return;
 }

const list_all_subjects = (): void => {
  for (let[key, val] of Object.entries(subjects)){
    if (key === 'default') continue;
    console.log(key);
  }
  return;
}

const print_all_sub_sch_fac = (): void => {
  for (let [course_code, course_attributes] of Object.entries(courses)){
    if (course_code === 'default') continue;
    const sub_code: string = course_code.replace(/[0-9]/g, '');
    //console.log(sub_code + ' -- ' + course_attributes['school'] + ' -- ' + course_attributes['faculty']);
    //console.log(course_attributes['school'])
    //console.log(course_attributes['school'] + ' -- ' + course_attributes['faculty']);
    //console.log(sub_code + ' -- ' + course_attributes['school']);
    //console.log(course_attributes['offering_terms'])
    const terms = course_attributes['offering_terms'];
    const cal = course_attributes['academic_calendar'];
    //if (cal === 'Semester' && terms === "Term 2, Term 3") console.log(course_code)
    console.log(cal + ': ' + terms);

  }
  return;
}

const get_calendar_terms = (): void => {
  for (let [course_code, course_attributes] of Object.entries(courses)){
    if ("academic_calendar" in course_attributes){
      const cal: string = course_attributes['academic_calendar'];
      let terms = ""
      if ("offering_terms" in course_attributes){
        terms = course_attributes['offering_terms'];
        console.log(cal + ': ' + terms);
      } else {
        console.log(cal + ': ' + course_code)
      }
      
    } else {
      console.log("no calendar??? " + course_code);
    }
  }
  return;
}

const print_all_attrs = (): void => {
  for (let [course_code, course_attributes] of Object.entries(courses)){
    //console.log(Object.keys(course_attributes))
    let attr_keys: string[] = [];
    for (let attr_key in course_attributes) console.log(attr_key)
  }
  return;
}


main();
