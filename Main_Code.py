'''
This program aims to take in a CSV file of a LIBS spectrum as an input. and then predict the elements present in the
sample from which the spectrum was taken.

The program flow can be described as :
1. Ask the user to give in the spectrum of the sample.
2. Run the spectrum through a peak analysing system in order to find the peaks.
3. compare the peaks with the existing NIST database in order to check the presence of each element.
4. If the criteria is satisfied  Return a list of elements present in the sample.

'''