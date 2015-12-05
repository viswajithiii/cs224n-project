import difflib
import json
import getopt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

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

    for threshold in np.arange(0.9,1,0.1).tolist():
        print 'Threshold:',threshold
        edit_count_list = []
        fraction_obtained = []
        diffval_list = []
        exceeds_threshold_count = 0
        successful_count = 0
        with open(filePath, 'r') as project_file:
            # for each project
            i = 0
            for line in project_file:
                i += 1
                if i %1000 == 0:
                    sys.stderr.write('%d\n' %(i))
    #            if i > 100:
    #                break
                project_data = json.loads(line)
                #print project_data["project_name"]

                lines_changed = 0
                edit_count = 0

                previous_snapshot = None
                exceeds_threshold = False
                ds = project_data['daily_snapshots']
                last_day = unicode(max([int(a) for a in ds.keys()]))
                successful = ds[last_day]['state'] == 'successful'

                if not successful:
                    continue

                for day_number in sorted(project_data["daily_snapshots"], key=lambda x: int(x)):
                    #print day_number
                    current_snapshot = project_data["daily_snapshots"][day_number]
                    if (previous_snapshot != None):
                        #find the diff
                        if previous_snapshot["full_description"] != current_snapshot["full_description"]:
                            edit_count += 1
                            difference = 1.0 - SequenceMatcher(None, previous_snapshot["full_description"], current_snapshot["full_description"]).ratio()
                            diffval_list.append(difference)
                            if difference > threshold and successful:
                                exceeds_threshold = True  
                                print 'EXCEEDED THRESHOLD: %s' %(project_data["project_name"])
                                print 'Day ', day_number, ' of ', last_day
                                print 'Raised:', current_snapshot["current_pledged"]
                                print 'Target:',current_snapshot["target_funds"]
                                print 'Previous:'
                                print repr(previous_snapshot["full_description"])
                                print 'Current:'
                                print repr(current_snapshot["full_description"])
                                break
                            #lines_changed += calculate_lines_changed(previous_snapshot["full_description"], current_snapshot["full_description"])

                    previous_snapshot = current_snapshot
    #            edit_count = float(edit_count) / (len(project_data["daily_snapshots"])-1)
                #print edit_count
    #            edit_count_list.append(edit_count)
                if exceeds_threshold:
                    exceeds_threshold_count += 1
                    ds = project_data['daily_snapshots']
                    last_day = unicode(max([int(a) for a in ds.keys()]))
                    fraction_obtained.append(float(ds[last_day]['current_pledged'])/float(ds[last_day]['target_funds']))
                    successful = ds[last_day]['state'] == 'successful'
                    if successful:
                        successful_count += 1
         

        print 'Exceeds Threshold:',exceeds_threshold_count
        print 'Successful:',successful_count
        print 'Fraction successful:', float(successful_count)/exceeds_threshold_count
    #    print fraction_obtained
    #    plt.hist(diffval_list)
    #    plt.show()

main()
