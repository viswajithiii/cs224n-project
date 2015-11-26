import sys
import json

alphabet = 'abcdefghijklmnopqrtsuvwxyz'
for letter in alphabet:
    inputfilename = '../../data/transformed/'+letter+'.json'
    outfilename = '../../data/transformed/'+letter+'new.json'
    if len(sys.argv) > 1:
        inputfilename = sys.argv[1]
    inputfile = open(inputfilename,'r')
    outputfile = open(outfilename,'w')
    total = 0
    canceled = 0
    unfinished = 0
    both = 0
    suspended = 0
    live = 0
    for line in inputfile:
        jsonobj = json.loads(line)
        ds = jsonobj['daily_snapshots']
        last_day = unicode(max([int(a) for a in ds.keys()]))
        forbidden = ['full_description', 'faqs', 'reward_amounts','blurb', 'risks']
        for key in ds[last_day]:
            if not key in forbidden:
                pass
    #            print key, ': ', ds[last_day][key]
        flag_c = False
        flag_e = False
        flag_s = False
        flag_l = False
        if ds[last_day]['state'] == 'canceled':
            canceled += 1
            flag_c = True
        if ds[last_day]['state'] == 'suspended':
            suspended += 1
            flag_s = True
        if ds[last_day]['state'] == 'live':
            live += 1
            flag_l = True
        if not ds[last_day]['ended']:
            unfinished += 1
            flag_e = True
        if flag_c and flag_e:
            both += 1
        if not (flag_c or flag_e or flag_s or flag_l):
            outputfile.write(line)
        total += 1

    print letter
    print 'Total projects:', total
    print 'Unfinished:', unfinished
    print 'Canceled:', canceled
    print 'Suspended:', suspended
    print 'Live:', live
    print 'Good projects:', total -(unfinished+canceled+suspended+live) + both
