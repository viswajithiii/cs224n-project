import difflib
import json
import getopt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np

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
    if filePath[-1] != '/':
        filePath.append('/')

    outfile = open('edited_projects.json','w')
    letters = "abcdefghijklmnopqrstuvwxyz"
    #letters = "q"
    edit_count_list = []
    fraction_obtained = []
    for letter in letters:
        file_loc = "%s%s.json" % (filePath, letter)
        # for each project file
        print letter
        with open(file_loc, 'r') as project_file:
            # for each project
            for line in project_file:
                project_data = json.loads(line)
                #print project_data["project_name"]

                lines_changed = 0
                edit_count = 0

                previous_snapshot = None
                for day_number in sorted(project_data["daily_snapshots"], key=lambda x: int(x)):
                    #print day_number
                    current_snapshot = project_data["daily_snapshots"][day_number]
                    if (previous_snapshot != None):
                        #find the diff
                        if previous_snapshot["full_description"] != current_snapshot["full_description"]:
                            edit_count += 1
                            #lines_changed += calculate_lines_changed(previous_snapshot["full_description"], current_snapshot["full_description"])

                    previous_snapshot = current_snapshot
                edit_count = float(edit_count) / (len(project_data["daily_snapshots"])-1)
                #print edit_count
                edit_count_list.append(edit_count)
                if edit_count > 0:
                    outfile.write(line)
#                ds = project_data['daily_snapshots']
#                last_day = unicode(max([int(a) for a in ds.keys()]))
#                fraction_obtained.append(float(ds[last_day]['current_pledged'])/float(ds[last_day]['target_funds']))
     

#   plt.hist(edit_count_list)
#   plt.yscale('log', nonposy='clip')
#    print np.corrcoef(fraction_obtained,edit_count_list)
#    no_o_frac = []
#    no_o_e = []
#    for (i,edit_count) in enumerate(edit_count_list):
#        if fraction_obtained[i] < 2:
#            no_o_frac.append(fraction_obtained[i])
#            no_o_e.append(edit_count)
#    plt.scatter(no_o_frac,no_o_e)
#    plt.show()

main()
