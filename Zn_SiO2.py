import numpy as np
import matplotlib.pyplot as plt
from tools import dielectric_constant
from tools import eff_meterial
from tools import eps2nk
from tools import file_load
from tools import data_load

FACTOR_VOL = 0.16
OUT_PUT_FILE = "./data/new_meterial_%s.txt" % FACTOR_VOL
MET_A_PATH = "./data/Zn.txt"
MET_B_PATH = "./data/SiO2.txt"

def rmse(predictions, targets):
    return np.sqrt(((np.array(predictions) - np.abs(np.array(targets))-np.array(predictions)) ** 2).mean())

def main():

    vol_incl = FACTOR_VOL
    begin_wavlen = 250
    end_wavlen = 1500
    bendlen = (end_wavlen - begin_wavlen)/5
    x = np.linspace(begin_wavlen, end_wavlen, num=bendlen, endpoint=True)

    Zn_n, Zn_k = data_load.dataload(MET_A_PATH, x)
    Zn_DielectricConstantCpx = dielectric_constant.dielectric_constant(Zn_n, Zn_k)

    SiO2_n, SiO2_k = data_load.dataload(MET_B_PATH, x)
    SiO2_DielectricConstantCpx = dielectric_constant.dielectric_constant(SiO2_n, SiO2_k)

    new_meterial_Cpx = eff_meterial.effective_meterial_model(Zn_DielectricConstantCpx, SiO2_DielectricConstantCpx,
                                                             vol_incl, model="Bruggeman")
    new_n = eps2nk.cal_n(new_meterial_Cpx)
    new_k = eps2nk.cal_k(new_meterial_Cpx)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x, new_n, label='n')
    ax1.set_ylabel('N value')
    ax1.set_title("N/K value of Zn%f+SiO2, RMSE = %f" % (vol_incl, rmse(new_n, new_k)))
    plt.legend(loc=2)
    ax2 = ax1.twinx()
    ax2.plot(x, new_k, 'r', label="k")
    ax2.set_ylabel('K value')
    ax2.set_xlabel('wavelength')
    plt.legend(loc=1)
    plt.show()

    file_load.file_write(x, new_n, new_k, OUT_PUT_FILE)


if __name__ == '__main__':
    #for f in range(0, 30, 2):
    #    main(f/100)
    main()