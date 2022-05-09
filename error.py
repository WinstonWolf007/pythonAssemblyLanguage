def display(type_e, file, line, code, msg):
    print('\033[1:31m' +
          f'File "{file}", line {line}\n\n\t{code}\n'+
          str(type_e).split("\'")[1] + f': {msg}' + '\033[0m')
