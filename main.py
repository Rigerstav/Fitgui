def fit_linear(filename):
    
    data_dict = {}
    check_input_type = rows_or_columns(filename)  # here we check what kind of input we get
    if check_input_type == 'columns':
        data_dict = column_function(filename)

        if data_dict == 'length Error':
            return "Input file error: Data lists are not the same length."

        if data_dict == 'zero division Error':
            return "Input file error: Not all uncertainties are positive."

    if check_input_type == 'rows':
        data_dict = rows_function(filename)

        if data_dict == 'length Error':
            return "Input file error: Data lists are not the same length."

        if data_dict == 'zero division Error':
            return "Input file error: Not all uncertainties are positive."

    a = find_a(data_dict)
    b = find_b(data_dict, a)
    chi_squared = find_chi_squared(data_dict)
    chi_squared_reduced = find_chi_reduced(data_dict)
    da = find_da(data_dict)
    db = find_db(data_dict)
    print('a =', a, '+-', da)
    print('b =', b, '+-', db)
    print('chi2 =', chi_squared)
    print('chi2_reduced =', chi_squared_reduced)
    plot_linear(a, b, data_dict)


def rows_or_columns(input_file):
    # this function check what kind
    # of input we get

    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()
    if len((input_data[0].split())) == 4:
        return 'columns'
    else:
        return 'rows'


def column_function(input_file):
    # This function reads an input file arranged in columns
    # It will return an organized data file

    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()  # Now we read the file
    data_list = []  # rearrange data
    data_points = 0
    for row in input_data:
        split_row = row.split()
        data_list.append(split_row)

    for row in range(1, len(data_list)):  # check how many measure points we have
        if len(data_list[row]) == 0:
            data_points = row
            break
        if data_list[row][0] == 'x' or data_list[row][0] == 'y':
            data_points = data_list[row]
            break

    for row in range(1, data_points):
        if len(data_list[row]) != 4:  # check length of data. Should be 4 due to X, dX, Y, dY
            return "length Error"

    for row in data_list[1:data_points]:  # convert numbers to float
        for number in range(0, 4):
            float_number = float(row[number])
            row.insert(number, float_number)
            row.remove(row[number+1])

    for argument in range(0, len(data_list[0])):  # here we change all the strings to lowercases
        lower_argument = data_list[0][argument].lower()
        data_list[0].remove(data_list[0][argument])
        data_list[0].insert(argument, lower_argument)

    for argument in range(0, len(data_list[0])):  # checking if all uncertainties are higher than zero
        if data_list[0][argument] == 'dx' or data_list[0][argument] == 'dy':
            for uncertainty in data_list[1:data_points]:
                if uncertainty[argument] <= 0.0:
                    return 'zero division Error'

    data_dict = {}  # here we sort the data in a dictionary
    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'x':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            data_dict['x'] = temp_list[1:]

    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'dx':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            data_dict['dx'] = temp_list[1:]

    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'y':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            data_dict['y'] = temp_list[1:]

    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'dy':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            data_dict['dy'] = temp_list[1:]

    for argument in range(-2, 0, 1):  # for regular input, this will be the index for the axis
        if data_list[argument][0] == 'x':
            data_dict['x axis'] = data_list[argument][2:]

        if data_list[argument][0] == 'y':
            data_dict['y axis'] = data_list[argument][2:]

    return data_dict


def rows_function(input_file):
    # this function reads an input file arranged in rows
    # It will return an organized data file

    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()  # Now we read the file
    data_list = []  # rearrange data

    for row in input_data:
        split_row = row.split()
        data_list.append(split_row)

    for argument in range(0, 3):  # here we check if every argument has the same amount of points
        if len(data_list[argument]) != len(data_list[argument+1]):
            return 'length Error'

    for argument in data_list[0:4]:  # now we change all points to floats
        for number in range(1, len(argument)):
            float_number = float(argument[number])
            argument.insert(number, float_number)
            argument.remove(argument[number+1])

    for argument in data_list[0:4]:  # now we check that all uncertainties are positive
        if argument[0] == 'dx' or argument[0] == 'dy':
            for uncertainty in argument[1:]:
                if uncertainty <= 0.0:
                    return 'zero division Error'

    for argument in data_list[0:4]:
        lower_argument = argument[0].lower()
        argument.remove(argument[0])
        argument.insert(0, lower_argument)

    data_dict = {}  # here we sort the data in a dictionary
    for argument in data_list[:4]:
        if argument[0] == 'x':
            data_dict['x'] = argument[1:]

    for argument in data_list[:4]:
        if argument[0] == 'dx':
            data_dict['dx'] = argument[1:]

    for argument in data_list[:4]:
        if argument[0] == 'y':
            data_dict['y'] = argument[1:]

    for argument in data_list[:4]:
        if argument[0] == 'dy':
            data_dict['dy'] = argument[1:]

    for argument in range(-2, 0, 1):  # here we check if this is regular or bonus input
        if data_list[argument][0] == 'b':  # for a bonus input, this will be the index for the axis
            for index in range(-5, -3, 1):
                if data_list[index][0] == 'x':
                    data_dict['x axis'] = data_list[index][2:]
                if data_list[index][0] == 'y':
                    data_dict['y axis'] = data_list[index][2:]

            float_list = []
            for number in data_list[argument][1:]:
                float_list.append(float(number))
            data_dict['b'] = float_list

        if data_list[argument][0] == 'a':
            float_list = []
            for number in data_list[argument][1:]:
                float_list.append(float(number))
            data_dict['a'] = float_list

        if data_list[argument][0] == 'x':  # for regular input, this will be the index for the axis
            data_dict['x axis'] = data_list[argument][2:]

        if data_list[argument][0] == 'y':
            data_dict['y axis'] = data_list[argument][2:]

    return data_dict


def calculate_average(z_list, input_dict):  # here we calculate the z average ("roof")
    dy = input_dict['dy']
    numerator = 0
    denominator = 0
    for i in range(0, len(dy)):
        numerator += (z_list[i]/((dy[i])**2))
        denominator += (1/((dy[i])**2))
    z_avg = numerator/denominator
    return z_avg


def find_a(input_dict):
    # here we calculate parameter a

    xy_list = []
    x_squared_list = []
    x = input_dict['x']
    y = input_dict['y']

    for i in range(0, len(x)):  # here we create input for 'calculate average'
        xy_list.append((x[i])*(y[i]))
        x_squared_list.append(((x[i])**2))

    xy_avg = calculate_average(xy_list, input_dict)
    x_avg = calculate_average(x, input_dict)
    y_avg = calculate_average(y, input_dict)
    x_squared_avg = calculate_average(x_squared_list, input_dict)
    parameter_a = ((xy_avg - (x_avg * y_avg))/(x_squared_avg - (x_avg ** 2)))
    return parameter_a


def find_da(input_dict):
    # here we calculate the uncertainty of parameter a

    x_squared_list = []
    x = input_dict['x']
    dy = input_dict['dy']
    dy_squared_list = []
    number_of_points = len(x)

    for i in range(0, len(x)):  # here we create input for 'calculate average'
        x_squared_list.append(((x[i]) ** 2))
        dy_squared_list.append(((dy[i])**2))

    avg_dy_squared = calculate_average(dy_squared_list, input_dict)
    avg_x_squared = calculate_average(x_squared_list, input_dict)
    avg_x = calculate_average(x, input_dict)
    da_squared = avg_dy_squared/(number_of_points*(avg_x_squared-(avg_x**2)))
    da = da_squared**0.5
    return da


def find_db(input_dict):
    # here we calculate the uncertainty of parameter b

    x_squared_list = []
    x = input_dict['x']
    dy = input_dict['dy']
    dy_squared_list = []
    number_of_points = len(x)

    for i in range(0, len(x)):  # here we create input for 'calculate average'
        x_squared_list.append(((x[i]) ** 2))
        dy_squared_list.append(((dy[i])**2))

    avg_dy_squared = calculate_average(dy_squared_list, input_dict)
    avg_x_squared = calculate_average(x_squared_list, input_dict)
    avg_x = calculate_average(x, input_dict)
    db_squared = (avg_dy_squared*avg_x_squared)/(number_of_points*(avg_x_squared-(avg_x**2)))
    db = db_squared ** 0.5
    return db


def find_b(input_dict, a):  # here we calculate parameter b
    y = input_dict['y']
    x = input_dict['x']
    y_avg = calculate_average(y, input_dict)
    x_avg = calculate_average(x, input_dict)
    b = y_avg - a*x_avg
    return b


def find_chi_squared(data_dict):  # here we calculate chi squared
    chi_squared = 0
    x = data_dict['x']
    y = data_dict['y']
    dy = data_dict['dy']
    a = find_a(data_dict)
    b = find_b(data_dict, a)

    for i in range(0, len(x)):
        chi_squared += (((float(y[i])-((a*x[i])+b))/(float(dy[i]))) ** 2)

    return chi_squared


def find_chi_reduced(data_dict):  # here we calculate chi squared reduced
    n = data_dict['x']
    points_amount = len(n)
    chi_squared = find_chi_squared(data_dict)
    chi_squared_reduced = (chi_squared/(points_amount-2))
    return chi_squared_reduced


def plot_linear(a, b, data_dict):  # this function create and save the plot
    import matplotlib.pyplot as plt
    import numpy as np
    x_axis = data_dict['x axis']
    y_axis = data_dict['y axis']
    x_points = data_dict['x']
    y_points = data_dict['y']
    dx = data_dict['dx']
    dy = data_dict['dy']
    plt.xlabel('{} {}'.format(x_axis[0], x_axis[1]))
    plt.ylabel('{} {}'.format(y_axis[0], y_axis[1]))
    min_x = min(x_points)
    max_x = max(x_points)
    t = np.arange(min_x, max_x+0.2, 0.2)  # here we create points for the linear fit
    fit_line = a*t + b
    plt.plot(t, fit_line, 'r')
    plt.errorbar(x_points, y_points, xerr=dx, yerr=dy, fmt='b+')
    plt.savefig("linear_fit.svg", format="svg")
    return plt.show()


# bonus section #

def search_best_parameter(filename):
    data_dict = {}
    check_input_type = rows_or_columns(filename)  # here we check what kind of input we get
    if check_input_type == 'columns':
        data_dict = column_function(filename)

        if data_dict == 'length Error':
            return "Input file error: Data lists are not the same length."

        if data_dict == 'zero division Error':
            return "Input file error: Not all uncertainties are positive."

    if check_input_type == 'rows':
        data_dict = rows_function(filename)

        if data_dict == 'length Error':
            return "Input file error: Data lists are not the same length."

        if data_dict == 'zero division Error':
            return "Input file error: Not all uncertainties are positive."

    chi_squared_initial = bonus_find_chi(data_dict, data_dict['a'][0], data_dict['b'][0])
    numeric_fit = bonus_numeric_search_for_chi(chi_squared_initial, data_dict)
    chi_squared = numeric_fit[0]
    best_a = numeric_fit[1]
    best_b = numeric_fit[2]
    chi_squared_reduced = bonus_find_chi_reduced(len(data_dict['x']), chi_squared)
    a_points = numeric_fit[3]
    da = data_dict['a'][2]
    db = data_dict['b'][2]

    print('a =', best_a, '+-', da)
    print('b =', best_b, '+-', db)
    print('chi2 =', chi_squared)
    print('chi2_reduced =', chi_squared_reduced)
    plot_linear(best_a, best_b, data_dict)
    bonus_plot_chi(best_b, a_points, data_dict)


def bonus_find_chi(data_dict, a, b):  # here we calculate chi for numeric fit
    chi_squared = 0
    x = data_dict['x']
    dx = data_dict['dx']
    y = data_dict['y']
    dy = data_dict['dy']
    for i in range(0, len(x)):
        chi_squared += (((float(y[i])-((a*x[i])+b))/(((float(dy[i])) ** 2)
                         + ((a*(x[i]+dx[i])) - (a*(x[i]-dx[i]))) ** 2) ** 0.5) ** 2)
    return chi_squared


def bonus_numeric_search_for_chi(chi_squared, data_dict):  # this function numerically search for chi
    best_a = data_dict['a'][0]
    best_b = data_dict['b'][0]
    a_points = np.arange(data_dict['a'][0], data_dict['a'][1], data_dict['a'][2])
    b_points = np.arange(data_dict['b'][0], data_dict['b'][1], data_dict['b'][2])
    for a in a_points:
        for b in b_points:
            find_chi = bonus_find_chi(data_dict, a, b)
            if find_chi < chi_squared:
                chi_squared = find_chi
                best_a = a
                best_b = b
    return chi_squared, best_a, best_b, a_points


def bonus_find_chi_reduced(n, chi):  # here we normalize chi squared
    chi_squared_reduced = (chi/(n-2))
    return chi_squared_reduced


def bonus_plot_chi(best_b, a_points, data_dict):  # this function plots chi as a function of a
    import matplotlib.pyplot as plt
    import numpy as np
    x_axis = 'a'
    y_axis = 'chi2(b = {0:.1f})'.format(best_b)
    x_points = a_points
    y_points = []
    for i in x_points:
        chi = bonus_find_chi(data_dict, i, best_b)
        y_points.append(chi)

    plt.xlabel('{}'.format(x_axis))
    plt.ylabel('{}'.format(y_axis))
    plt.plot(x_points, y_points, 'b')
    plt.savefig("numeric_sampling.svg", format="svg")

    return plt.show()


