import os
import re
import subprocess

# insanely hacky and borderline insane 'build my own json' tool
# goes through subject file line by line and finds 
# all couses which match subject code
print("{")
print('\t"all_subjects": [')
with open('data/all_subjects', 'r') as subject_file:
  for line in subject_file:
    #print(line)
    line_list = line.rstrip().split(": ")
    subject_code = line_list[0]
    print('\t\t{')
    print('\t\t\t"code": "' + subject_code + '",')
    subject_name = line_list[1]
    print('\t\t\t"name": "' + subject_name + '",')
    print('\t\t\t"courses": [')
    course_file = open('data/all_course_codes', 'r') 
    for cline in course_file:
      if re.findall(line_list[0], cline):
        print('\t\t\t\t"' + cline.rstrip() + '",')
    print('\t\t\t]')
    print('\t\t},')
  print('\t]')
  print('}')

