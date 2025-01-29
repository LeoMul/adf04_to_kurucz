from atomic_calc import *
from parsing_adf04 import *
import sys
from vr_lib import * 
import numpy as np
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',  help='Specify path of input file')
parser.add_argument('-v', '--van_reg',  help='include van regemorter for allowed transitions (default on, turn off to use R-matrix data.)',type=float)
parser.add_argument('-a', '--axelrod',  help='include axelrod for forbidden transitions (default off, but astropeople do it.)',type=float)
parser.add_argument('-o', '--output_name',  help='output file name, otherwise will make something up based on adf04 name',type=str)
args = parser.parse_args()



if not args.file:
    print("No data file specified - printing help")
    parser.print_help()
    exit()
else:

    file = args.file

    x,y,ion_potential = read_in_initial(file)

    element_code_split = x

    diff = element_code_split - np.floor(element_code_split)

    print(diff)

    if np.abs(diff - 0.02) < 0.00001:
        ionisation = 'second'
        print('double ionisation detected')
    elif np.abs(diff - 0.01) < 0.00001:
        ionisation = 'first'
        print('single ionisation detected')
    elif np.abs(diff) < 0.00001:
        ionisation = 'neutral'
        print('neutral ionisation detected')

    else:
        print('higher than double ionised not implemented, stopping')
        sys.exit()



    current_name_un = args.file 

    current_name = np.array([*current_name_un])

    string = ''


    print(current_name)
    index = np.where(current_name == '/')
    index = np.concatenate(index)
    #print(index)
    if len(index) > 0:
        
        for ii in range(max(index)+1,len(current_name)):
            string += current_name[ii]
        current_name_un = string

    if not args.output_name:
        new_file = current_name_un + '_vr.dat'

    else:
        new_file = args.output_name
    coefficient = 0.0
    axelrod = False
    van_reg = True 

    if args.van_reg:
        print('Using Van regemorter for (at least) allowed transitions')
    else:
        van_reg = False 
        print('Using R-matrix data for allowed lines.')

    if args.axelrod:
        axelrod = True
        print("USING AXELROD FOR FORBIDDEN TRANSITIONS")
        coefficient = float(args.axelrod)
    else:
        print("USING van Regemeorter FOR FORBIDDEN TRANSITIONS - not recommended")

    print('writing to')
    print(new_file)
    temps_kelvin = write_out_levels_get_temps(file,y,new_file)
    csfs_strings,term_strings,jvalues,energy_levels_cm_minus_one = get_level_and_term_data(file,num_levels=y)
    qn = (get_princple_quantum_numbers(csfs_strings))
    #n = np.zeros_like(qn)
    #print(qn)
    calculate_and_write_out_vr(file,
                               y,
                               temps_kelvin,
                               jvalues,
                               energy_levels_cm_minus_one,
                               new_file,
                               ionisation,
                               axelrod,
                               van_reg,
                               coefficient,
                               ion_potential,
                               qn)