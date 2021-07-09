import json
from pathlib import Path
from load_parse_save_prog import process_prog
import random
import os

def prog_scraper():
  prog_file = Path.cwd() / '..' / 'data' / 'json' / 'all_programs.json'
  all_progs_dict = load_prog_dict(prog_file)
  fac_file = Path.cwd() / '..' / 'data' / 'json' / 'faculties.json'
  facf = open(fac_file, 'r')
  fac_data = json.load(facf)
  facf.close()
  start = False
  for (fac_code, val) in fac_data.items():
    print(fac_code)
    prog_list = val.get('Programs')
    if prog_list:
      for prog in prog_list:
        if (prog == "3635" or start is True):
          if start is False:
            print('resuming here...')
          start = True
          prog_json = process_prog(fac_code, prog)
          if (prog_json == "SHTF"):
            print('exiting early')
            start = False
            break
          all_progs_dict.update(prog_json)
        print('\n' + prog + '\n')

  dump_prog_dict(prog_file, all_progs_dict)
  return

def load_prog_dict(prog_file):
  if not os.path.exists(prog_file):
    pf = open(prog_file, 'w')
    pf.write("{}")
    pf.close()
  pf = open(prog_file, 'r')
  all_progs_dict = json.load(pf)
  pf.close()
  return all_progs_dict

def dump_prog_dict(prog_file, all_progs_dict):
  open(prog_file, 'w').close()
  pf = open(prog_file, 'w')
  json.dump(all_progs_dict, pf)
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
  prog_scraper()
  #get_all_double_degs()