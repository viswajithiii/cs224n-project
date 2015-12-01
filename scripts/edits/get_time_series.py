import sys
import json
import matplotlib.pyplot as plt
import numpy as np
import pickle
from collections import OrderedDict

alphabet = 'abcdefghiklmnopqrstuvwxyz'
#alphabet = 'edited_projects'
total = 0
successful = 0
#fraction_obtained = []
last_day_dict = {}
time_series_mat = []
for letter in alphabet:
    print letter
    inputfilename = '../../data/transformed/'+letter+'.json'
#    inputfilename = '../../data/transformed/edited_projects.json'
    if len(sys.argv) > 1:
        inputfilename = sys.argv[1]
    inputfile = open(inputfilename,'r')
    for line in inputfile:
        curr_time_series = [0]*30
        total += 1
        jsonobj = json.loads(line)
        ds = jsonobj['daily_snapshots']
        last_day = max([int(a) for a in ds.keys()])
        if last_day in last_day_dict:
            last_day_dict[last_day] += 1
        else:
            last_day_dict[last_day] = 1
        
        curr_dict = OrderedDict()
        for day_number in sorted(ds,key=lambda x: int(x)):
            effective_dn = (float(day_number)/last_day)*30
            curr_dict[effective_dn] = ds[day_number]
        for eff_day in range(1,30):
            if eff_day in curr_dict:
                curr_time_series[eff_day] = curr_dict[eff_day]
            else:
                prev = None
                for day in curr_dict:
                    if day > eff_day:
                        curr_time_series[eff_day] = (day-eff_day)
        time_series_mat.append(curr_time_series)
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
