import difflib
import json
import getopt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher
import pickle
from utils import *

DIFF_THRESHOLD = 0



def get_pledged_amount(project_data, day_number):
    return float(project_data["daily_snapshots"]["%d" % (day_number)]["current_pledged"])

def generate_data_vec(previous_snapshot, current_snapshot):
    features = []

    concreteness_feature = get_concreteness_score(current_snapshot["full_description"]) - get_concreteness_score(previous_snapshot["full_description"])
    features.append(concreteness_feature)

    desc_len_feature = float(len(current_snapshot["full_description"]))/ float(len(previous_snapshot["full_description"]))
    features.append(desc_len_feature)

    sentiment_feature = get_sentiment_score(current_snapshot["full_description"]) - get_sentiment_score(previous_snapshot["full_description"]) 
    features.append(sentiment_feature)
    liwc_features_curr = get_liwc_features(current_snapshot["full_description"])
    liwc_features_pre= get_liwc_features(previous_snapshot["full_description"])
#    print liwc_features_curr
#    print liwc_features_pre
    liwc_features_diff = [0]*len(liwc_features_curr)
    liwc_features_diff[0] = liwc_features_curr[0] - liwc_features_pre[0]
    features.extend(liwc_features_diff)
#    print features
#    print features
    return features

def calculate_gain(project_data, current_day, days_list):
    try:
        past_pledged_per_day = (get_pledged_amount(project_data, current_day - 1) - get_pledged_amount(project_data, 0)) / (current_day - 1)
        future_pledged_per_day = (get_pledged_amount(project_data, int(days_list[-1])) - get_pledged_amount(project_data, current_day + 1)) / (int(days_list[-1]) - current_day - 1)
    except KeyError:
        return -1
    except ZeroDivisionError:
        return -1
    if past_pledged_per_day == 0:
        return -1
    return future_pledged_per_day / past_pledged_per_day

xfile = open('X.txt', 'w')
yfile = open('y.txt', 'w')

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


    with open(filePath, 'r') as project_file:
        # for each project
        i = 0
        lines = project_file.readlines()
        for line in lines:
            print i
            i += 1
            project_data = json.loads(line)
            #print project_data["project_name"]

            lines_changed = 0
            edit_count = 0

            previous_snapshot = None
            days_list = sorted(project_data["daily_snapshots"], key=lambda x: int(x))
            gain_threshold = 0
            
            features = []
            for day_number in days_list:
                #print day_number
                current_day = int(day_number)
                current_snapshot = project_data["daily_snapshots"][day_number]
                if (previous_snapshot != None):
                    #find the diff
                    if previous_snapshot["full_description"] != current_snapshot["full_description"]:
                        #print "found edit"
                        edit_count += 1
                        data_vec = generate_data_vec(previous_snapshot, current_snapshot)
                        features.append(data_vec)
                        gain = calculate_gain(project_data, current_day, days_list)
                        if (gain != -1):
                            #print "data point"
                            if gain > 1 + gain_threshold:
                                label = 1
                            elif gain < 1 - gain_threshold:
                                label = 0
                            else:
                                continue
                            comma = False
                            for value in data_vec:
                                if comma:
                                    xfile.write(",%f" % (value))
                                else:
                                    comma = True
                                    xfile.write("%f" % (value))
                            xfile.write("\n")
                            yfile.write("%d\n" % (label))

                previous_snapshot = current_snapshot

main()
