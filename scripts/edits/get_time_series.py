import sys
import json
import matplotlib.pyplot as plt
import numpy as np
import pickle

alphabet = 'abcdefghiklmnopqrstuvwxyz'
#alphabet = 'edited_projects'
total = 0
successful = 0
#fraction_obtained = []
last_day_dict = {}
for letter in alphabet:
    print letter
    inputfilename = '../../data/transformed/'+letter+'.json'
#    inputfilename = '../../data/transformed/edited_projects.json'
    if len(sys.argv) > 1:
        inputfilename = sys.argv[1]
    inputfile = open(inputfilename,'r')
    for line in inputfile:
        total += 1
        jsonobj = json.loads(line)
        ds = jsonobj['daily_snapshots']
        last_day = max([int(a) for a in ds.keys()])
        if last_day in last_day_dict:
            last_day_dict[last_day] += 1
        else:
            last_day_dict[last_day] = 1
        
    print last_day_dict
#        fraction_obtained.append(float(ds[last_day]['current_pledged'])/float(ds[last_day]['target_funds']))
#    print 'Total:', total
#    print 'Successful:', successful

#print fraction_obtained
print last_day_dict
#print 'Total:', total
#print 'Successful:', successful
#pickle.dump(fraction_obtained,open('fraction_obtained_per_edited_project.pkl','w'))
#plt.hist(fraction_obtained,bins=np.arange(0,5,0.1).tolist())
#plt.show()
