import wget
from eeg_analysis import read_edf
import time
import numpy 
import os

data, electrodes = read_edf()

eeg_names = "RECORDS-WITH-SEIZURES.txt"
eeg_names = numpy.genfromtxt("RECORDS-WITH-SEIZURES.txt", delimiter=",", dtype=str)
num_of_eeg = len(eeg_names)
print("EEG's : {}".format(num_of_eeg))


os.makedirs("EEG_DATA")
total_time_1 = time.time()
for i in range(0, num_of_eeg, 1):
    print("Downloading {}\n".format(eeg_names[i]))
    init_time = time.time()
    url = 'https://physionet.org/files/chbmit/1.0.0/{}?download'.format(eeg_names[i])
    filename = wget.download(url,)
    end_time = time.time()
    print("\n Elpsed time: {} sec".format(end_time-init_time))
total_time_2 = time.time()
print("Total time elapsed: {}".format(total_time_2-total_time_1))
