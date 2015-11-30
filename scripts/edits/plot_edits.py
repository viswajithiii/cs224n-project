import pickle
import matplotlib.pyplot as plt

scatter_list = pickle.load(open('scatter_list.pickle', 'r'))
difference_list = []
gain_list = []
for difference, gain in scatter_list:
    if abs(gain) < 500:
        difference_list.append(difference)
        gain_list.append(gain)
plt.scatter(difference_list, gain_list)
plt.show()