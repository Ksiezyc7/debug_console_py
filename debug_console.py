import msvcrt
import re
def _match_type(text: str, type: str):
    if len(type) < 1:
        return False
    match type:
        case "int":
            return re.search("^-?[0-9]+$", text) != None
        case "float":
            return re.search("^-?[0-9]+(\\.[0-9]+)?$", text) != None
        case "str":
            return re.search("^\"[^\"]*\"$", text) != None
        case "bool":
            return re.search("^(true|false)$", text) != None
    if("|" in type):
        return re.search(f"^({type})$", text) != None
    if(type[0] == "!"):
        return re.search(f"^{type[1:]}$", text) != None
def _match(args: list, types: list):
    for i in range(len(args)):
        if(not _match_type(args[i], types[i])):
            return False
    return True
def _cast_to_type(val: str, type: str):
    if len(type) < 1:
        return None
    match type:
        case "int":
            return int(val)
        case "float":
            return float(val)
        case "str":
            return val.strip("\"")
        case "bool":
            if(val == "true"):
                return True
            elif(val == "false"):
                return False
            else:
                return None
    if("|" in type):
        return val
    if(type[0] == "!"):
        return val.lstrip("!")
def _cast_to_type_l(val: list, type: list):
    a = []
    for i in range(len(val)):
        a.append(_cast_to_type(val[i], type[i]))
    return a
class DebugConsole:
    
    buffer = ""
    def __init__(self):
        self.buffer = ""
        self.commands = []
        pass
    def log(self, message: str):
        print(f"\r{len(self.buffer) * " "}\r{message}\n{self.buffer}", end="", flush=True)
    def set_buffer(self, m: str):
        if(m == ""):
            print(f"\r{len(self.buffer)*" "}\r", end="", flush=True)
        else:
            print(f"\r{len(self.buffer) * " "}\r{len(self.buffer)}\r{m}", end="", flush=True)
        self.buffer = m
    def error(self, message: str):
        self.log("\033[0;91m[ERROR]\033[m " + message)
    def warn(self, message: str):
        self.log("\033[0;93m[WARNING]\033[m " + message)     
    def process_keys(self):
        key = 0
        if msvcrt.kbhit():
            key = int.from_bytes(msvcrt.getch(), "little")
        if(key > 31 and key < 127):
            self.set_buffer(self.buffer + chr(key))
        if(key == 8 or key == 127):
            if(len(self.buffer) == 1):
                self.set_buffer("")
            else:
                self.set_buffer(self.buffer[:-1])
        if(key == 13):
            self.call()
            #call function
            self.set_buffer("")
        elif(key == 27):
            exit(0)
    def bind_command(self, name: str, arguments: list, callback):
        self.commands.append((name, arguments, callback))
    def _function_error(self, message: str):
        self.log(f"\033[0;91m{message}\033[0m")
    def call(self):
        global __match
        if(len(self.buffer) < 1):
            return
        if(self.buffer[0] != "/"):
            return
        self.log(self.buffer)
        cmd = self.buffer.rstrip("\n").split()
        overloads = []
        for i in self.commands:
            if i[0] == cmd[0].lstrip("/"):
                overloads.append(i)
        if(len(overloads) == 0):
            self._function_error("No such function found")
            return
        has_matched_len = False
        _iter = 0
        chosen_overload = None
        f_args = []
        for o in overloads:
            if(len(o[1]) != len(cmd[1:])):
                continue
            has_matched_len = True
            if(_match(cmd[1:], o[1])):
                chosen_overload = o
        if(not has_matched_len):
            self._function_error(f"No overload of {cmd[0]} takes {len(cmd[1:])} arguments")
            return
        if(chosen_overload == None):
            self._function_error(F"No overload of {cmd[0]} takes such arguments")
            return
        f_args = _cast_to_type_l(cmd[1:], chosen_overload[1])
        chosen_overload[2](f_args)
        

            
