def rows_or_columns(input_file):  # this function check what kind
    # of input we get
    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()
    if len((input_data[0].split())) == 4:
        return "columns"
    else:
        return "rows"


# print (rows_or_columns("Col_input.txt"))
# def

# This function reads the input file
def input_file_function(input_file):
    file_pointer = open(input_file, 'r')
    input_data = file_pointer.readlines()  # Now we read the file
    my_list = []  # rearrange data
    for row in input_data:
        split_row = row.split()
        my_list.append(split_row)
    for row in range(1, len(my_list)):  # check how many measure points we have
        if len(my_list[row]) == 0:
            data_points = row
            break
        if my_list[row][0] == 'x' or my_list[row][0] == 'y':
            data_points = my_list[row]
            break
    for row in range(1, data_points):
        if len(my_list[row]) != 4:  # check length of data. Should be 4 due to X, dX, Y, dY
            return "Input file error: Data lists are not the same length."
    for row in my_list[1:data_points]:  # convert numbers to float
        for number in range(0, 4):
            float_number = float(row[number])
            row.insert(number, float_number)
            row.remove(row[number+1])

            # if

    #  for row in input_data:
    #    if len(row)!=len(row)+1:
    #           return (print ("Input file error: Data lists are not the same length."))

    return my_list


print(input_file_function('Err_data_len.txt'))
