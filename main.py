def fit_linear(filename):
    data_list = []
    check_input_type = rows_or_columns(filename)
    if check_input_type == 'columns':
        data_list = column_function(filename)
        if data_list == 'length Error':
            return "Input file error: Data lists are not the same length."
        if data_list == 'zero division Error':
            return "Input file error: Not all uncertainties are positive."
    if check_input_type == 'rows':
        data_list = rows_function(filename)
        if data_list == 'length Error':
            return "Input file error: Data lists are not the same length."
        if data_list == 'zero division Error':
            return "Input file error: Not all uncertainties are positive."
    a = find_a(data_list)
    b = find_b(data_list, a)
    chi_squared = find_chi_squared(data_list)
    chi_squared_reduced = find_chi_reduced(data_list)
    da = find_da(data_list)
    db = find_db(data_list)
    print('a =', a, '+-', da)
    print('b =', b, '+-', db)
    print('chi2 =', chi_squared)
    print('chi2_reduced =', chi_squared_reduced)


def rows_or_columns(input_file):  # this function check what kind
    # of input we get
    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()
    if len((input_data[0].split())) == 4:
        return 'columns'
    else:
        return 'rows'


def column_function(input_file):  # This function reads an input file arranged in columns
    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()  # Now we read the file
    data_list = []  # rearrange data

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

    for argument in range(0, len(data_list[0])):  # formatting
        lower_argument = data_list[0][argument].lower()
        data_list[0].remove(data_list[0][argument])
        data_list[0].insert(argument, lower_argument)

    for argument in range(0, len(data_list[0])):  # checking if all uncertainties are higher than zero
        if data_list[0][argument] == 'dx' or data_list[0][argument] == 'dy':
            for uncertainty in data_list[1:data_points]:
                if uncertainty[argument] <= 0.0:
                    return 'zero division Error'

    fixed_list = []  # now we make sure the data is arranged as x,dx,y,dy
    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'x':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            fixed_list.append (temp_list)
    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'dx':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            fixed_list.append(temp_list)
    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'y':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            fixed_list.append(temp_list)
    for argument in range(0, 4):
        temp_list = []
        if data_list[0][argument] == 'dy':
            for point in range(0, data_points):
                temp_list.append(data_list[point][argument])
            fixed_list.append(temp_list)
    return fixed_list


def rows_function(input_file):  # this function reads an input file arranged in rows
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

    fixed_list = []  # now we make sure the data is arranged as x,dx,y,dy
    for argument in data_list[:4]:
        if argument[0] == 'x':
            fixed_list.append(argument)
    for argument in data_list[:4]:
        if argument[0] == 'dx':
            fixed_list.append(argument)
    for argument in data_list[:4]:
        if argument[0] == 'y':
            fixed_list.append(argument)
    for argument in data_list[:4]:
        if argument[0] == 'dy':
            fixed_list.append(argument)
    fixed_list.append(data_list[4:])

    return fixed_list


def find_a(input_list):  # here we calculate parameter a
    xy_list = ['xy']
    x_squared_list = ['x squared']
    x = input_list[0]
    y = input_list[2]
    for i in range (1,len(x)):
        xy_list.append ((x[i])*(y[i]))
        x_squared_list.append (((x[i])**2))
    xy_avg = calculate_average(xy_list, input_list)
    x_avg = calculate_average(x,input_list)
    y_avg = calculate_average(y,input_list)
    x_squared_avg = calculate_average(x_squared_list, input_list)
    parameter_a = ((xy_avg - (x_avg * y_avg))/(x_squared_avg - (x_avg ** 2)))
    return parameter_a


def find_da(input_list):  # here we calculate the uncertainty of parameter a
    x_squared_list = ['x squared']
    x = input_list[0]
    dy = input_list[3]
    dy_squared_list = ['dy squared']
    number_of_points = len(x)-1
    for i in range(1, len(x)):
        x_squared_list.append(((x[i]) ** 2))
        dy_squared_list.append(((dy[i])**2))
    avg_dy_squared = calculate_average(dy_squared_list, input_list)
    avg_x_squared = calculate_average(x_squared_list, input_list)
    avg_x = calculate_average(x, input_list)
    da_squared = avg_dy_squared/(number_of_points*(avg_x_squared-(avg_x**2)))
    da = da_squared**0.5
    return da


def find_db (input_list):  # here we calculate the uncertainty of parameter b
    x_squared_list = ['x squared']
    x = input_list[0]
    dy = input_list[3]
    dy_squared_list = ['dy squared']
    number_of_points = len(x)-1
    for i in range(1, len(x)):
        x_squared_list.append(((x[i]) ** 2))
        dy_squared_list.append(((dy[i])**2))
    avg_dy_squared = calculate_average(dy_squared_list, input_list)
    avg_x_squared = calculate_average(x_squared_list, input_list)
    avg_x = calculate_average(x, input_list)
    db_squared = (avg_dy_squared*avg_x_squared)/(number_of_points*(avg_x_squared-(avg_x**2)))
    db = db_squared ** 0.5
    return db


def find_b(input_list, a):  # here we calculate parameter b
    y = input_list[2]
    x = input_list[0]
    y_avg = calculate_average(y, input_list)
    x_avg = calculate_average(x, input_list)
    b = y_avg - a*x_avg
    return b


def calculate_average (z_list, input_list):  # here we calculate the z average
    dy = input_list[3]
    numerator = 0
    denominator = 0
    for i in range(1,len(dy)):
        numerator += (z_list[i]/((dy[i])**2))
        denominator += (1/((dy[i])**2))
    z_avg = numerator/denominator
    return z_avg


def find_chi_squared(data_list):  # here we calculate chi squared reduced
    chi_squared = 0
    x = data_list[0]
    y = data_list[2]
    dy = data_list[3]
    a = find_a(data_list)
    b = find_b(data_list, a)
    da = find_da(data_list)
    db = find_db(data_list)
    for i in range(1, len(x)):
        chi_squared += (((float(y[i])-((a*x[i])+b))/(float(dy[i]))) ** 2)
    return chi_squared


def find_chi_reduced (data_list):
    x = data_list[0]
    points_amount = len(x)-1
    chi_squared = find_chi_squared(data_list)
    chi_squared_reduced = (chi_squared/(points_amount-2))
    return chi_squared_reduced


print(fit_linear('Err_data_len.txt'))

