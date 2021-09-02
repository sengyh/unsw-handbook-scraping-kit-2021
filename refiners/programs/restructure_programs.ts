import * as programs from '../../data/json/raw/programs.json';
import * as _ from 'lodash';
import { process_any_course_str } from '../specialisations/spec_element_helper';

const restructure_programs = (): void => {
  for (let [key, val] of Object.entries(programs)) {
    if (key === 'default') continue;
    const program_code: string = key;
    const program_attrs: any = val;
    const program_structure: any = val.structure;
    console.log(program_code);
    process_pstructure(program_structure);
  }
  return;
}

const process_pstructure = (program_structure: any): void => {
  const struct_keys: any[] = Object.keys(program_structure);
  struct_keys.forEach(key => {
    const struct_obj = program_structure[key];
    const is_obj = is_object(struct_obj);
    if (is_obj) {
      console.log(key);
      const struct_obj_keys: any[] = Object.keys(struct_obj);
      struct_obj_keys.forEach(so_key => {
        const struct_obj_lv2 = struct_obj[so_key];
        process_pstruct_obj(so_key, struct_obj_lv2);
      });
    }
  })
  console.log('\n')
}

// mainly inside disciplinary component object of structure
// good news, there are no objects inside 
const process_pstruct_obj = (so_key: string, pstruct_obj_lv2: any): void => {
  const is_obj = is_object(pstruct_obj_lv2);
  if (is_obj) {
    console.log('\t' + so_key)
    const psobj_lv2_keys: any[] = Object.keys(pstruct_obj_lv2);
    psobj_lv2_keys.forEach(lv2_key => {
      const psobj_lv2_elem = pstruct_obj_lv2[lv2_key];
      if (is_object(psobj_lv2_elem)) {
        //console.log('\t\t' + lv2_key)
      } else {
        if (Array.isArray(psobj_lv2_elem)) {
          console.log('\t\t\t' + lv2_key)
        } else {
          console.log('\t\t' + lv2_key)
        }
      }
    });
  } else {
    if (Array.isArray(pstruct_obj_lv2)) {
      console.log('\t\t\t' + so_key)
    } else {
      console.log('\t\t' + so_key)
    }
  }  
}

const is_object = (suspected_obj: any): boolean => {
  return typeof suspected_obj === 'object' && suspected_obj !== null && !Array.isArray(suspected_obj);
}

restructure_programs();