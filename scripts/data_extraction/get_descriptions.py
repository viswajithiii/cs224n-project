from bs4 import BeautifulSoup
import sys
import os
import getopt
import re
import json
from utils import *
reload(sys)
sys.setdefaultencoding('UTF8')

pattern = re.compile(r'[^0-9]')

filePath = ''
outfilename ='../../data/transformed/q.txt'

try:
	opts, args = getopt.getopt(sys.argv[1:], "f:o:", ["filepath=","outfile="])
except getopt.GetoptError:
	print "Invalid or missing arguments"
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-f", "--filepath"):
		filePath = arg
	if opt in ("-o", "--outfile"):
		outfilename = arg

if filePath=='':
	print "Provide path to all files"
	sys.exit(2)

print filePath
print outfilename
# List of [directory path, project name] lists
list_of_all_project_names = []
# Map from project name to highest day number reached
max_day_map = dict()

# Walk over all files to get all project names there are
for root, dirnames, filenames in os.walk(filePath):
	for filename in filenames:
		if "_day-0_" in filename:
			list_of_all_project_names.append([root, filename.split('_day-0_')[0]])

# Walk over all files to get max day for each project
for root, dirnames, filenames in os.walk(filePath):
	for filename in filenames:
		if '_day-' not in filename:
			continue
		project_name = filename.split('_day-')[0]
		day_number = int(filename.split('_day-')[1].split('_')[0])
		if project_name in max_day_map and max_day_map[project_name] < day_number or project_name not in max_day_map:
			max_day_map[project_name] = day_number
			
# Now, walk over all files to get whatever you want
projects_data = {} # We create a dictionary to be finally stored in json format for all the projects

#This is for purged projects, which just disappear from Kickstarter, and which break BeautifulSoup.
purged_projects = {}

for root, dirnames, filenames in os.walk(filePath):
	print len(filenames)
	i = 0
	for filename in filenames:
		i += 1
		print i, " of ", len(filenames)
#		if i < 50000:
#			continue
		if '_day-' not in filename:
			continue
		project_name = filename.split('_day-')[0]
		day_number = int(filename.split('_day-')[1].split('_')[0])
		print project_name, " ", day_number

		if project_name in purged_projects:
			continue
		# Add the project if we havent seen it before
		if project_name not in projects_data:
			projects_data[project_name] = {}
			projects_data[project_name]["project_name"] = project_name
			projects_data[project_name]["daily_snapshots"] = {}
		
		# PUT HERE WHATEVER CONDITION YOU WANT FOR THE DAY NUMBER
		#if day_number != max_day_map[project_name]: #if you want max day for that project
		#if day_numer != 0 #if you want the zeroeth day for that project
		#	continue
		
		f = open(root + '/' + filename, 'r')
		
		#Beautiful Soup object for the whole HTML page
		soup = BeautifulSoup(f, 'html.parser')
		
		#print project_name
		#print '\n\n\n\n\n\n'
		
		#Short blurb about the project
		blurb = get_blurb(soup)
		#Text under full_description
		full_description = get_full_description(soup)
		#Text under risks
		risks = get_risks(soup)
		#Reward currenty and reward amounts (in a list of [amount (integer), reward (text)] lists)
		try:
			reward_currency, reward_amounts = get_rewards(soup)
		except IndexError: #Comes up in some fringe cases where our project is taken down in an inconsistent way.
			purged_projects[project_name] = True
			continue
		

		#State is the project scale, is a string, can be 'live', 'canceled', 'failed', 'successful'
		#Ended is a boolean which states whether the project is ended. Is either True or False
		state,ended = get_project_status(soup)
		
		#Purged projects are useless, they just disappear
		if state == 'purged':
			purged_projects[project_name] = True
			continue

		try:
			current_funds, target_funds = get_current_target_amounts(soup)
		except TypeError: #This comes up in some fringe cases where our project is taken down for some dispute or whatever.
			purged_projects[project_name] = True
			continue
		num_backers = get_num_backers(soup)

		#print full_description
		#print '\n\n\n\n\n\n'

		faqs = get_project_faqs(soup)
		# Add all the required information in projects_data (add/remove if required)
		projects_data[project_name]["daily_snapshots"][day_number] = {
			"blurb":blurb,
			"full_description":full_description,
			"risks":risks,
			"reward_currency":reward_currency,
			"reward_amounts":reward_amounts,
			"current_pledged": current_funds,
			"target_funds": target_funds,
			"num_backers": num_backers,
			"state": state,
			"ended": ended,
			"faqs":faqs,
		}

print "Collected all the data. Dumping to file ..."
# Output the data collected. Each line is a json format for one project
outfile = open(outfilename, 'w')
for project_name in projects_data:
	if project_name in purged_projects:
		continue
	outfile.write("%s\n" % (json.dumps(projects_data[project_name])))
