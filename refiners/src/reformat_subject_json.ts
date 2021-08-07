import * as subjects from "../../data/json/original/subjects.json";
import * as fs from "fs";

type SubjectType = {
  code: string;
  name: string;
  courses: string[];
};

const reformat_subject_json = (): void => {
  const all_subjects = subjects.all_subjects;
  let reformatted_subjects = {}
  all_subjects.forEach(subject => {
    let rsub_obj = construct_rsub_obj(subject);
    reformatted_subjects = { ...reformatted_subjects, ...rsub_obj };
  });
  fs.writeFileSync('../data/json/all_subjects.json', JSON.stringify(reformatted_subjects));
  return;
}

const construct_rsub_obj = (subject: SubjectType): any => {
  const {code, name, courses} = subject;
  const subject_obj: any = {[code]: {"name": name, "courses": courses}};
  return subject_obj;
}

reformat_subject_json();

export default reformat_subject_json;