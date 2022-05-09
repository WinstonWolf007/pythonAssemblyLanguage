from error import display


# default var
data = {'dft': [0]}
associate, funcCode = {}, {}
inFunc = [None, False]
infoFIle = {}


# It used for looping a function
def loop(value):
    if value[2][0].strip() == '%':
        param = value[2:]
        param2 = param[1:]
        param3 = param[0].replace(" ", "").split('<')
        param3 += param2
        param3 = [x.replace('>', '').strip() for x in param3]
        value[2:] = [param3]

    if len(value) == 3:
        fnName = value[2][0]
        fnParam = value[2:][0][1:]
        return 'loop', value[0], value[1], fnName, fnParam


# The condition function
def if_(value):
    global infoFIle

    # get 2 number and the comparison symbol
    nbr = [int(x) for x in [value[0], value[2]]]
    symbol = int(value[1])

    # dict condition (just optimization)
    comparison = {
        0: True if nbr[0] != nbr[1] else False,
        1: True if nbr[0] == nbr[1] else False,
        2: True if nbr[0] > nbr[1] else False,
        3: True if nbr[0] < nbr[1] else False,
        4: True if nbr[0] >= nbr[1] else False,
        5: True if nbr[0] <= nbr[1] else False
    }

    # call function if condition is True else do nothing
    if symbol in comparison:
        if comparison.get(symbol):
            value = value[3:]
            value[0].replace(' ', '')
            fnName, fistParam = value[0].split('<')
            p1 = value[1:]
            param = [x.strip().replace('>', '') for x in p1]
            param.insert(0, fistParam)
            return 'if', fnName.strip(), param
    else:
        # symbol is not in comparison dict
        display(
            SyntaxError,
            'None',
            infoFIle['lineNbr'],
            infoFIle['lineCode'],
            f'"{symbol}" it not comparison symbol. Choice in {[x for x in comparison.keys()]}'
        )


# The function is used for create function
def def_(value):
    global inFunc, funcCode, associate

    nt = value[0].strip().split('<')
    nameFunc = nt[0].strip()
    tableFunc = nt[1].strip()
    octet = int(value[1].replace(">", "").strip())
    inFunc[0] = nameFunc
    inFunc[1] = True
    rgt([octet, tableFunc])
    funcCode[nameFunc] = []
    associate[nameFunc] = tableFunc


def rgt(value):
    byte, name = value
    if name != 'dft':
        data[name] = [x - x for x in range(int(byte))]
    else:
        # name == dft
        display(
            NameError,
            'None',
            infoFIle['lineNbr'],
            infoFIle['lineCode'],
            f'Do not use the "{name}" name. It is reserved for the "&call" function.'
        )


def lk(value):
    for rgtTable in value:
        if rgtTable in data:
            print(data.get(rgtTable))
        else:
            # rgtTable not in data
            display(
                SyntaxError,
                'None',
                infoFIle['lineNbr'],
                infoFIle['lineCode'],
                f'The "{rgtTable}" register does not exist.'
            )


def out(value):
    table = data[value[0]]
    try:
        msg = "".join([str(chr(int(x))) for x in table if x != 0])
    except:
        msg = ""

    if '\\n' in msg:
        print(msg.replace('\\n', ''))
    else:
        print(msg, end='')


def get(value):
    startRgt, startIdx, endRgt, endIdx = value
    if startRgt in data and endRgt in data:
        v = data[startRgt][int(startIdx)]
        data[endRgt][int(endIdx)] = v
    else:
        if startRgt not in data and endRgt not in data:
            display(
                SyntaxError,
                'None',
                infoFIle['lineNbr'],
                infoFIle['lineCode'],
                f'The two registers does not exist.'
            )
        elif startRgt not in data:
            display(
                SyntaxError,
                'None',
                infoFIle['lineNbr'],
                infoFIle['lineCode'],
                f'The "{startRgt}" registers does not exist.'
            )
        elif endRgt not in data:
            display(
                SyntaxError,
                'None',
                infoFIle['lineNbr'],
                infoFIle['lineCode'],
                f'The "{endRgt}" registers does not exist.'
            )


def del_(value):
    for rgtTable in value:
        if rgtTable in data:
            if rgtTable != 'dft':
                data.pop(rgtTable)
            else:
                display(
                    NameError,
                    'None',
                    infoFIle['lineNbr'],
                    infoFIle['lineCode'],
                    f'You can\'t delete the "dft" register'
                )
        else:
            display(
                SyntaxError,
                'None',
                infoFIle['lineNbr'],
                infoFIle['lineCode'],
                f'The "{rgtTable}" register does not exist.'
            )


def getInput(value):
    msg, target = value
    gets = input("".join([chr(x) for x in data[msg]]))
    for x, g in enumerate(gets):
        data[target][x] = int(ord(g))


def put(value):
    table, idx, values = value
    if table in data:
        data[table][int(idx)] = int(values)
    else:
        display(
            SyntaxError,
            'None',
            infoFIle['lineNbr'],
            infoFIle['lineCode'],
            f'The "{table}" register does not exist.'
        )


def call(value):
    values = data['dft'][0]
    fn = {0: out, 1: exit, 2: getInput}
    if values in fn:
        if values == 1:
            exit(int(value[0]))
        fn.get(values)(value)


def upt(value):
    table, idx, values = value
    if table in data:
        if len(values) >= 1:
            if values[0] == '+':
                data[table][int(idx)] += int(values.replace('+', ''))
            elif values[0] == '-':
                data[table][int(idx)] -= int(values.replace('-', ''))
            elif values[0] == '*':
                data[table][int(idx)] *= int(values.replace('*', ''))
            elif values[0] == '/':
                data[table][int(idx)] /= int(values.replace('/', ''))
            else:
                display(
                    SyntaxError,
                    'None',
                    infoFIle['lineNbr'],
                    infoFIle['lineCode'],
                    f'The "{values[0]}" operation does not exist.'
                )
    else:
        display(
            SyntaxError,
            'None',
            infoFIle['lineNbr'],
            infoFIle['lineCode'],
            f'The "{table}" register does not exist.'
        )
