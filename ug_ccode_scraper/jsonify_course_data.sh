#!/bin/bash

# moved all subject names to another file
egrep -v '^[A-Z]{4}: ' all_codes_2 > only_codes

# convert all course codes file to urls.
awk '{print "https://www.handbook.unsw.edu.au/undergraduate/courses/2021/" $0}' oc_2 > code_links