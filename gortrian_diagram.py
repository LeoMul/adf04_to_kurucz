import matplotlib.pyplot as plt
import atomic_calc
import parsing_adf04
import output
import numpy as np
import argparse

MAX_LINES = (2**63-1)

parser = argparse.ArgumentParser()

# Adding optional argument

parser.add_argument('-f', '--file',  help='Specify path of input file')
parser.add_argument('-n', '--num_transition',  help='Requested number of lines (all lines by default)',type=int)
parser.add_argument('-o', '--output_name',  help='output file name, otherwise will make something up based on adf04 name',type=str)
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


    

def main():
    print("-------------------------")
    print("Initiating adf04 parsing ")
    print("reading file: ",path)
    print("-------------------------")

    elementcode,num_levels,x = parsing_adf04.read_in_initial(path)
    #this could be made into an object oriented code and probably more pretty, but for the sake of getting results this is good enough imo.
    file_name_string = ''
    if args.output_name:
        file_name_string = args.output_name
    else:
        file_name_string = 'Kurucz_formatted_adf04_element' + str(elementcode)

    csfs_strings,term_strings,jvalues,energy_levels_cm_minus_one = parsing_adf04.get_level_and_term_data(path,num_levels)
    print(term_strings)
    a_values_float,upper_levels,lower_levels,num_transitions = parsing_adf04.get_transition_data(num_levels,path)
    wavelengths,transition_energies = atomic_calc.calculate_wavelengths_and_transition_energies(energy_levels_cm_minus_one,upper_levels,lower_levels)

    log_gf,f_values = atomic_calc.calculate_oscillator_strengths(a_values_float,wavelengths,jvalues,upper_levels,lower_levels)

    plt.figure()


    fig, ax = plt.subplots()
    max_level = 10

    level_map = np.zeros(max_level)
    unique_csfs = []
    counter = 0
    for jj in range(0,max_level):
        current_csf = csfs_strings[jj]
        if current_csf not in unique_csfs:
            unique_csfs.append(current_csf)
            level_map[jj] = counter 
            counter +=1
        else:
            i = unique_csfs.index(current_csf)
            level_map[jj] = i
    level_map+=1
    #print(level_map)


    uppers_to_be_kept = []
    lowers_to_be_kept = []
    log_gf_to_be_kept = []

    for ii in range(0,len(log_gf)):
        upper = upper_levels[ii]
        lower = lower_levels[ii]
        if (upper < max_level+1) and (lower < max_level+1):
            uppers_to_be_kept.append(upper)
            lowers_to_be_kept.append(lower)
            log_gf_to_be_kept.append(log_gf[ii])

    for ii in range(0,max_level):
        #print(energy_levels_cm_minus_one[ii])
        x = level_map[ii]
        ax.hlines(y=energy_levels_cm_minus_one[ii], xmin=x-0.25, xmax=x+0.25, linewidth=0.5, color='k')



    log_gf = np.array(log_gf_to_be_kept)
    upper_levels = uppers_to_be_kept
    lower_levels = lowers_to_be_kept

    opacity_range =  np.power(10,log_gf )
    opacity_range-= min(opacity_range) 
    opacity_range /= max(opacity_range)
    #opacity_range *= 255.01
    #a = 100.0
    #opacity_range = np.exp(opacity_range*a) - 1.0 
    #opacity_range /= (np.exp(a) - 1.0)
    #print('max is',max(opacity_range))

    print(lower_levels)
    for ii in range(0,len(log_gf)):
        upper = upper_levels[ii]
        lower = lower_levels[ii]

        if (upper < max_level+1) and (lower < max_level+1):
            x = level_map[lower-1]
            xpdx = level_map[upper-1] 


            dx = xpdx-x
            
            y = energy_levels_cm_minus_one[lower-1]
            dy = energy_levels_cm_minus_one[upper-1]-energy_levels_cm_minus_one[lower-1]
            op = opacity_range[ii]
            if op > 0.02:
                print(log_gf[ii],op,lower,upper)
            ax.arrow(x,y,dx,dy, alpha=op,color='b',linewidth=0.5)
            #print(op)
            #print(lower,upper,energy_levels_cm_minus_one[lower-1],energy_levels_cm_minus_one[upper-1])

            #if x == 3 and xpdx == 5:
            #    
            #    

    plt.xticks(ticks=np.arange(1,len(unique_csfs)+1,1),labels=unique_csfs)
    plt.xlabel("Configuration")
    plt.ylabel("Fine-structure level (cm-1)")
    #plt.yscale('log')
    #plt.ylim([])
        #for ii in range(0,level_cut_off_max):
    #    for jj in range(ii+1,level_cut_off_max):
    #            if jj < max_level:
    #                



    fig.savefig('got_test.pdf')

    return 0 

main()
