import json
from pathlib import Path
from load_parse_save_ddeg import process_ddeg
import random
import os

def ddeg_scraper():
  ddeg_file = Path.cwd()  / '..' / '..' / 'data' / 'json' / 'all_double_degrees.json'
  all_ddegs_dict = load_ddeg_dict(ddeg_file)
  start = True
  all_ddegs = get_all_double_degs()
  for ddeg in all_ddegs:
    if (ddeg == "3955" or start is True):
      if start is False:
        print('resuming here...')
      start = True
      ddeg_json = process_ddeg(ddeg)
      if (ddeg_json == "SHTF"):
        print('exiting early')
        start = False
        break
      all_ddegs_dict.update(ddeg_json)
    print('\n' + ddeg + '\n')

  dump_ddeg_dict(ddeg_file, all_ddegs_dict)
  return

def load_ddeg_dict(ddeg_file):
  if not os.path.exists(ddeg_file):
    pf = open(ddeg_file, 'w')
    pf.write("{}")
    pf.close()
  pf = open(ddeg_file, 'r')
  all_ddegs_dict = json.load(pf)
  pf.close()
  return all_ddegs_dict

def dump_ddeg_dict(ddeg_file, all_ddegs_dict):
  open(ddeg_file, 'w').close()
  pf = open(ddeg_file, 'w')
  json.dump(all_ddegs_dict, pf)
  pf.close()
  print('fuck yesssssss')
  return

# returns list of all double degree codes (no duplicates)
def get_all_double_degs():
  fac_file = Path.cwd() / '..' / 'data' / 'json' / 'faculties.json'
  all_doubles = []
  double_count = 0
  with open(fac_file, 'r') as facf:
    fac_data = json.load(facf)
    for (fac_code, val) in fac_data.items():
      ddeg_list = val.get('Double Degrees')
      if ddeg_list:
        for ddeg in ddeg_list:  
          all_doubles.append(ddeg)
          double_count += 1
  unique_doubles = list(set(all_doubles))
  unique_doubles.sort()
  return unique_doubles


if __name__ == '__main__':
  ddeg_scraper()
  #get_all_double_degs()