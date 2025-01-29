import atomic_calc
import parsing_adf04
import output

import numpy as np

def main(adf04_file,reorder_file=''):

    adf04_raw = open(adf04_file,'r')
    output_name = adf04_file + '_rearranged'
    outputfile = open(output_name,'w')
    adf04_raw_data = adf04_raw.readlines()
    outputfile.write(adf04_raw_data[0])
    #outputfile.write(adf04_raw_data[1])

    reorder = np.loadtxt(reorder_file,dtype=int)

    before_index = reorder[:,0]
    new_index = reorder[:,1]

    counter = 0 
    levels_found = False
    for jj in range(0,len(adf04_raw_data)):
        counter+= 1
        if adf04_raw_data[jj].split() == ['-1']:
            print('found')
            levels_found = True
            break 
        
    if levels_found == False:
        print("couldnt find -1 at end of levels. check input.")
        return 

    num_levels = counter - 2

    print(" i found ",num_levels,' levels')
    levels_data = adf04_raw_data[1:counter-1]


    shifted_level_data = []
    for jj in range(0,num_levels):
        shifted_level_data.append('')

    for jj in range(0,num_levels):
        shifted_level_data[new_index[jj]-1] = levels_data[before_index[jj]-1]

    for jj in range(0,num_levels):
        outputfile.write(shifted_level_data[jj])

    print(shifted_level_data)
    outputfile.write('   -1\n')

    x = np.chararray([num_levels,num_levels],itemsize = 1000)
    x[0,0] = adf04_raw_data[counter+3]
    print(x[0,0])
    outputfile.write(str(x[0,0]).replace('b',))
    return 0    


import argparse
MAX_LINES = (2**63-1)
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument('-f', '--file',  help='Specify path of input file')
parser.add_argument('-r', '--reorder',  help='Specify path of reorder file')

args = parser.parse_args()

#if args.help:
#    print("Help Message. Probably")
if not args.file:
    print("No data file specified - printing help")
    parser.print_help()
    exit()
else:
    path = args.file
    main(path,reorder_file=args.reorder) 



