import numpy as np
import math
import string
from scipy.interpolate import interp1d
from tools import data_load


class MultiLayer(object):

    def __init__(self, incidence_angle, layer, mat, data_path):

        #self.optical_constant = optical_constant
        #self.optical_constant_inter = self.inter_op(self.optical_constant)
        #self.refractive_index = zip(self.optical_constant_inter[0], self.optical_constant_inter[1])
        #self.extinction_coefficient = zip(self.optical_constant_inter[0], self.optical_constant_inter[1])
        #self.thickness = thickness
        self.incidence_angle = incidence_angle
        self.layer, self.layer_len = self.layers_structure(layer)
        self.data_path = data_path
        self.mat = mat
        self.n0 = []
        self.nk = []
        self.max_wavelength = 1600
        self.min_wavelength = 250

        self.mat_data = self.get_mat_data()
        self.A = self.cal_final_result()


    def get_mat_data(self):
        mat_data = {}
        for k, mat in self.mat.items():
            filename = self.data_path + mat + ".txt"
            mat_data[mat] = self.inter_op(data_load.data_load_model(filename))

        return mat_data

    def inter_op(self, optical_constant):

        wavelength = optical_constant[0]
        b_refractive_index = optical_constant[1]
        b_extinction_coefficient = optical_constant[2]

        aim = np.linspace(self.min_wavelength, self.max_wavelength, num=(self.max_wavelength-self.min_wavelength)/10, endpoint=True)

        fn = interp1d(wavelength, b_refractive_index)
        fk = interp1d(wavelength, b_extinction_coefficient)
        refractive_index = fn(aim)
        extinction_coefficient = fk(aim)

        return [aim, refractive_index, extinction_coefficient]

    def cal_admittance_p(self, n, k, in_ag):

        N = self.cal_N(n, k)

        return N*math.cos(in_ag)

    def cal_admittance_s(self, n, k, in_ag):

        N = self.cal_N(n, k)

        return N/math.cos(in_ag)

    def cal_optical_thickness(self, w, n, k, th, in_ag):

        N = self.cal_N(n, k)
        pi = math.pi

        return (2*pi/w)*N*th*math.cos(in_ag)

    def cal_N(self, n, k):

        return complex(n, k)

    def cal_Y(self, B, C):

        return B/C

    def cal_refractive_rate(self, n0, B, C):

        Y = self.cal_Y(B, C)
        cop = (n0 - Y)/(n0 + Y)
        cop_conj = cop.conjugate()

        return cop/cop_conj

    def cal_transmittance(self, n0, nk, B, C):

        Y = self.cal_Y(B, C)
        up = 4 * n0 * nk
        down = (n0 + Y)*((n0 + Y).conjugate())

        return up/down

    def cal_absorption(self, n0, nk, B, C):
        R = self.cal_refractive_rate(n0, B, C)
        T = self.cal_transmittance(n0, nk, B, C)

        return 1 - R - T

    def layers_structure(self, layers):

        layers_temp = layers.split(" ")

        value = []
        mat = []

        for layer in layers_temp:
            value.append(float(layer[0:-1]))
            mat.append(layer[-1])

        return zip(mat, value), len(layers_temp)

    #def mat_zip(self, mats):

    #    mats = "{" + mats + "}"

    #    return eval(mats)

    def cal_layer_feature(self):

        mat = self.mat
        layers = self.layer
        s_list = []
        temp_list = []
        BC = []

        for index, layer in enumerate(layers):

            th = layer[1]
            l_mat = self.mat_data[self.mat[layer[0]]]
            w_list = l_mat[0]
            n_list = l_mat[1]
            k_list = l_mat[2]

            for i in range(0, len(w_list)):
                w = w_list[i]
                n = n_list[i]
                k = k_list[i]
                temp_list.append(self.cal_M_s(w, n, k, th, self.incidence_angle))
                if index == self.layer_len - 1:
                    s_list.append(np.array([[1], [self.cal_admittance_s(n, k, self.incidence_angle)]]))
                    self.nk.append(self.cal_admittance_s(n, k, self.incidence_angle))
                if index == 0:
                    self.n0.append(self.cal_admittance_s(n, k, self.incidence_angle))
            if index == 0:
                m_list = temp_list

            else:
                for _ in range(0, len(m_list)):
                    #if _ == 138:
                        #print(_)
                    m_list[_] = np.dot(m_list[_], temp_list[_])


            temp_list = []
        for _ in range(0, len(m_list)):
            print(m_list[_])
            print(s_list[_])
            print(np.dot(m_list[_], s_list[_]))
            BC.append(np.dot(m_list[_], s_list[_]))


        return BC


    def cal_M_s(self, w, n, k,th, in_ag):

        delta = self.cal_optical_thickness(w, n, k, th, in_ag)
        y = self.cal_admittance_s(n, k, in_ag)
        i = complex(0, 1)
        M = np.array([[np.cos(delta), (i*np.sin(delta))/y], [i*y*np.sin(delta), np.cos(delta)]])

        return M


    def cal_M_p(self, w, n, k, th, in_ag):

        delta = self.cal_optical_thickness(w, n, k, th, in_ag)
        y = self.cal_admittance_p(n, k, in_ag)
        i = complex(0, 1)

        M = np.array([math.cos(delta), (i*math.sin(delta)) / y],
                     [i*y*math.sin(delta), math.cos(delta)])

        return M
        
    def find_mat(self, mat):

        optical_constant = self.inter_op(mat)

        return optical_constant

    def cal_final_result(self):

        BC_list = self.cal_layer_feature()

        A = []
        #for BC, n0, nk  in BC_list, self.n0, self.nk:
        for i in range(0, len(BC_list)):
            B = BC_list[i][0]
            C = BC_list[i][1]

            Y = self.cal_Y(B, C)
            A.append(self.cal_absorption(self.n0[i], self.nk[i], B, C))

        return A


