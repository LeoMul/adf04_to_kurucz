import atomic_calc
import parsing_adf04
import output

import argparse

MAX_LINES = (2**63-1)

parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument('-f', '--file',  help='Specify path of input file')
parser.add_argument('-r','--reject_bad_a_values',  help='Reject bad A values? i.e 1e-30 in adf04 file (off by default)',action="store_true")
parser.add_argument('-n', '--num_transition',  help='Requested number of lines (all lines by default)',type=int)

args = parser.parse_args()

#if args.help:
#    print("Help Message. Probably")
if not args.file:
    print("No data file specified - printing help")
    parser.print_help()
    exit()
else:
    path = args.file
    if args.num_transition:
        num_requested_lines = args.num_transition 
        print("requesting ",num_requested_lines, " lines")
    else:
        num_requested_lines = MAX_LINES
        print("requesting all lines")


    reject_bad_a_values = False 
    if args.reject_bad_a_values:
        reject_bad_a_values = args.reject_bad_a_values
        reject_bad_a_values = True
        #user_input_a_values = args.reject_bad_a_values
        #print("hello",user_input_a_values)
        #if args.reject_bad_a_values == 0:
        #    reject_bad_a_values = False
        #    print("will not reject bad a values")
        #elif args.reject_bad_a_values == 1:
        #    reject_bad_a_values = True
        #    print("will reject bad a values")
#
        #else:
        #    reject_bad_a_values = False
        #    print("bad a value option - use either 0 or 1 or leave blank")
        #    exit()
    else:
        print("will not reject bad A values")
        reject_bad_a_values = False 
    

def main():
    print("-------------------------")
    print("Initiating adf04 parsing ")
    print("reading file: ",path)
    print("-------------------------")

    elementcode,num_levels = parsing_adf04.read_in_initial(path)
    #this could be made into an object oriented code and probably more pretty, but for the sake of getting results this is good enough imo.

    csfs_strings,term_strings,jvalues,energy_levels_cm_minus_one = parsing_adf04.get_level_and_term_data(path,num_levels)
    a_values_float,upper_levels,lower_levels,num_transitions = parsing_adf04.get_transition_data(num_levels,path)
    wavelengths,transition_energies = atomic_calc.calculate_wavelengths_and_transition_energies(energy_levels_cm_minus_one,upper_levels,lower_levels)

    log_gf,f_values = atomic_calc.calculate_oscillator_strengths(a_values_float,wavelengths,jvalues,upper_levels,lower_levels)
    output.write_out_kurucz_fortran_format(lower_levels,upper_levels,jvalues,wavelengths,a_values_float,log_gf,energy_levels_cm_minus_one,elementcode,csfs_strings,num_requested_lines,reject_bad_a_values)
    #output.write_out_data_in_an_actually_coherent_format(lower_levels,upper_levels,jvalues,wavelengths,a_values_float,log_gf,energy_levels_cm_minus_one,elementcode,csfs_strings)

    return 0 

main()