import { is_double_nested, check_if_val_name_eq_key, is_object, is_specialisation_block, has_disciplinary_component } from "./pstruct_helpers";
import { construct_refined_spec_obj, construct_refined_program_structure, construct_refined_course_obj } from "./pstruct_constructors";
import type {ProcessedProgramStructure, ProcessedStructBody, SpecElem, OtherInfoElem} from '../custom_types';
import * as _ from 'lodash'

export const process_structure = (program_structure: any): void => {
  // initialise 
  let refined_prog_structure: ProcessedProgramStructure = construct_refined_program_structure();
  const disciplinary_component_exists: boolean = has_disciplinary_component(program_structure);
  const struct_keys: string[] = Object.keys(program_structure); 
  struct_keys.forEach(key => {
    const struct_obj = program_structure[key];
    const is_obj = is_object(struct_obj);
    if (is_obj) {
      if (is_double_nested(struct_obj)) {
        // extract 
        if (key === 'Disciplinary Component') {
          refined_prog_structure.core_structure_uoc = parseInt(struct_obj.uoc);
          refined_prog_structure.core_structure_desc = struct_obj.requirements;
          refined_prog_structure = process_disciplinary_component(struct_obj, refined_prog_structure);
        } else {
          // this whole bit is super fucking tricky, come back later
          if (disciplinary_component_exists) {
            
          } else {
            //console.log(key)
            //console.log(struct_obj)
            //console.log('')
          }     
        }
      } else {
        //console.log(key)
        //console.log(JSON.stringify(struct_obj, null, 2))
        //console.log('')
      }
    }
  })
  //console.log(JSON.stringify(refined_prog_structure, null, 2))
  console.log('\n')
}

const process_disciplinary_component = (struct_obj: any, refined_prog_structure: ProcessedProgramStructure): ProcessedProgramStructure => {
  const struct_keys_lv2: string[] = Object.keys(struct_obj);
  struct_keys_lv2.forEach(key => {
    const struct_obj_lv2: any = struct_obj[key];
    if (is_object(struct_obj_lv2)) {
      // now check if there are specialistion objects inside
      if (is_specialisation_block(struct_obj_lv2)) {
        //console.log(struct_obj_lv2.name)
        const spec_block_req: string = struct_obj_lv2.requirements.replaceAll(/\n{2,}/gm, '\n');
        const sbr_first_line: string = spec_block_req.split('\n')[0];
        //console.log(sbr_first_line + '\n')
        const refined_spec_block: SpecElem = construct_refined_spec_obj(key, struct_obj_lv2);
        // assigns spec block from disc component into either core or optional spec
        if (sbr_first_line.match(/may/gm)) {
          refined_prog_structure.optional_specialisations.push(refined_spec_block);
        } else {
          refined_prog_structure.core_specialisations.push(refined_spec_block);
        }
      } else {
        // process course blocks
        // ignore if course groups, can of worms i do not wanna touch 
        construct_refined_course_obj(key, struct_obj_lv2);
      }
    }
  })
  //console.log(JSON.stringify(refined_prog_structure, null, 2));
  return refined_prog_structure;
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
        // no further nesting detected
        //console.log('\t\t' + lv2_key)
      } else {
        if (Array.isArray(psobj_lv2_elem)) {
          console.log('\t\t\t' + lv2_key)
        } else {
          console.log('\t\t' + lv2_key) // + ': ' + psobj_lv2_elem.replaceAll(/\n/gm, '\t'))
        }
      }
    });
  } else {
    if (Array.isArray(pstruct_obj_lv2)) {
      console.log('\t\t\t' + so_key)
    } else {
      console.log('\t\t' + so_key) // + ': ' + pstruct_obj_lv2.replaceAll(/\n/gm, '\t'))
    }
  } 
}