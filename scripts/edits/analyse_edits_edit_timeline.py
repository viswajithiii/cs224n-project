import difflib
import json
import getopt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher
import pickle

DIFF_THRESHOLD = 0
# When do the edit?

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def get_pledged_amount(project_data, day_number):
    return float(project_data["daily_snapshots"]["%d" % (day_number)]["current_pledged"])

# Standard sentence tokenizer.
def sent_tokenize(text, language='english'):
    """
    Return a sentence-tokenized copy of *text*,
    using NLTK's recommended sentence tokenizer
    (currently :class:`.PunktSentenceTokenizer`
    for the specified language).

    :param text: text to split into sentences
    :param language: the model name in the Punkt corpus
    """
    #tokenizer = load('tokenizers/punkt/{0}.pickle'.format(language))
    #return tokenizer.tokenize(text)

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

    edit_points = []
    with open(filePath, 'r') as project_file:
        # for each project
        i = 0
        for line in project_file:
            print i
            i += 1
            project_data = json.loads(line)
            #print project_data["project_name"]

            lines_changed = 0
            edit_count = 0

            previous_snapshot = None
            days_list = sorted(project_data["daily_snapshots"], key=lambda x: int(x))
            for day_number in days_list:
                #print day_number
                current_snapshot = project_data["daily_snapshots"][day_number]
                if (previous_snapshot != None):
                    #find the diff
                    if previous_snapshot["full_description"] != current_snapshot["full_description"]:
                        edit_count += 1
                        edit_points.append(float(day_number) / float(days_list[-1]))
                        #lines_changed += calculate_lines_changed(previous_snapshot["full_description"], current_snapshot["full_description"])

                previous_snapshot = current_snapshot
            #print edit_count
#                ds = project_data['daily_snapshots']
#                last_day = unicode(max([int(a) for a in ds.keys()]))
#                fraction_obtained.append(float(ds[last_day]['current_pledged'])/float(ds[last_day]['target_funds']))
    avg_edit_point = sum(edit_points) / len(edit_points)
    print avg_edit_point
    plt.hist(edit_points)
    plt.show()

main()
