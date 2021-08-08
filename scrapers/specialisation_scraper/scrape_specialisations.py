import json
from pathlib import Path
from get_save_process_spec import process_spec
import random
import os

def spec_scraper():
  spec_file = Path.cwd() / '..' / '..' / 'data' / 'json' / 'all_specialisations.json'
  if not os.path.exists(spec_file):
    sf = open(spec_file, 'w')
    sf.write("{}")
    sf.close()
  sf = open(spec_file, 'r')
  all_specs_dict = json.load(sf)
  sf.close()

  fac_file = Path.cwd() / '..' / '..' / 'data' / 'json' / 'faculties.json'
  with open(fac_file, 'r') as facf:
    fac_data = json.load(facf)
    start = True
    for (fac_code, val) in fac_data.items():
      print(fac_code)
      spec_dict = val.get('Specialisations')
      if spec_dict:
        for (spec_type, spec_list) in spec_dict.items():
          print('\t' + spec_type)
          for spec in spec_list:
            if (spec == "ZPEMO1" or start is True):
              if start is False:
                print('resuming here...')
              start = True
              spec_json = process_spec(fac_code, spec)
              if (spec_json == "SHTF"):
                print('exiting early')
                start = False
                break
              all_specs_dict.update(spec_json)
            print('\t\t' + spec)
  facf.close()

  open(spec_file, 'w').close()
  sf = open(spec_file, 'w')
  json.dump(all_specs_dict, sf)
  sf.close()
  print('fuck yesssssss')
  print(len(get_all_specs()))
  return

  #sorted_list = sorted(jumbled_specs, key=lambda x: (x[-1], x[0]))
def get_all_specs():
  all_specs = []
  # access all specialities inside faculty json 
  # FAC_ADA, FAC_ENG, FAC_LAW, FAC_MED, FAC_SCI
  fac_file = Path.cwd() / '..' / '..' / 'data' / 'json' / 'faculties.json'
  with open(fac_file, 'r') as facf:
    fac_data = json.load(facf)
    #print(type(fac_data))
    for (fac_code, val) in fac_data.items():
      #if (fac_code == 'FAC_ENG'):
      #print(val.get('name'))
        spec_dict = val.get('Specialisations')
        if spec_dict:
          for (spec_type, spec_list) in spec_dict.items():
            for spec in spec_list:
              all_specs.append(spec)
              #if (spec == "COMPAH"):
              #  process_spec(fac_code, spec)
              #print(spec)
  return all_specs

if __name__ == '__main__':
  spec_scraper()