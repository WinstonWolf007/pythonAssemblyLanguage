from error import display


"""

Replace function is used to replace the variable box for real value

[table:idx] -> codeLine = data[table][idx]

"""


def replace(i, j, values, data):
    if '[' in i and ']' in i:
        # get table, idx
        info = i.replace('[', '').replace(']', '').strip().split(':')

        # get the ascii value (9) -> TABS
        if len(info) == 2:
            table, idx = info

            # for upt function (operation)
            if i[0] in ['+', '-', '*', '/']:
                if table.replace(i[0], '') in data:
                    values[j] = str(i[0]) + str(data[table.replace(i[0], '').strip()][int(idx.strip())])
            else:
                if table in data:
                    values[j] = data[table.strip()][int(idx.strip())]

        # get the ascii code of ascii (9) -> 57
        elif len(info) == 4 and info[2] == '<str>':
            table, idx, val, idxStr = info
            values[j] = ord(str(data[table.strip()][int(idx.strip())])[int(idxStr)])

    # return the new data value
    return values


"""

The exe function is used for executed the code

"""


def exe(code_line, all_function, data):
    functionName = code_line[0].replace('&', '').replace('%', '')

    # get the parameter of function -> &put <get this>
    values = [x.strip() for x in " ".join(code_line[1:]).strip().split(',')]

    # replace var name per data value
    for j, i in enumerate(values):
        values = replace(i, j, values, data)

    # call python function in dict (file: main.py / var func)
    if functionName in all_function:
        v = all_function.get(functionName)(values)
        return v if v else None
    else:
        return values
