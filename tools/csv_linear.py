import csv

'''
constant_value = {
    wavelength = "wavelength",
    n_value = "n_value",
    k_value = "k_value"
}
'''

inputfile = "./data/InAs.csv"
outputfile = "./data/InAs_Similiar.csv"

#constant_value = []

def linear_similiar(constant_values, begin_wavelength, end_wavelength):
    constant_value_wavelength = []
    constant_value_n_value = []
    constant_value_k_value = []
    linear_constants = []

    for constant_value in constant_values:
        constant_value_wavelength.append(constant_value[0])
        constant_value_n_value.append(constant_value[1])
        constant_value_k_value.append(constant_value[2])

    perview_wavelength = 0
    next_wavelength = 0

    for wavelength in range(begin_wavelength, end_wavelength):
        linear_constant = []

        if wavelength in constant_value_wavelength:
            linear_constant.append(wavelength)
            value_index = constant_value_wavelength.index(wavelength)
            linear_constant.append(constant_value_n_value[value_index])
            linear_constant.append(constant_value_k_value[value_index])
            linear_constants.append(linear_constant)
            perview_wavelength = wavelength
            next_wavelength = constant_value_wavelength[value_index + 1]

        else:
            perview_index = constant_value_wavelength.index(perview_wavelength)
            perview_wavelength_n_value = constant_value_n_value[perview_index]
            perview_wavelength_k_value = constant_value_k_value[perview_index]

            next_index = constant_value_wavelength.index(next_wavelength)
            next_wavelength_n_value = constant_value_n_value[next_index]
            next_wavelength_k_value = constant_value_k_value[next_index]

            gradient_n = (next_wavelength_n_value - perview_wavelength_n_value)/(next_wavelength - perview_wavelength)
            gradient_k = (next_wavelength_k_value - perview_wavelength_k_value)/(next_wavelength - perview_wavelength)

            linear_constant.append(wavelength)
            linear_constant.append(perview_wavelength_n_value + ((wavelength - perview_wavelength) * gradient_n))
            linear_constant.append(perview_wavelength_k_value + ((wavelength - perview_wavelength) * gradient_k))
            linear_constants.append(linear_constant)

    return linear_constants

constant_values = []

with open(inputfile, 'r') as f:
    reader = csv.reader(f)
    print(reader)
    for line in reader:
        constant_value = []
        wavelength_nm = float(line[0]) * 1000
        #print(wavelength_nm)
        int_wavelength_nm = int(float(line[0]) * 1000)
        print(int_wavelength_nm)
        print(line[1])
        n_value = (float(line[1]) / wavelength_nm) * int_wavelength_nm 
        k_value = (float(line[2]) / wavelength_nm) * int_wavelength_nm 

        constant_value.append(int_wavelength_nm) 
        constant_value.append(n_value) 
        constant_value.append(k_value)
        constant_values.append(constant_value) 

begin_wavelength = 206
end_wavelength = 826

linear_constants = linear_similiar(constant_values, begin_wavelength, end_wavelength)

datacsv=open(outputfile,'w',encoding='utf8',newline='')
csvwriter = csv.writer(datacsv,dialect=("excel"))
for line in linear_constants:
    csvwriter.writerow(line)  
    
print(linear_constants)