import * as programs from '../../data/json/raw/programs.json';

const program_print_helpers = (): void => {
  for (let [key, val] of Object.entries(programs)) {
    if (key === 'default') continue;
    const prog_code: string = key;
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