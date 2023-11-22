import numpy as np
OSCILLATOR_CONVERSION_CONST = 6.67025177e13 #This number is from Drake's handbook on atomic physics, more precision possibly needed?

def calculate_wavelengths_and_transition_energies(wavenumbers,upper_levels,lower_levels):
    num1 = len(upper_levels)
    num2 = len(lower_levels)
    
    assert(num1==num2),"disparity in number of upper and lower levels, stopping."
    wavelengths = np.zeros(num1)
    transition_energies = np.zeros(num1)
    for jj in range(num1):
        upper_levels_index = upper_levels[jj]-1
        lower_levels_index = lower_levels[jj]-1
        transition_energies[jj] = wavenumbers[upper_levels_index] - wavenumbers[lower_levels_index]
    wavelengths = np.power(transition_energies,-1)*10_000_000

    return wavelengths,transition_energies

def calculate_oscillator_strengths(a_values_float,wavelengths,total_j_for_each_level,upper_levels,lower_levels):
    num = len(a_values_float)
    num2 = len(upper_levels)
    num3 = len(lower_levels)

    assert(num2 == num3),"num of upper levels is not the same as num of lower levels, stopping"
    assert(num == num2),'number of a values is not the same as number of transitions, stopping'

    loggf = np.zeros(num)
    upper_weights = np.zeros(num)
    lower_weights = np.zeros(num)

    new_a_values = a_values_float.copy()

    for ii in range(0,num):
        upper_weights[ii] = 2.0 * total_j_for_each_level[upper_levels[ii]-1] + 1.0
        lower_weights[ii] = 2.0 * total_j_for_each_level[lower_levels[ii]-1] + 1.0
        if new_a_values[ii] == 0.0:
            new_a_values[ii] = 1.0e-30
            #print('help')

    weighted_transition_strength = upper_weights*wavelengths*wavelengths*new_a_values/OSCILLATOR_CONVERSION_CONST 
    absolute_transition_strength = weighted_transition_strength / lower_weights


    #print(weighted_transition_strength)
    loggf = np.log10(weighted_transition_strength)
    return loggf,absolute_transition_strength

