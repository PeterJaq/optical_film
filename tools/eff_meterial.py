"""
Effective medium approximations:

INPUT:

The  effective dielectric constant:  eps_base, eps_incl

The  volume fraction of the inclusions: vol_incl

The knowledge from the wiki: Maxwell-Garnett equation:

OUTPUT:

The  effective dielectric constant: eps_mean

2018/2/24 BY Jiang A.Q.

Prof.Chen lab, Fudan Univ.
Prof.Yoshie lab, IPS, Waseda Univ.
"""

import scipy
import math

def effective_meterial_model(eps_base_li, eps_incl_li, vol_incl, model="Maxwell-Garnett"):
    eps_mean_li = []
    for _ in range(0, len(eps_base_li)):
        eps_base = eps_base_li[_]
        eps_incl = eps_incl_li[_]
        print(eps_base)
        print(eps_incl)
        if model == "Maxwell-Garnet":
            eps_value = Maxwell_Garnett_equation(eps_base, eps_incl, vol_incl)
        elif model == "Bruggeman":
            eps_value = Bruggeman_equation(eps_base, eps_incl, vol_incl)
        eps_mean_li.append(eps_value)

    return eps_mean_li

def Maxwell_Garnett_equation(eps_base, eps_incl, vol_incl):
    factor_up = 2 * vol_incl * (eps_incl - eps_base) + eps_incl + 2 * eps_base
    factor_down = 2 * eps_base + eps_incl + vol_incl * (eps_base - eps_incl)
    eps_value = eps_base * factor_up / factor_down

    return eps_value

def Bruggeman_equation(ea, eb, p):
    operator = 8 * ea * eb + ((ea - 2 * eb - 3*ea*p + 3 * eb * p)**(1/2))
    eps_value = 0.25 * (-ea + 2 * eb + 3 * ea * p - 3 * eb * p - (operator ** (1/2)))
    return eps_value
