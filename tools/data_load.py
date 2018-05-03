import os
import string
import numpy
import csv
from scipy.interpolate import interp1d

def dataload(filename, waveLenRange):
    n = []
    k = []
    wavlen = []

    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            data = lines.strip().split(" ")
            data[0] = float(data[0])

            n.append(data[1])
            k.append(data[2])
            if(data[0] < 10):
                wavlen.append(float(data[0])*1000)
            else:
                wavlen.append(float(data[0]))

        fn = interp1d(wavlen, n)
        fk = interp1d(wavlen, k)

        new_n = fn(waveLenRange)
        new_k = fk(waveLenRange)

        return new_n, new_k


def data_load_model(filename):
    n = []
    k = []
    w = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            data = lines.strip().split(" ")
            data[0] = float(data[0])
            w.append(data[0])
            n.append(data[1])
            k.append(data[2])

    return [w, n, k]


"""
Model TEST:
def main():
    filename = "SIO2"
    data = dataload(filename, 0.2, 1.0)
    print(data)

if __name__ == '__main__':
    main()

"""