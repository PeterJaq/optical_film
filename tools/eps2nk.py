import math

def cal_n(eps_li):
    n_val = []
    for _ in range(0, len(eps_li)):
        eps_cpx = eps_li[_]
        eps_real = eps_cpx.real
        eps_image = eps_cpx.imag

        n_up = math.sqrt(math.pow(eps_real, 2) + math.pow(eps_image, 2)) + eps_real
        n_down = 2

        n_val.append(math.sqrt(n_up/n_down))
    return n_val


def cal_k(eps_li):
    k_val = []
    for _ in range(0, len(eps_li)):
        eps_cpx = eps_li[_]
        eps_real = eps_cpx.real
        eps_image = eps_cpx.imag
        k_up = math.sqrt(math.pow(eps_real, 2) + math.pow(eps_image, 2)) - eps_real
        k_down = 2

        k_val.append(math.sqrt(k_up / k_down))
    return k_val

