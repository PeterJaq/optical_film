import os
import model.multi_layer

if __name__ == '__main__':
    film_str = "0.5S 0.25L 0.25H 0.25L"
    mat_list = {"S": "Cu", "L": "SiO2", "H": "Zn"}
    angle = 0
    film = model.multi_layer.MultiLayer(incidence_angle=0, layer=film_str, mat=mat_list, data_path="./data/")