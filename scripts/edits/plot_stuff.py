import matplotlib.pyplot as plt
import pickle
import sys
import numpy as np

if len(sys.argv) > 1:
    filename = sys.argv[1]

obj = pickle.load(open(filename,'r'))
print sum(obj)/len(obj)
print np.mean(obj)
print np.var(obj)
print np.median(obj)

plt.hist(obj, bins = np.arange(-2,2,0.1))
plt.axvline(np.mean(obj), color='g', linestyle='dashed', linewidth=2)
plt.axvline(np.median(obj), color='r', linestyle='dashed', linewidth=2)
plt.xlabel('Impact of edit on reward')
plt.ylabel('Number of edits')
plt.show()

