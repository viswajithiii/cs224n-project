import difflib
import json
import getopt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher
import pickle

GAIN_THRESHOLD = 1

def get_pledged_amount(project_data, day_number):
    return float(project_data["daily_snapshots"]["%d" % (day_number)]["current_pledged"])

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:", ["filepath="])
    except getopt.GetoptError:
        print "Invalid or missing arguments"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--filepath"):
            filePath = arg

    if filePath=='':
        print "Provide path to all files"
        sys.exit(2)
#    if filePath[-1] != '/':
#        filePath.append('/')

    #gain_thresholds = [0.0, 0.2, 0.4, 0.6, 0.8, 1, 1.2]
    gain_thresholds = [1.2]
    for threshold in gain_thresholds:
        high_gain_edit = 0
        low_gain_edit = 0
        high_loss_edit = 0
        with open(filePath, 'r') as project_file:
            # for each project
            i = 0
            for line in project_file:
                #print i
                i += 1
                project_data = json.loads(line)
                #print project_data["project_name"]

                edit_count = 0

                previous_snapshot = None
                days_list = sorted(project_data["daily_snapshots"], key=lambda x: int(x))
                for day_number in days_list:
                    #print day_number
                    current_day = int(day_number)
                    current_snapshot = project_data["daily_snapshots"][day_number]
                    if (previous_snapshot != None):
                        #find the diff
                        if previous_snapshot["full_description"] != current_snapshot["full_description"]:
                            edit_count += 1
                            try:
                                past_pledged_per_day = (get_pledged_amount(project_data, current_day - 1) - get_pledged_amount(project_data, 0)) / (current_day - 1)
                                future_pledged_per_day = (get_pledged_amount(project_data, int(days_list[-1])) - get_pledged_amount(project_data, current_day + 1)) / (int(days_list[-1]) - current_day - 1)
                                overall_pledged_per_day = (get_pledged_amount(project_data, int(days_list[-1])) - get_pledged_amount(project_data, 0)) / (int(days_list[-1]))
                                if overall_pledged_per_day < 0:
                                    print get_pledged_amount(project_data,int(days_list[-1]))
                                    print get_pledged_amount(project_data,0)
                                    print days_list
                                    print days_list[-1]
                                    assert False
                                gain = (future_pledged_per_day - past_pledged_per_day) / overall_pledged_per_day
                                if gain > 10:
                                    print "\nHIGH GAIN FOUND!"
                                    print "Gain = %f, past_pledged_per_day = %f, future_pledged_per_day = %f, overall_pledged_per_day = %f" % (gain, past_pledged_per_day, future_pledged_per_day, overall_pledged_per_day)
                                    print "Previous:" 
                                    print previous_snapshot["full_description"]
                                    print "Current:"
                                    print current_snapshot["full_description"]
                                if gain > threshold:
                                    high_gain_edit += 1
                                elif gain < -threshold:
                                    high_loss_edit += 1
                                else:
                                    low_gain_edit += 1
                            except ZeroDivisionError:
                                pass
                            except KeyError:
                                pass
                    previous_snapshot = current_snapshot
        total_edits = high_gain_edit + high_loss_edit + low_gain_edit
        print "\nTHRESHOLD = %0.2f" % (threshold)
        print "high_gain_edit = %0.3f" % (float(high_gain_edit) / total_edits) 
        print "high_loss_edit = %0.3f" % (float(high_loss_edit) / total_edits) 
        print "low_gain_edit = %0.3f" % (float(low_gain_edit) / total_edits) 
main()
