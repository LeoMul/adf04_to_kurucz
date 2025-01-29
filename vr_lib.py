import numpy as np 
import scipy as sci 
from  parsing_adf04 import *
import sys

factor = np.sqrt(3.0) / (2.0*np.pi)

RYDBERG_CM = 109737.316
BOLTZMAN_EV = 8.6173303e-5
RYDBERG_EV = 13.6057039763 

AXELROD_NUMBER = 0.0560758454577287
AXELROD_NUMBER = 0.004

y_table = [0.01,0.02,0.04,0.1,0.2,0.4,1,2,4,10]

p_neural_table = [1.160,0.956,0.758,0.493,0.331,0.209,0.100,0.063,0.040,0.023]

p_single_ionised_table = [1.160,0.977,0.788,0.554,0.403,0.290,0.214,0.201,0.200,0.200]

interpolated_neutral = sci.interpolate.interp1d(y_table,p_neural_table)
interpolated_single_ionised = sci.interpolate.interp1d(y_table,p_single_ionised_table)

def e1(y):
    return -0.57722 - np.log(y)

def P_single_ionised(y):
    
    if y < 0.01:
        return factor * e1(y)
    elif y > 10.0:
        return 0.2
    else:
        return interpolated_single_ionised(y)

def P_neutral(y):
    
    if y < 0.01:
        return factor * e1(y)
    elif y > 10.0:
        return 0.066 / np.sqrt(y)
    else:
        return interpolated_neutral(y)

def P_neutral_array(y_table):
    p = np.zeros_like(y_table)
    for ii in range(0,len(p)):
        p[ii] = P_neutral(y_table[ii])
    return p

def P_single_ionised_array(y_table):
    p = np.zeros_like(y_table)
    for ii in range(0,len(p)):
        p[ii] = P_single_ionised(y_table[ii])
    return p

def P_double_ionised_array(temperature,ion_charge, upper_n, lower_n, upper_energy, lower_energy, ip):

    p = np.zeros_like(temperature)
    for ii in range(0,len(p)):
        p[ii] = vr_pfactor_double_ionized_sjb(temperature[ii],ion_charge, upper_n, lower_n, upper_energy, lower_energy, ip)
    return p


def van_regemorter_single_ionised(temp_array,e_ij_ryd,stat_weight_upper,avalue):

    wavelength_cm = 1.0 / (e_ij_ryd*RYDBERG_CM)

    factor = 2.39e6 * avalue * stat_weight_upper * wavelength_cm**3

    y_array = e_ij_ryd * RYDBERG_EV / (BOLTZMAN_EV*temp_array)
    #print(y_array)
    ecs_vr = factor * P_single_ionised_array(y_array)

    return ecs_vr

def van_regemorter_from_adf04(temp_array,e_i_cm,e_j_cm,stat_weight,avalue,ionisation,princ_upper,princ_lower,ion_potential):

    eij = np.abs(e_i_cm - e_j_cm)

    wavelength_cm = 1.0 / eij
    e_ij_ryd = eij / RYDBERG_CM
    factor = 2.39e6 * avalue * stat_weight * wavelength_cm**3
    y_array = e_ij_ryd * RYDBERG_EV / (BOLTZMAN_EV*temp_array)
    #print(y_array)

    if ionisation == 'neutral':
        ecs_vr = factor * P_neutral_array(y_array)
    elif ionisation == 'first':
        ecs_vr = factor * P_single_ionised_array(y_array)
    elif ionisation == 'second':
        ion_charge = 2
        ecs_vr = factor * P_double_ionised_array(temp_array,ion_charge, princ_upper, princ_lower, max(e_j_cm,e_i_cm), min(e_j_cm,e_i_cm), ion_potential)
    else:
        print('beyond double not implemented')
        sys.exit()

    return ecs_vr

def convert_float_to_adf04string(float):

    x = '{:7.2E}'.format(float).replace('E','')

    #print(x)
    return x

def convert_many_floats_to_adf04(float_array):
    string = ''
    for jj in range(0,len(float_array)):
        string += convert_float_to_adf04string(float_array[jj]) + ' '
    return string 

def write_out_ecs_vr(index_i,index_j,ecs_vr,a_value,outfile,convert_ecs):
    avalue_converted = convert_float_to_adf04string(a_value)
    if convert_ecs == True:
        ecs_converted_string = convert_many_floats_to_adf04(float_array=ecs_vr)
        out_string = ' {:3} {:3} {} {}{}\n'.format(index_i,index_j,avalue_converted,ecs_converted_string,'0.00+00')
    else:
        string = ''
        for jj in ecs_vr:
            string += jj + ' '
    
        out_string = ' {:3} {:3} {} {}\n'.format(index_i,index_j,avalue_converted,string)

    outfile.write(out_string)

    return 0

def calculate_and_write_out_vr(infile,
                               num_levels,
                               temps_kelvin,
                               j_values,
                               wavenumbers,
                               outfile_path,
                               ionisation,
                               axelrod,
                               van_reg,
                               axelrod_coeff,
                               ion_potential,
                               princ_qn
                               ):
    infile_ = open(infile,'r')
    infile_read = infile_.readlines()

    outfile = open(outfile_path,'a')

    for jj in range(num_levels+3,len(infile_read)):

        split = infile_read[jj].split()

        index_i = int(split[0])
        index_j = int(split[1])
        a_value = convert_a_value_string_to_float(split[2])
        current_ecs = split[3:]
        stat_weight = 2.0 * j_values[index_j-1] + 1.0 
        e_i = wavenumbers[index_i-1]
        e_j = wavenumbers[index_j-1]
        wl = 1.0 / np.abs(e_i - e_j)
        upper_weight = 2.0 * j_values[index_i-1] + 1.0
        gf = a_value * upper_weight * wl * wl * 6.6702e-1
        #print(gf)

#def van_regemorter_from_adf04(temp_array,e_i_cm,e_j_cm,stat_weight,avalue,ionisation,princ_upper,princ_lower,ion_potential
        convert = False

        if (axelrod == True) and (gf < 1.0e-3):
            ecs = np.ones(len(temps_kelvin)) * axelrod_coeff * stat_weight * upper_weight
            convert = True

        elif(van_reg == True) and (gf >= 1.0e-3): 
            princ_upper = princ_qn[index_j-1]
            princ_lower = princ_qn[index_i-1]
            ecs = van_regemorter_from_adf04(temps_kelvin,e_i,e_j,upper_weight,a_value,ionisation,princ_upper,princ_lower,ion_potential)
            convert = True
        else:
            ecs = current_ecs

        write_out_ecs_vr(index_i,index_j,ecs,a_value,outfile,convert) 

        if (index_i-index_j) == 1 and (index_i == num_levels):
            break
    outfile.write('-1')
    outfile.write('-1 -1')


def get_princple_quantum_numbers(csf_strings):
    letters = ['s','p','d','f','g','h']
    #rn this only works for things single digit occupations in outermost shell
    num_levels = len(csf_strings)
    principal_quantum_numbers = np.zeros(num_levels)

    for (index,string) in enumerate(csf_strings):
        reduced_string = string[0:-2] 
        if reduced_string[-1] in letters:
            principal_quantum_numbers[index] = float(reduced_string[-2])
        else:
            principal_quantum_numbers[index] = float(reduced_string[-1])

    return principal_quantum_numbers


