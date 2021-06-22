import json

with open('data/subject_course.json') as f:
  data = json.load(f)

  #print(data['all_subjects']['code'])
  for subject in data['all_subjects']:
    if (subject.get('code') == 'MATH'):
      print(subject.get('courses'))