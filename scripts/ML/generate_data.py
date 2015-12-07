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
from difflib import SequenceMatcher


DIFF_THRESHOLD = 0



def get_pledged_amount(project_data, day_number):
    return float(project_data["daily_snapshots"]["%d" % (day_number)]["current_pledged"])

def generate_data_vec(previous_snapshot, current_snapshot):
    feature_names = []
    features = []

    concreteness_feature = get_concreteness_score(current_snapshot["full_description"]) - get_concreteness_score(previous_snapshot["full_description"])
    feature_names.append('Concreteness')
    features.append(concreteness_feature)

    desc_len_feature = float(len(current_snapshot["full_description"]))/ float(len(previous_snapshot["full_description"]))
    feature_names.append('Description Length Ratio')
    features.append(desc_len_feature)

    sentiment_feature = get_sentiment_score(current_snapshot["full_description"]) - get_sentiment_score(previous_snapshot["full_description"]) 
    feature_names.append('Sentiment')
    features.append(sentiment_feature)

    diff_dict = get_diff_dict(previous_snapshot["full_description"], current_snapshot["full_description"])
    liwc_features = get_liwc_features(diff_dict)
    feature_names.extend(liwc_features[0])
    features.extend(liwc_features[1])
#    print features
#    print features
    return (feature_names,features)

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

    #desc_diff_dict = {}
    desc_diff_dict = pickle.load(open('desc_diff_dict.pickle', 'r'))
    
    with open(filePath, 'r') as project_file:
        # for each project
        i = 0
        lines = project_file.readlines()
        header_written = False
        for line in lines:
            print i
            i += 1
            project_data = json.loads(line)
            project_name = project_data["project_name"]
            #desc_diff_dict[project_name] = {}
            lines_changed = 0
            edit_count = 0

            previous_snapshot = None
            days_list = sorted(project_data["daily_snapshots"], key=lambda x: int(x))
            gain_threshold = 0
            diff_threshold = 0
            features = []
            for day_number in days_list:
                #print day_number
                current_day = int(day_number)
                current_snapshot = project_data["daily_snapshots"][day_number]
                if (previous_snapshot != None):
                    #find the diff
                    if previous_snapshot["full_description"] != current_snapshot["full_description"]:
                        #print "found edit"
                        #difference = 1.0 - SequenceMatcher(None, previous_snapshot["full_description"], current_snapshot["full_description"]).ratio()
                        #desc_diff_dict[project_name][day_number] = difference
                        #previous_snapshot = current_snapshot
                        #continue
                        difference = float(desc_diff_dict[project_name][day_number])
                        if difference < diff_threshold:
                            previous_snapshot = current_snapshot
                            continue
                        edit_count += 1
                        gain = calculate_gain(project_data, current_day, days_list)
                        if (gain != -1):
                            #print "data point"
                            if gain > 1 + gain_threshold:
                                label = 1
                            elif gain < 1 - gain_threshold:
                                label = 0
                            else:
                                previous_snapshot = current_snapshot
                                continue
                            
                            data_vec = generate_data_vec(previous_snapshot, current_snapshot)
                            if not header_written:
                                header_written = True
                                feature_names = data_vec[0]
                                comma = False
                                for feature_name in feature_names:
                                    if comma:
                                        xfile.write(",%s" %(feature_name))
                                    else:
                                        comma = True
                                        xfile.write("%s" % (feature_name))
                                xfile.write("\n")
                            features.append(data_vec[1])
                            comma = False
                            for value in data_vec[1]:
                                if comma:
                                    xfile.write(",%f" % (value))
                                else:
                                    comma = True
                                    xfile.write("%f" % (value))
                            xfile.write("\n")
                            yfile.write("%d\n" % (label))


                previous_snapshot = current_snapshot
            #pickle.dump(desc_diff_dict, open('desc_diff_dict.pickle', 'w'))

main()
