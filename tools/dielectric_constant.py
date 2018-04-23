"""
Dielectric constant:

INPUT:

The N/K value of meterials: n_val, k_val

OUTPUT:

The  effective dielectric constant: Dielectric constant

2018/2/24 BY Jiang A.Q.

Prof.Chen lab, Fudan Univ.
Prof.Yoshie lab, IPS, Waseda Univ.
"""


def dielectric_constant_normal(n_val, k_val):
    return pow(n_val, 2) - pow(k_val, 2)


def dielectric_constant_complex(n_val, k_val):
    return pow(n_val, 2) - pow(k_val, 2), 2*n_val*k_val


def dielectric_constant(n, k):
    dielectric_constant_cpx = []
    
    if len(n) == len(k):
        for index in range(0, len(n)):
            n_val = n[index]
            k_val = k[index]
            real, image = dielectric_constant_complex(n_val, k_val)
            dielectric_constant_cpx.append(complex(real, image))

    return dielectric_constant_cpx

