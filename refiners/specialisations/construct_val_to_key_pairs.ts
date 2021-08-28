import * as subjects from '../../data/json/subjects.json';
import * as fs from 'fs';

const construct_subject_name_key_obj = (): void => {
  let sub_name_key_obj: Record<string, string> = {};
  for (let [key, val] of Object.entries(subjects)) {
    if (key === 'default') continue;
    const sub_code: string = key;
    const sub_attrs: {name: string, courses: string[]} = val;
    if (sub_attrs.name in sub_name_key_obj) {
      if (sub_attrs.courses.length > 0) sub_name_key_obj[sub_attrs.name] += ' | ' + sub_code;
    } else {
      sub_name_key_obj = {...sub_name_key_obj, ...{[sub_attrs.name]: sub_code}};
    }
  }
  fs.writeFileSync('../../data/json/name_to_code/subject_val_key.json', JSON.stringify(sub_name_key_obj, null, 2));
  return;
}

construct_subject_name_key_obj();