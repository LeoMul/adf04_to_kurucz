Usage: 

python3 "path_to"/adf04_to_kurucz.py -f "path_to_adf04_file"

the code reads the adf04 file, outputs the data in Kurucz format. It converts the A values to log(gf), 
and retains (most of) the level labels in the adf04 file.

since CARSUS expects the wavelengths in fortran F11.4 format, it automatically rejects any wavelength that cannot be stored in this format.



the additional optional arguments:
     -r '0 or 1' tells the code to either accept or reject bad A values from the adf04 file (i.e the default value of 1e-30). 0 is on by default.
     -n 'n' specifies number of lines wanted, by default it prints all (except those rejected on wavelength or a value grounds if specified.)

current dependencies: 
    fortranformat (I will eventually remove this as i had an output subroutine that worked without it - but this is more convenient.)
    numpy (I challenge you, user, to find a python program for scientific purposes that does not have this)
    re (for string manipulation)
    argparse (for the easy command line interface )