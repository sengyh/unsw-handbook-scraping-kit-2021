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
    console.log("n/a")
    return prereq_obj;
  }
  const prereq_regex: RegExp = /pre[- ]*(r-*eq)*[a-z/]*[:; ]+/gim;  // 1182 matches
  const coreq_regex: RegExp = /co[- ]*((re)*req)+[a-z]*[:; ]+/gim   // 88 matches 
  const excl_regex: RegExp = /excl[a-z]*[;: ]+/gim;   // 78 matches
  const equiv_regex: RegExp = /Equiv[a-z]*[:; ]+/gm;  // 14 matches
  const preq_match: number = prereq_str.search(prereq_regex);
  const creq_match: number = prereq_str.search(coreq_regex);
  const excl_match: number = prereq_str.search(excl_regex);
  const equiv_match: number = prereq_str.search(equiv_regex);
  console.log(preq_match.toString() + ' | ' + creq_match.toString() + ' | ' + excl_match.toString() + ' | ' + equiv_match.toString())
  return prereq_obj;
}

export default process_prereq;