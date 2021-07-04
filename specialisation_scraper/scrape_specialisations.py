import json
from pathlib import Path
from get_save_process_spec import process_spec
import random

def spec_scraper():
  all_specs = get_all_specs()
  #for spec in all_specs:
  #  if (spec == 'SOLAAH'):
  #    process_spec(spec)
  #    break
      #print(spec)
  random.shuffle(all_specs)
  # TODO: migrate to test file
  #jumbled_specs = all_specs
  #print(jumbled_specs)
  #sorted_list = sorted(jumbled_specs, key=lambda x: (x[-1], x[0]))
  #print(sorted_list)
  

  return

def get_all_specs():
  all_specs = []
  # access all specialities inside faculty json 
  # FAC_ADA, FAC_ENG, FAC_LAW, FAC_MED, FAC_SCI
  fac_file = Path.cwd() / '..' / 'data' / 'json' / 'all_faculties.json'
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
              if (spec == "JAPNG1"):
                process_spec(fac_code, spec)
              #print(spec)
  return all_specs

if __name__ == '__main__':
  spec_scraper()