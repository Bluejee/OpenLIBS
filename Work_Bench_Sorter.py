"""

This program aims to take in a CSV file named workbench in the Element_Database directory containing the persistent
lines of an element and sort them and create a new CSV file named after the element.

The program flow can be described as :
1. Ask the user to give in the name of the element.
2. Run the workbench through a sorter.
3. create a new CSV file.

"""

import numpy as np

print('Hey there!, Welcome.')
element = input('Enter the name of the Element :: ')

data = np.genfromtxt('Element_Database/Workbench.csv', delimiter=',')

# Converting from Angstrom to nm
for i in range(len(data)):
    data[i] = data[i]/10

data.view('f8,f8,f8').sort(order=['f0'], axis=0)

np.savetxt('Element_Database/'+element + '.csv', data, delimiter=',')
