import * as ddegs from '../../data/json/raw/double_degrees.json';
import { is_object } from '../programs/pstruct_helpers';

const traverse_ddeg_struct = (): void => {
  for (let [code, val] of Object.entries(ddegs)) {
    if (code === 'default') continue;
    const ddeg_struct: any = val.structure;
    console.log(code)
    const lv1_keys: string[] = Object.keys(ddeg_struct);
    lv1_keys.forEach(lv1_key => {
      if (is_object(ddeg_struct[lv1_key])){
        console.log('\t' + lv1_key) 
        traverse_lv2_obj(ddeg_struct[lv1_key]);
      }
    })
    console.log('\n')
  }
}

const traverse_lv2_obj = (lv1_obj: any): void => {
  const lv2_keys: string[] = Object.keys(lv1_obj);
  lv2_keys.forEach(lv2_key => {
    if (is_object(lv1_obj[lv2_key])){
      console.log('\t\t' + lv2_key) 
      traverse_lv3_obj(lv1_obj[lv2_key]);
    }
  })
}

const traverse_lv3_obj = (lv2_obj: any): void => {
  console.log(lv2_obj)
  const lv3_keys: string[] = Object.keys(lv2_obj);
  lv3_keys.forEach(lv3_key => {
    if (is_object(lv2_obj[lv3_key])){
      console.log('\t\t\t' + lv3_key) 
      traverse_lv4_obj(lv2_obj[lv3_key]);
    }
  })
}

const traverse_lv4_obj = (lv3_obj: any): void => {
  const lv4_keys: string[] = Object.keys(lv3_obj);
  lv4_keys.forEach(lv4_key => {
    if (is_object(lv3_obj[lv4_key])){
      console.log('\t\t\t\t' + lv4_key) 
      //traverse_lv2_obj(lv3_obj[lv4_key]);
    }
  })
}



traverse_ddeg_struct();