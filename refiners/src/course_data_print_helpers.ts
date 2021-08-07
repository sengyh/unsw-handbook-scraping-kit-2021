import * as courses from "../../data/json/courses.json";
import * as f_courses from "../../data/json/courses_partfill.json";
import * as subjects from "../../data/json/subjects.json";
import * as faculties from "../../data/json/faculties.json";
import * as fs from "fs";
import * as _ from "lodash";
import { keys } from "lodash";

 const main = (): void => {
  add_schools_to_fac();
  //get_calendar_terms();
  //print_all_attrs();
   return;
 }

const add_schools_to_fac = (): void => {
  for (let [course_code, course_attributes] of Object.entries(courses)){
    //console.log(course_code)
    //console.log(course_attributes['name'])
    const sub_code: string = course_code.replace(/[0-9]/g, '');
    if ("school" in course_attributes){
      const school: string = course_attributes['school'];
      //console.log(course_attributes["faculty"] + ' -- ' + school + ' -- ' + sub_code)
      console.log(school + ' -- ' + course_attributes['faculty'])
    } else {
      //console.log(course_attributes["faculty"] + ' -- ' + ' -- ' + sub_code);
      console.log(' -- ' + course_attributes['faculty'])
    }
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
  for (let [course_code, course_attributes] of Object.entries(f_courses)){
    //console.log(Object.keys(course_attributes))
    let attr_keys: string[] = [];
    for (let attr_key in course_attributes) console.log(attr_key)
  }
  return;
}


main();
