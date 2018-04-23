import os
import csv
import string
from scipy import io

def file_write(wavelen, constant_n, constant_k, filename):
    try:
        file = open(filename, 'w')
    except IOError:
        print('*** file open error:')

    for i in range(0, len(constant_n)):
        file.write("%f, %f, %f\n" % (wavelen[i], constant_n[i], constant_k[i]))
    file.close()

