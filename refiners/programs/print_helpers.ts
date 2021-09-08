import * as programs from '../../data/json/raw/programs.json';
import type {} from '../custom_types';

const program_print_helpers = (): void => {
  for (let [prog_code, val] of Object.entries(programs)) {
    if (prog_code === 'default') continue;
    const structure: any = val.structure;
    const struct_keys: any[] = Object.keys(structure);
    console.log(prog_code + ': ' + val.name)
    struct_keys.forEach(skey => {
      if (skey !== 'overview') {
        const struct_obj_key = Object.keys(structure[skey])
        if (struct_obj_key.length === 3) {
          console.log(skey)
          console.log('\t' + struct_obj_key)
          //console.log(struct_obj_key)
        }
      }
    })
    console.log('')
  }
}



program_print_helpers();