import * as _ from "lodash";
import { start } from "repl";

export type Prereq = {
  unlocked_by: string[];
  other_requirements: {
    uoc?: number;
    wam?: number;
    programs?: number[];
    specialisation?: string;
    raw_prereq?: string;
  };
}

const process_prereq = (prereq_str: string): Prereq => {
  let prereq_obj: Prereq = {unlocked_by: [], other_requirements: {}}
  if (prereq_str === 'None' || prereq_str === '') {
    //console.log("n/a")
    return prereq_obj;
  }
  const [prreq_section, coreq_section, excl_section, equiv_section, misc_section]: string[] = split_raw_prereq_str(prereq_str)
  
  return prereq_obj;
}

// todo in the future: [(preq,71),(creq,-1),(excl,0),(equiv,-1)]
// array.sort\_by((_,idx): idx)
const split_raw_prereq_str = (raw_prereq_str: string): string[] => {
  console.log(raw_prereq_str);

  const prereq_regex: RegExp = /pre[- ]*(r-*eq)*[a-z/]*[:; ]+/gim;  // 1182 matches
  const coreq_regex: RegExp = /co[- ]*((re)*req)+[a-z]*[:; ]+/gim   // 88 matches 
  const excl_regex: RegExp = /excl[a-z]*[;: ]+/gim;   // 78 matches
  const equiv_regex: RegExp = /Equiv[a-z]*[:; ]+/gm;  // 14 matches
  const pstr_elem_patterns: RegExp[] = [prereq_regex, coreq_regex, excl_regex, equiv_regex];
  const preq_match: number = raw_prereq_str.search(prereq_regex);
  const creq_match: number = raw_prereq_str.search(coreq_regex);
  const excl_match: number = raw_prereq_str.search(excl_regex);
  const equiv_match: number = raw_prereq_str.search(equiv_regex);
  const pstr_elem_indexes: number[] = [preq_match, creq_match, excl_match, equiv_match];

  // pstr_elem_strings: [prereq, coreq, excl, equiv, misc]
  let pstr_elem_strings: string[] = new Array(5).fill("");
  const no_match: boolean = pstr_elem_indexes.every(elem => elem === pstr_elem_indexes[0]);
  if (no_match) {
    console.log(pstr_elem_indexes + ': equal -1s')
    pstr_elem_strings[0] = raw_prereq_str;
  } else {
    pstr_elem_strings = constuct_pstr_elem_strings(raw_prereq_str, pstr_elem_patterns, pstr_elem_indexes, pstr_elem_strings);
  }
  console.log(pstr_elem_strings);
  console.log('\n')
  return pstr_elem_strings;
}

const constuct_pstr_elem_strings = (raw_prereq_str: string, pstr_elem_patterns: RegExp[], pstr_elem_indexes: number[], pstr_elem_strings: string[]): string[] => {
  const no_negatives: number[] = pstr_elem_indexes.filter(num => num >= 0);
  const array_in_order: boolean = no_negatives.every((elem,i,arr) => !i || arr[i-1] <= elem);
  const arr = pstr_elem_indexes;
  console.log(arr + ': ' + array_in_order.toString());
  if (array_in_order) {
    let starts_from_beginning: boolean = false;    
    // find first non negative number, look for next non negative number
    for (let i = 0; i < arr.length; i++) {
      if (arr[i] === 0) starts_from_beginning = true;
      if (arr[i] >= 0) {
        for (let j = i+1; j < arr.length; j++) {
          // last index reached and still negative
          if (arr[j] < 0 && j + 1 == arr.length) {
            pstr_elem_strings[i] = raw_prereq_str.slice(arr[i]).replace(pstr_elem_patterns[i], '');
          }
          if (arr[j] >= 0) {
            pstr_elem_strings[i] = raw_prereq_str.slice(arr[i], arr[j]).replace(pstr_elem_patterns[i], '');
            i = j;
          }
        }
      }
      if (i == 3 && arr[i] >= 0) {
        pstr_elem_strings[i] = raw_prereq_str.slice(arr[i]).replace(pstr_elem_patterns[i], '');
      } 
    }
    // has extra stuff in the beginning, slic to misc_section
    if (!starts_from_beginning && array_in_order){
      for (let i = 0; i < arr.length; i++) {
        if (arr[i] >= 0) {
          pstr_elem_strings[4] = raw_prereq_str.slice(0, arr[i]);
          break;
        }
      }
    }
  } else {
    // reverse order (figure this shit out)
    // only 2 courses have this condition (for now...)
    const array_in_rorder: boolean = no_negatives.every((elem,i,arr) => !i || arr[i-1] >= elem);
    if (array_in_rorder) {
      let prev_index: number = raw_prereq_str.length - 1;
      for (let i = 0; i < arr.length; i++) {
        if (arr[i] >= 0) {
          pstr_elem_strings[i] = raw_prereq_str.slice(arr[i], prev_index).replace(pstr_elem_patterns[i], '');
          prev_index = arr[i];
        }
      }
    }
  }
  pstr_elem_strings = pstr_elem_strings.map(str => _.trim(str, ',.;: '))
  return pstr_elem_strings;
}


export default process_prereq;