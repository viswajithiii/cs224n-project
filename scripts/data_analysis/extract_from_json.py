import sys
import json
import matplotlib.pyplot as plt
import numpy as np
import pickle

alphabet = 'abcdefghiklmnopqrstuvwxyz'
alphabet = 'edited_projects'
total = 0
successful = 0
fraction_obtained = []
for letter in alphabet:
    print letter
    inputfilename = '../../data/transformed/edited_projects.json'
    if len(sys.argv) > 1:
        inputfilename = sys.argv[1]
    inputfile = open(inputfilename,'r')
    for line in inputfile:
        total += 1
        print total
        jsonobj = json.loads(line)
        ds = jsonobj['daily_snapshots']
        last_day = unicode(max([int(a) for a in ds.keys()]))
        if ds[last_day]['state'] == 'successful':
            successful += 1
        fraction_obtained.append(float(ds[last_day]['current_pledged'])/float(ds[last_day]['target_funds']))
    print 'Total:', total
    print 'Successful:', successful
    break

print fraction_obtained

print 'Total:', total
print 'Successful:', successful
pickle.dump(fraction_obtained,open('fraction_obtained_per_edited_project.pkl','w'))
#plt.hist(fraction_obtained,bins=np.arange(0,5,0.1).tolist())
#plt.show()
