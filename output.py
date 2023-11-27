import fortranformat as ff
import re
import numpy as np
MAX_LINES = (2**63-1)

def write_out_stuff_for_tests(lower_levels,upper_levels,jvalues,wavelengths,avalues,loggf,num_to_be_printed):
    num_trans = len(lower_levels)
    if num_to_be_printed > num_trans:
        will_print = num_trans 
    else:
        will_print = num_to_be_printed 

    print("Upper, Lower,Upper J, Lower J, Wavelength, Avalue, loggf ")

    for jj in range(0,will_print):
        lower_index = lower_levels[jj]
        upper_index = upper_levels[jj]
        print(upper_index,lower_index,jvalues[upper_index-1],jvalues[lower_index-1],wavelengths[jj],avalues[jj],loggf[jj])

def make_level_labels(csf_strings):
    labels = []
    num = len(csf_strings)
    for ii in range(num):
        new_string = csf_strings[ii]
        new_string = re.sub("\(.*?\)","",csf_strings[ii])[0:10]
        length = len(new_string)
        if length < 10:
            new_string = ' ' * (10-length) + new_string 
        labels.append(new_string) 
    return labels       

def make_level_labels_full_length(csf_strings):
    labels = []
    num = len(csf_strings)
    for ii in range(num):
        new_string = csf_strings[ii]
        new_string = re.sub("\(.*?\)","",csf_strings[ii])
        length = len(new_string)
        labels.append(new_string) 
    return labels  


def print_out_kurucz_format(lower_levels,upper_levels,jvalues,wavelengths,avalues,loggf,wavenumbers,elementcode,csfs):
    num_trans = len(wavelengths)

    labels = make_level_labels(csf_strings=csfs)

    make_level_labels(csf_strings=csfs)
    for jj in range(0,1000):

        lower_level_index = lower_levels[jj]
        upper_level_index = upper_levels[jj]

        #this is probably incredibly poor string formatting ettiquette but it is 2224 on a saturday and i'm not fussed

        string_to_be_written = '{:11.4f}'.format(wavelengths[jj])
        string_to_be_written += '{:7.3f}'.format(loggf[jj])
        string_to_be_written += '{:6.2f}'.format(elementcode)

        string_to_be_written += '{:12.3f}'.format(wavenumbers[lower_level_index-1])
        string_to_be_written += '{:5.1f}'.format(jvalues[lower_level_index-1])

        string_to_be_written += ' ' +labels[lower_level_index-1][0:10]
        
        string_to_be_written += '{:12.3f}'.format(wavenumbers[upper_level_index-1])
        string_to_be_written += '{:5.1f}'.format(jvalues[upper_level_index-1])
        string_to_be_written += ' ' +labels[upper_level_index-1][0:10]
        string_to_be_written += '{:6.2f}'.format(0.0)
        string_to_be_written += '{:6.2f}'.format(0.0)
        string_to_be_written += '{:6.2f}'.format(0.0)
        string_to_be_written += '    DARC'
        
        string_to_be_written += '  {:}'.format(0)
        string_to_be_written += '{:6.3f}'.format(0.0)

        string_to_be_written += '  {:}'.format(0)
        string_to_be_written += '{:6.3f}'.format(0.0)

        string_to_be_written += '    {:}'.format(0)
        string_to_be_written += '    {:}'.format(0)

        string_to_be_written += '      {:}'.format(0)
        string_to_be_written += '       {:}'.format(0)
        string_to_be_written += '    {:}'.format(0)
        string_to_be_written += '     {:}'.format(0)
        print(string_to_be_written)
    return 0

def write_out_kurucz_format(lower_levels,upper_levels,jvalues,wavelengths,avalues,loggf,wavenumbers,elementcode,csfs):
    num_trans = len(wavelengths)
    f = open('Kurucz_formatted_adf04_element' + str(elementcode),'w')
    labels = make_level_labels(csf_strings=csfs)

    make_level_labels(csf_strings=csfs)
    for jj in range(0,num_trans):

        lower_level_index = lower_levels[jj]
        upper_level_index = upper_levels[jj]

        #this is probably incredibly poor string formatting ettiquette but it is 2224 on a saturday and i'm not fussed

        string_to_be_written = '{:11.4f}'.format(wavelengths[jj])
        string_to_be_written += '{:7.3f}'.format(loggf[jj])
        string_to_be_written += '{:6.2f}'.format(elementcode)

        string_to_be_written += '{:12.3f}'.format(wavenumbers[lower_level_index-1])
        string_to_be_written += '{:5.1f}'.format(jvalues[lower_level_index-1])

        string_to_be_written += ' ' +labels[lower_level_index-1][0:10]
        
        string_to_be_written += '{:12.3f}'.format(wavenumbers[upper_level_index-1])
        string_to_be_written += '{:5.1f}'.format(jvalues[upper_level_index-1])
        string_to_be_written += ' ' +labels[upper_level_index-1][0:10]
        string_to_be_written += '{:6.2f}'.format(0.0)
        string_to_be_written += '{:6.2f}'.format(0.0)
        string_to_be_written += '{:6.2f}'.format(0.0)
        string_to_be_written += '       0'
        
        string_to_be_written += '  {:}'.format(0)
        string_to_be_written += '{:6.3f}'.format(0.0)

        string_to_be_written += '  {:}'.format(0)
        string_to_be_written += '{:6.3f}'.format(0.0)

        string_to_be_written += '    {:}'.format(0)
        string_to_be_written += '    {:}'.format(0)

        #string_to_be_written += '      {:}'.format(0)
        string_to_be_written += '              {:}'.format(0)
        string_to_be_written += '    {:}'.format(0)
        #string_to_be_written += '     {:}'.format(0) 
        if jj < (num_trans-1):
            string_to_be_written += '\n'
        f.write(string_to_be_written)
    f.close()
    return 0

def write_out_kurucz_fortran_format(lower_levels,upper_levels,jvalues,wavelengths,avalues,loggf,wavenumbers,elementcode,csfs,level_truncate,reject_bad_a_values):
    num_trans = len(wavelengths)


    print("INITIATING KURUCZ FORMAT BUSINESS")

    file_name_string = 'Kurucz_formatted_adf04_element' + str(elementcode)

    f = open(file_name_string,'w')
    labels = make_level_labels(csf_strings=csfs)

    print("Writing out to ",file_name_string)
    format_string = 'F11.4,F7.3,F6.2,F12.3,F5.1,1X,A10,F12.3,F5.1,1X,A10,F6.2,F6.2,F6.2,A4,I2,I2,I3,F6.3,I3,F6.3,I5,I5,A10,I5,I5'
    line = ff.FortranRecordWriter(format_string)

    num_trans_to_be_printed = 0

    #if level_truncate==MAX_LINES:
    #    print("User requested all lines",num_trans)
    #else:
    #    print("User requested ",level_truncate," lines")

    if level_truncate==MAX_LINES:
        print("User requested all lines",num_trans)
        num_trans_to_be_printed = num_trans
    elif level_truncate > num_trans:
        print("too many lines requested - requesting max number  ",num_trans)
        num_trans_to_be_printed = num_trans
    else: 
        num_trans_to_be_printed = level_truncate
        print("User requested ",num_trans_to_be_printed," lines")
    print("-------------------------")
    print("printing")
    rejected_transitions_wavelength = 0
    rejected_transitions_a_value = 0
    suspect_transitions_a_value = 0
    for iter in range(0,num_trans_to_be_printed):
        current_wavelength = wavelengths[iter]
        current_a_value = avalues[iter]
        lower_index = lower_levels[iter]-1
        upper_index = upper_levels[iter]-1

        if (current_wavelength >= 1e6):
            #too large a wavelength breaks the fortran format, and too low an avalue probably doesnt matter anyway.
            #print("rejecting transition from ",lower_index+1, "to ",upper_index+1," with wavelength ",current_wavelength, " angs and Einstein A value ",current_a_value)
            rejected_transitions_wavelength += 1
            print("ignoring",upper_index+1,lower_index+1)
        elif ((current_a_value < 1e-29) and (reject_bad_a_values == True)):
            rejected_transitions_a_value += 1
        else:
            #but not rejected ... logic could probably be better structured
            if current_a_value < 1e-29:
                suspect_transitions_a_value+=1

            array = [current_wavelength,loggf[iter],elementcode] 
            lower_level_info = [wavenumbers[lower_index],jvalues[lower_index],labels[lower_index]]
            upper_level_info = [wavenumbers[upper_index],jvalues[upper_index],labels[upper_index]]

            first_zero_array =[0,0,0]
            second_zero_array = [0,0]

            array.extend(lower_level_info)
            array.extend(upper_level_info)
            array.extend(first_zero_array)
            array.extend(['gfxxyy'])
            array.extend(first_zero_array)
            array.extend(first_zero_array)
            array.extend(second_zero_array)
            array.extend([''])
            array.extend(second_zero_array)

            #print(line.write(array))
            f.write(line.write(array))
            f.write("\n")
            #print(wavelengths[iter])
    print("-------------------------")
    rejected_transitions = rejected_transitions_a_value + rejected_transitions_wavelength
    print("output summary: ")
    print(num_trans_to_be_printed, 'lines requested')
    print(rejected_transitions," lines rejected")
    print('       ',rejected_transitions_wavelength,'bad wavelengths rejected')
    if reject_bad_a_values == True:
        print('       ',rejected_transitions_a_value,'bad A values rejected')
    else:
        print('       ',suspect_transitions_a_value,'bad A values found (not rejected as per user instruction)')
    print(num_trans_to_be_printed-rejected_transitions, "lines printed")
    print("output data is in ",file_name_string)
    print("-------------------------")

    return 0

def write_out_line_list_my_format_fortran_format(lower_levels,upper_levels,jvalues,wavelengths,avalues,loggf,wavenumbers,elementcode,csfs,level_truncate,reject_bad_a_values):
    num_trans = len(wavelengths)


    print("INITIATING MORE EASY TO UNDERSTAND FORMAT BUSINESS")

    file_name_string = 'lines_formatted_adf04_element' + str(elementcode)

    f = open(file_name_string,'w')
    labels = csfs

    print("Writing out to ",file_name_string)
    format_string = 'F15.4,ES10.3,ES10.3,ES10.3,F6.2,I5,F5.1,1X,A15,F12.3,I5,F5.1,1X,A15,F12.3'    
    line = ff.FortranRecordWriter(format_string)

    num_trans_to_be_printed = 0

    if level_truncate==MAX_LINES:
        print("User requested all lines",num_trans)
    else:
        print("User requested ",level_truncate," lines")


    if level_truncate > num_trans:
        print("too many lines requested - requesting max number  ",num_trans)
        num_trans_to_be_printed = num_trans
    else: 
        num_trans_to_be_printed = level_truncate
        print("printing ",num_trans_to_be_printed," lines")
    print("-------------------------")

    rejected_transitions_wavelength = 0
    rejected_transitions_a_value = 0
    suspect_transitions_a_value = 0
    for iter in range(0,num_trans_to_be_printed):
        current_wavelength = wavelengths[iter]
        current_a_value = avalues[iter]
        lower_index = lower_levels[iter]-1
        upper_index = upper_levels[iter]-1

        if (current_wavelength >= 1e8 or current_wavelength == np.inf):
            #too large a wavelength breaks the fortran format, and too low an avalue probably doesnt matter anyway.
            #print("rejecting transition from ",lower_index+1, "to ",upper_index+1," with wavelength ",current_wavelength, " angs and Einstein A value ",current_a_value)
            rejected_transitions_wavelength += 1
            print("ignoring",upper_index+1,lower_index+1)
        elif ((current_a_value < 1e-29) and (reject_bad_a_values == True)):
            rejected_transitions_a_value += 1
        else:
            #but not rejected ... logic could probably be better structured
            if current_a_value < 1e-29:
                suspect_transitions_a_value+=1

            stat_weight = 2.0 * jvalues[lower_index] + 1
            other_weight = 2.0 * jvalues[upper_index] + 1
            array = [current_wavelength,current_a_value,stat_weight*current_a_value,other_weight*current_a_value,elementcode] 
            lower_level_info = [lower_index+1,jvalues[lower_index],labels[lower_index],wavenumbers[lower_index]]
            upper_level_info = [upper_index+1,jvalues[upper_index],labels[upper_index],wavenumbers[upper_index]]

    
            array.extend(lower_level_info)
            array.extend(upper_level_info)

            #print(line.write(array))
            f.write(line.write(array))
            f.write("\n")
            #print(wavelengths[iter])
    print("-------------------------")
    rejected_transitions = rejected_transitions_a_value + rejected_transitions_wavelength
    print("output summary: ")
    print(num_trans_to_be_printed, 'lines requested')
    print(rejected_transitions," lines rejected")
    print('       ',rejected_transitions_wavelength,'bad wavelengths rejected')
    if reject_bad_a_values == True:
        print('       ',rejected_transitions_a_value,'bad A values rejected')
    else:
        print('       ',suspect_transitions_a_value,'bad A values found (not rejected as per user instruction)')
    print(num_trans_to_be_printed-rejected_transitions, "lines printed")
    print("output data is in ",file_name_string)
    print("-------------------------")

    return 0



def write_out_data_in_an_actually_coherent_format(lower_levels,upper_levels,jvalues,wavelengths,avalues,loggf,wavenumbers,elementcode,csfs):
    num_trans = len(wavelengths)
    f = open('test_coherent_formatted_adf04_element' + str(elementcode),'w')
    labels = make_level_labels(csf_strings=csfs)
    file =  open('test.csv', 'w', newline='')

    format_string = 'F12.4,1X,F12.4,1X,e12.2,F6.2,1X,I2,F12.3,F5.1,A10,1X,I2,F12.3,F5.1,A10'
    line = ff.FortranRecordWriter(format_string)

    level_truncate = num_trans
    print("outputting the first ",level_truncate," lines")
    for iter in range(0,level_truncate):
        lower_index = lower_levels[iter]-1
        upper_index = upper_levels[iter]-1

        if wavelengths[iter] > 1e5:

            array = [wavelengths[iter],wavenumbers[upper_index]-wavenumbers[lower_index],avalues[iter],elementcode,lower_index,wavenumbers[lower_index],jvalues[lower_index],labels[lower_index],upper_index,wavenumbers[upper_index],jvalues[lower_index],labels[upper_index]] 


            print(line.write(array))
        #f.write(line.write(array))
        #f.write("\n")wa
        #print(wavelengths[iter])

    return 0