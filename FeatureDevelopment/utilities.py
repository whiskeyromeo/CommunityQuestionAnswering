import sys


def getargvalue(name, required):
    output = False
    for arg in sys.argv:
        if arg[2:len(name)+2] == name:
            output = arg[3+len(name):]
    if required and not output:
        raise Exception("Required argument " + name + " not found in sys.argv")
    return output


def argvalueexists(name):
    output = False
    for arg in sys.argv:
        if arg[2:len(name)+2] == name:
            output = True
    return output
