import sys
import json
import matplotlib.pyplot as plt

alphabet = 'abcdefghiklmnopqrstuvwxyz'
alphabet = 'abc'
total = 0
successful = 0
fraction_obtained = []
for letter in alphabet:
    print letter
    inputfilename = '../../data/transformed/'+ letter + '.json'
    if len(sys.argv) > 1:
        inputfilename = sys.argv[1]
    inputfile = open(inputfilename,'r')
    for line in inputfile:
        total += 1
        jsonobj = json.loads(line)
        ds = jsonobj['daily_snapshots']
        last_day = unicode(max([int(a) for a in ds.keys()]))
        if ds[last_day]['state'] == 'successful':
            successful += 1
        fraction_obtained.append(float(ds[last_day]['current_pledged'])/float(ds[last_day]['target_funds']))
    print 'Total:', total
    print 'Successful:', successful

print 'Total:', total
print 'Successful:', successful
print fraction_obtained
plt.hist(fraction_obtained,bins=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,2.0,3.0,4.0,5.0])
plt.show()
