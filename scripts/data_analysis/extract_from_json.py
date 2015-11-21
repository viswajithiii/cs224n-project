import sys
import json

inputfilename = '../../data/transformed/q.json'
if len(sys.argv) > 1:
    inputfilename = sys.argv[1]
inputfile = open(inputfilename,'r')
total = 0
for line in inputfile:
    jsonobj = json.loads(line)
    ds = jsonobj['daily_snapshots']
    last_day = unicode(max([int(a) for a in ds.keys()]))
    if ds[last_day]['state'] not in ['successful','failed']:
        print ds[last_day]['state']
#    for key in ds[last_day]:
    
