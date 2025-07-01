import numpy as np

def read_dat(path_to_dat):
    # Open the .dat file in read mode
    with open(path_to_dat, "r") as file:
        # Read all lines into a list
        lines = file.readlines()

    # Initialize lists to store the data
    y_cen = []
    y_span = []
    chord = []
    time = []
    cl_values = []

    # Flag to determine when to start reading Cl values
    read_time = False
    read_y = False
    k = 0
    # Process each line
    for line in lines:
        # Skip commented lines
        if line.startswith("#"):
            if " t ," in line:
                # Set the flag to start reading Cl values
                read_time = True
                continue
            elif "y_cen , y_span, chord" in line:
                read_y = True
                continue
            else:
                pass
        # Split the line into values
        values = line.split()
        if read_time:
            # Extract time and Cl values
            time.append(float(values[0]))
            cl_values.append([float(cl) for cl in values[1:]])
        if read_y:
            if k == 0:
                y_cen.append([float(y_cen) for y_cen in values[:]])
                k += 1
            elif k ==1:
                y_span.append([float(y_span) for y_span in values[:]])
                k += 1
            elif k == 2:
                chord.append([float(chord) for chord in values[:]])
                read_y = False
    # Convert lists to NumPy arrays
    y_cen = np.array(y_cen)
    y_span = np.array(y_span)
    chord = np.array(chord)
    time = np.array(time)
    cl_values = np.array(cl_values)
    
    return y_cen, y_span, chord, time, cl_values

def extract_n_column_from_file(filename,n):
    column = []

    with open(filename, 'r') as file:
        for line in file:
            # Split the line into columns
            columns = line.split()
            # Check if the second column can be converted to a float
            if len(columns) > n-1:
                try:
                    # Convert the second column value to float and add to the list
                    column.append(float(columns[n-1]))
                except ValueError:
                    # Skip lines where the second column is not a number
                    continue

    return column
