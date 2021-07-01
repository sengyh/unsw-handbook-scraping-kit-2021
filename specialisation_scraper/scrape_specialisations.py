import json
from pathlib import Path
from get_spec_json import process_spec

def spec_scraper():
  all_specs = get_all_specs()
  print(all_specs)
  for spec in all_specs:
    process_spec(spec)
    print(spec)

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
  return all_specs

if __name__ == '__main__':
  spec_scraper()