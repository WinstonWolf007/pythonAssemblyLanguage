from main2 import *
from main3 import *


# func name selection
func = {
    'rgt': rgt,
    'def': def_,
    'lk': lk,
    'upt': upt,
    'put': put,
    'del': del_,
    'call': call,
    'get': get,
    'if': if_,
    'loop': loop
}

# read each line in file
with open("../PAL file/script.bs", 'r+') as file:
    infoFIle['lineNbr'] = 0
    infoFIle['lineCode'] = ''

    for line in file:
        # if error, send line number to user
        infoFIle['lineNbr'] += 1
        infoFIle['lineCode'] = line

        # delete comment
        if ';' in line:
            line = line.split(';')[0]

        # put False if it ends function
        if line.strip().replace('\n', '') == '&endf':
            inFunc = [None, False]

        # don't exe code if empty
        elif line.strip().replace('\n', '') == '':
            pass

        # append code in function data if True
        elif inFunc[1] is True:
            funcCode[inFunc[0]].append(line.replace('\n', '').strip().split(" "))

        else:
            line = line.replace('\n', '').strip().split(" ")

            # check if is a good line and execute
            if line[0][0] in ['%', '&']:
                val = exe(line, func, data)

                # if val is if, loop or function call (%func <>)
                if val is not None:
                    if val[0] == 'if':
                        param = associate[val[1].replace('%', '')]
                    elif val[0] == 'loop':
                        param = associate[val[3].replace('%', '')]
                    else:
                        param = associate[line[0].replace('%', '')]

                    for y, x in enumerate(data[param]):
                        if val[0] == 'loop':
                            data[param][y] = val[4][y]
                        elif val[0] == 'if':
                            data[param][y] = val[2][y]
                        else:
                            data[param][y] = val[y]

                    if val[0] == 'if':
                        for code in funcCode[val[1].replace('%', '')]:
                            exe(code, func, data)

                    elif val[0] == 'loop':
                        for i in range(int(val[2])):
                            for code in funcCode[val[3].replace('%', '')]:
                                exe(code, func, data)
                    else:
                        for code in funcCode[line[0].replace('%', '')]:
                            exe(code, func, data)
