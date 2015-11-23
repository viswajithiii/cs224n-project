import difflib
import json
import getopt
import sys
import re
import matplotlib.pyplot as plt

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
	letters = "abcdefghijklmnopqrstuvwxyz"
	#letters = "q"
	edit_count_list = []
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

	plt.hist(edit_count_list)
	plt.yscale('log', nonposy='clip')
	plt.show()

main()





