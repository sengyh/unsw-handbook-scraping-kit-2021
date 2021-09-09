// mainly used to filter out nested pstruct objects: 
// still need to check whether the key is disciplinary component -- no fuckin clue what to do...
export const is_double_nested = (ps_obj: any): boolean => {
  const pskeys_lv2: string[] = Object.keys(ps_obj);
  for (let pskey_lv2 of pskeys_lv2) {
    const ps_obj_lv2: any = ps_obj[pskey_lv2];
    const is_obj: boolean = is_object(ps_obj_lv2);
    if (is_obj) {
      return true;
    }
  }   
  return false;
}

export const has_disciplinary_component = (program_structure: any): boolean => {
  if ('Disciplinary Component' in program_structure) return true;
  return false;
}

// for the weird ass data structure that my dumb brain thought out (was feeling pretty smug when i was writing the scraper)
export const check_if_val_name_eq_key = (ps_obj_key: string, ps_obj_lv2: any): boolean => {
  if (ps_obj_lv2.name === ps_obj_key) return true;
  return false;
}

// simply checks if item is an object, not including arrays
export const is_object = (suspected_obj: any): boolean => {
  return typeof suspected_obj === 'object' && suspected_obj !== null && !Array.isArray(suspected_obj);
}


export const is_specialisation_block = (struct_block: any): boolean => {
  if ('courses' in struct_block || 'course_groups' in struct_block) return false;
  return true;
}

export const num_objects_in_obj = (struct_obj: any): number => {
  const keys: string[] = Object.keys(struct_obj);
  let num_objects: number = 0;
  keys.forEach(key => {
    if (is_object(struct_obj[key])) num_objects++;
  })
  return num_objects;
}

export const num_spec_obj_in_struct_obj = (struct_obj: any): number => {
  const lv2_keys: string[] = Object.keys(struct_obj);
  let num_spec_objs: number = 0;
  lv2_keys.forEach(lv2_key => {
    if (is_object(struct_obj[lv2_key])) {
      if (is_specialisation_block(struct_obj[lv2_key])) {
        num_spec_objs++;
      }
    }
  });
  return num_spec_objs;
}
