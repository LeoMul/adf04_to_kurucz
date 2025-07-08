import numpy as np

BOLTZMAN_EV = 8.6173303e-5


def get_angular_letter(total_l_string):
    #translates L into the coresponding symbol.
    total_l = int(total_l_string)

    angular_dictionary = ['S','P','D','F','G','H']
    
    num = len(angular_dictionary)-1
    if total_l > num:
        return str(total_l)
    else:
        return angular_dictionary[total_l]

def convert_a_value_string_to_float(a_value_string):
    #print(a_value_string)

    array = [*a_value_string]
    array.remove('.')
    #this converts the hilariously outdated float format in adf04 files into an actual number

    #print(array)
    a_value_float = float(array[0]) + float(array[1])*0.1 + float(array[2])*0.01

    exponent = int(float(array[-2])*10 + float(array[-1]))
    #print(exponent)
    #it could be made more efficient if i could be bothered.
    if array[-3] == '+':
        a_value_float*= (10**exponent)
    elif array[-3] == '-':
        a_value_float *=(10**(-exponent))
    else:
        print('failure in a value conversion')
    return a_value_float

def convert_many_a_values(avalue_string_array):
    num = len(avalue_string_array)
    a_values = np.zeros(num)

    for jj in range(0,num):
        a_values[jj] = convert_a_value_string_to_float(a_value_string=avalue_string_array[jj])
    return a_values

def convert_upsilons(upsilon_string_array):
    shape = np.shape(upsilon_string_array)
    ups = np.zeros(shape)
    for ii in range(0,shape[0]):
        for jj in range(0,shape[1]):
            ups[ii,jj] = convert_a_value_string_to_float(upsilon_string_array[ii,jj])
    return ups

def get_transition_data(num_levels,path,max_level):
    print("Attempting to find transition data")
    num_transitions = int(num_levels * (num_levels-1)/2)
    print(num_transitions)
    if max_level!=-1:
        num_transitions = int(max_level * (max_level-1)/2)
        
    transition_data = np.loadtxt(path,skiprows=num_levels+3,dtype=str,usecols=[0,1,2],max_rows=num_transitions)

    #it is possible i may need to add an expection here if it doesnt find the expected number of transitions
    print("Expecting ",num_transitions," transitions")
    upper_levels = transition_data[:,0].astype(int)
    lower_levels = transition_data[:,1].astype(int)
    
    for ii in range(0,len(upper_levels)):
        if (upper_levels[ii] < lower_levels [ii]):
            u = upper_levels[ii]
            l = lower_levels[ii]
            upper_levels[ii] = l 
            lower_levels[ii] = u
    
    a_values_string_array = transition_data[:,2]
    print("found ",len(a_values_string_array),' transitions')


    num_transitions = len(a_values_string_array)
    a_values_float = convert_many_a_values(avalue_string_array=a_values_string_array)
    print("transition data found successfully")    
    print("-------------------------")

    return a_values_float,upper_levels,lower_levels,num_transitions

def get_all_transition_data_inc_upsilons(num_levels,path):
    print("Attempting to find transition data")
    num_transitions = int(num_levels * (num_levels-1)/2)
    temperatures = np.loadtxt(path,skiprows=num_levels+2,dtype=str,max_rows=1)

    transition_data = np.loadtxt(path,skiprows=num_levels+3,dtype=str,max_rows=num_transitions,usecols=(0,1,2))

    temperatures = convert_many_a_values(temperatures[2:])

    #upsilons = transition_data[:,3:-1]

    upsilons = np.empty([num_transitions,len(temperatures)],dtype=object)

    adf04_file = open(path,'r')
    adf04_file_read = adf04_file.readlines()
    skiprows = num_levels + 3 
    for ii in range(0,num_transitions):
        current_line = adf04_file_read[ii + skiprows].replace('\n','')[0:-8]
        current_line = current_line.split()
        #print(current_line)
        this_upsilon = current_line[3:]
        upsilons[ii,:] = np.array(this_upsilon,dtype=str)
        #print(this_upsilon)
        #print(upsilons[ii,:])
    #print(upsilons[1,:])
    upsilons = convert_upsilons(upsilons)
    #it is possible i may need to add an expection here if it doesnt find the expected number of transitions
    print("Expecting ",num_transitions," transitions")
    upper_levels = transition_data[:,0].astype(int)
    lower_levels = transition_data[:,1].astype(int)
    for ii in range(0,len(upper_levels)):
        if (upper_levels[ii] < lower_levels [ii]):
            u = upper_levels[ii]
            l = lower_levels[ii]
            upper_levels[ii] = l 
            lower_levels[ii] = u
            
    a_values_string_array = transition_data[:,2]
    print("found ",len(a_values_string_array),' transitions')


    num_transitions = len(a_values_string_array)
    a_values_float = convert_many_a_values(avalue_string_array=a_values_string_array)
    print("transition data found successfully")    
    print("-------------------------")

    return a_values_float,upper_levels,lower_levels,temperatures,upsilons,num_transitions

def process_term_strings_and_j_values(term_L_S,term_J,num_levels):
    term_strings = []

    jvalues = np.zeros(num_levels)
    for ii in range(0,num_levels):
        current_first_string = term_L_S[ii]
        m = current_first_string[1]
        try:
            total_l = current_first_string[3]
        except:
            total_l = '0'
            
        jtot = term_J[ii].strip(')') 
        try:
            jvalues[ii] = float(jtot)
        except:
            jvalues[ii] = 0.0
        L_string = get_angular_letter(total_l)
        new_term_string = m + L_string + jtot
        term_strings.append(new_term_string)
    return term_strings,jvalues
    
def get_level_and_term_data(path,num_levels):
    print("Attempting to find term data")
    
    #level_data = np.loadtxt(path,skiprows=1,max_rows=num_levels,dtype = str)
    ##the adf04 format seems to split these in two, so i parse them seperately.
    #term_L_S = level_data[:,2]
    #term_J = level_data[:,3]
    #csfs_strings = level_data[:,1]
    #level_numbers = level_data[:,0].astype(int)
    #energy_levels_cm_minus_one = level_data[:,4].astype(float)

    
    # big clean up on Tuesday 8th July 2025 
    
    term_L_S = np.empty(num_levels,dtype='<U5')
    term_J = np.empty(num_levels,dtype='<U5')
    csfs_strings = np.empty(num_levels,dtype='<U35')
    level_numbers = np.zeros(num_levels,dtype=int)
    energy_levels_cm_minus_one = np.zeros(num_levels,dtype=float)
    
    adf04_file = open(path,'r')
    adf04_file.readline()
    
    import re
    
    for ii in range(0,num_levels):
        string = adf04_file.readline()
        string_split = string.split()
        
        
        level_num = int(string_split[0])
        e_cm = float(string_split[-1])
        config_string = find_between(string,str(level_num),'(').replace(' ','')

        for jj in range(0,len(string)):
            if string[jj] == '(':
                break 
        ls_pos = jj 
        for jj in range(len(string)-1,0,-1):
            if string[jj] == ')':
                break
        j_pos = jj 
        
        #print(string[j_pos-4:j_pos+1])
        
        term_J[ii] = string[j_pos-4:j_pos+1]
        term_L_S[ii] = string[ls_pos:ls_pos+5]
        level_numbers[ii] = level_num
        energy_levels_cm_minus_one[ii] = e_cm
        csfs_strings[ii] = config_string
        print(term_L_S[ii],string[ls_pos:ls_pos+5])
    

    #needs to be 4 as the adf04 puts 3D4 to 3D 4 - maybe by changing delimiter we can avoid this
    
    term_strings,jvalues = process_term_strings_and_j_values(term_L_S,term_J,num_levels)

    print("term data found, probably")
    print("-------------------------")

    return csfs_strings,term_strings,jvalues,energy_levels_cm_minus_one

def find_between( s, first, last ):
###https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def read_in_initial(path):
    f = open(path,'r')
    first_line = f.readline()

    print(first_line)


    new_stuff = first_line[0:5].replace("+"," ").split()

    other_stuff = first_line[5:].split()
    print(other_stuff)
    extracting_ion_pot =  other_stuff[-1].split('.')
    ion_pot = float(extracting_ion_pot[0])
    #print(ion_pot)
    atomic_symbol = new_stuff[0]

    effective_charge = new_stuff[1]
    atomic_number = other_stuff[0]

    effective_charge_int = int(effective_charge[0])

    #effective_charge_for_element_code = str(effective_charge_int)
    #if effective_charge_int < 10:
    #    effective_charge_for_element_code = '0'+effective_charge_for_element_code

    #will fail for charges higher than 10 with current string manipulation


    print("Found atomic symbol ",atomic_symbol)
    print("Found atomic number",atomic_number)
    print("Found ionisation ",effective_charge)

    elementcode = int(atomic_number) + effective_charge_int/100
    print("Element code for TARDIS ",elementcode)
    print("-------------------------")

    checker = False 
    level_counter = 0
    while checker == False:
        current_line = f.readline()

        string_to_be_checked = current_line.strip()[0] 
        target_string = '-'
        if string_to_be_checked == target_string:
            checker = True
        else:
            level_counter += 1
     
    print("found ",level_counter," levels")
    f.close()
    return elementcode,level_counter,ion_pot
    
def write_out_levels_get_temps(path,level_counter,new_path):
    f_new = open(new_path,'w')
    f_old = open(path,'r')

    f_old_read = f_old.readlines()

    for jj in range(0,level_counter+3):
        f_new.write(f_old_read[jj])

    temps = f_old_read[level_counter+2].split()[2:]

    temps = convert_many_a_values(temps)
    #print(temps)    
    temps = np.array(temps)
    f_new.close()
    f_old.close()

    return temps

