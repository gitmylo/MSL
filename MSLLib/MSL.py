vardict = {}

def run(lines):
    createcommands()
    alllines = lines.splitlines()
    i = 0
    while i < len(alllines):
        output = handle(alllines[i], i)
        if output.changeline != -1:
            i = output.changeline
        if output.stop:
            break
        i = i + 1

def handle(line, linenum):
    returns = advancedreturn()
    data = split(line)

    returns = runcommand(data, returns, vardict, linenum)

    return returns

def runcommand(data, returns, vars, linenum):
    returns = runit(data, returns, vars, linenum)
    return returns

def split(line):
    data = commanddata()
    data.args = line.split(" ")
    data.onlyargs = data.args[1:]
    data.command = data.args[0]
    data.argsstring = " ".join(data.args[1:])
    data.argsfrom1 = " ".join(data.args[2:])
    data.argsfrom2 = " ".join(data.args[3:])
    data.argsfrom3 = " ".join(data.args[4:])
    data.argsfrom4 = " ".join(data.args[5:])
    return data

class advancedreturn:
    """A class for returning more data from a single line"""
    changeline = -1
    stop = False

class commanddata:
    """A class for storing the command data"""
    command = ""
    args = []
    onlyargs = []
    argsstring = ""
    argsfrom1 = ""
    argsfrom2 = ""
    argsfrom3 = ""
    argsfrom4 = ""

commandlist = []

def createcommands():
    commandlist.append(comment())
    commandlist.append(printline())
    commandlist.append(setcmd())
    commandlist.append(jumpif())
    commandlist.append(jump())
    commandlist.append(convertint())
    commandlist.append(convertfloat())
    commandlist.append(clone())
    commandlist.append(calculate())
    commandlist.append(end())
    commandlist.append(userinput())


def runit(data, returns, vars, linenum):
    for command in commandlist:
        if command.trigger == data.command:
            command.run(data, returns, vars, linenum)
    return returns

def formatstring(text):
    for key, value in vardict.items():
        text = text.replace(key, str(value))
    return text

class runnablecommand:
    trigger = ""

    def __init__(self, trigger):
        self.trigger = trigger

    def run(self, data, returns, vars):
        print("running command: " + data.command) 


class comment(runnablecommand):
    def __init__(self):
        self.trigger = "COM"

    def run(self, data, returns, vars, linenum):
        return returns

class printline(runnablecommand):
    def __init__(self):
        self.trigger = "PRL"

    def run(self, data, returns, vars, linenum):
        print(formatstring(data.argsstring))
        return returns

class setcmd(runnablecommand):
    def __init__(self):
        self.trigger = "SET"

    def run(self, data, returns, vars, linenum):
        vardict["$&" + data.args[1]] = data.argsfrom1
        return returns

class jumpif(runnablecommand):
    def __init__(self):
        self.trigger = "JIF"

    def run(self, data, returns, vars, linenum):
        initialarg = data.onlyargs[0]
        if((data.onlyargs[2] == "<" and float(data.onlyargs[1]) < float(data.onlyargs[3])) or (data.onlyargs[2] == ">" and float(data.onlyargs[1]) > float(data.onlyargs[3])) or (data.onlyargs[2] == "=" and data.onlyargs[1] == data.onlyargs[3])):
            returns.changeline = int(initialarg)
        return returns


class jump(runnablecommand):
    def __init__(self):
        self.trigger = "JMP"

    def run(self, data, returns, vars, linenum):
        initialarg = data.onlyargs[0]
        returns.changeline = int(initialarg)
        return returns

class convertint(runnablecommand):
    def __init__(self):
        self.trigger = "INT"

    def run(self, data, returns, vars, linenum):
        arg = data.onlyargs[0]
        vardict[arg] = int(vardict[arg])
        return returns

class convertfloat(runnablecommand):
    def __init__(self):
        self.trigger = "FLT"

    def run(self, data, returns, vars, linenum):
        arg = data.onlyargs[0]
        vardict[arg] = float(vardict[arg])
        return returns

class clone(runnablecommand):
    def __init__(self):
        self.trigger = "CLN"

    def run(self, data, returns, vars, linenum):
        arg = data.onlyargs[0]
        args2 = data.onlyargs[1]
        vardict[arg] = vardict[args2]
        return returns

class calculate():
    def __init__(self):
        self.trigger = "CAL"

    def run(self, data, returns, vars, linenum):
        storage = data.onlyargs[0]
        math = data.argsfrom1
        math = formatstring(math)
        output = eval(math)
        vardict["$&"+storage] = str(output)
        return returns

class end():
    def __init__(self):
        self.trigger = "END"

    def run(self, data, returns, vars, linenum):
        returns.stop = True
        return returns

class userinput():
    def __init__(self):
        self.trigger = "GET"

    def run(self, data, returns, vars, linenum):
        storage = data.onlyargs[0]
        text = data.argsfrom1
        vardict["$&"+storage] = input(formatstring(text))
        return returns