#coding=utf-8

SpaceChars = " \t"
LowercaseLetterChars = "abcdefghijklmnopqrstuvwxyz"
LetterChars = LowercaseLetterChars + LowercaseLetterChars.upper()
NumberChars = "0123456789"

def simple_escape_char(c):
    if c == "n": return "\n"
    elif c == "t": return "\t"
    elif c == "a": return "\a"
    elif c == "b": return "\b"
    elif c == "f": return "\f"
    elif c == "r": return "\r"
    elif c == "v": return "\v"
    elif c == "0": return "\0"
    elif c == "\n": return ""
    elif c == '"': return '"'
    elif c == "'": return "'"
    elif c == "\\": return "\\"
    else:
        # Just to be sure so that users don't run into trouble.
        assert False, "simple_escape_char: cannot handle " + repr(c) + " yet"

def cdata_parser_in_python(data):
    if data is None: return None
    data = data.lstrip(" \t")
    ret = ""
    state = 0
    aggregate_list = []
    aggregate_all = []
    last_char = ""
    str_type = ""
    for c in data:
        if state == 0:
            if c in SpaceChars: ret += c
            elif c in LetterChars + "_":
                ret += c
                state = 1
            elif c in NumberChars:
                state = 2
                ret += c
            elif c == '"':
                state = 4
                # ret += c
            elif c == "'": state = 6
            elif c == "{": state = 8
            else: ret += c
        elif state == 1: # boolean or wchar
            if c == '"':
                state = 4
                str_type = last_char
                continue
            ret += c
        elif state == 2: # number
            ret += c
            if c in NumberChars: pass
            elif c == "x": state = 3
            elif c == ".": state = 7
            elif c == "e": state = 7
            elif c in LetterChars + "_" + SpaceChars: pass # even if invalid, stay in this state
            else:
                state = 0
        elif state == 3: # hex number
            ret += c
            if c in NumberChars + LetterChars + "_": pass # also ignore invalids
            else: 
                state = 0
        elif state == 4: # str
            ret += c
            if c == "\\": state = 5
            elif c == '"': 
                state = 41
                ret = ret[0:-1]
            else: pass
        elif state == 5: # escape in str
            state = 4
            ret += simple_escape_char(c)
        elif state == 6: # char
            ret = ord(c)
            state = 0
        elif state == 7: #float
            ret += c
            if c in NumberChars: pass
        elif state == 8: #aggregation
            if c == ",":
                val = cdata_parser_in_python(ret)
                aggregate_list.append(val)
                ret = ""
            elif c == "}": 
                val = cdata_parser_in_python(ret)
                aggregate_list.append(val)
                aggregate_all.append(aggregate_list)
                aggregate_list = []
                ret = ""
                state = 81
            elif c in SpaceChars + "{": pass
            else:
                ret += c

            # last_char = c
        elif state == 81:
            if c == "{":
                state = 8
        else:
            state = 0  # recover
        last_char = c

    # boolean
    if state == 1:
        # print(ret)
        ret = ret.strip()
        ret = bool(ret=="true")
    elif state == 2:
        ret = int(ret)
    # 计算最后的16进制数
    elif state == 3:
        ret = int(ret, 16)
    # 字符串处理
    elif state == 41:
        # print(str_type)
        # 如果是宽字符
        if str_type != "" and str_type in "l" + "L":
            # print(ret)
            # print("here")
            ret = ret.lstrip("lL")
            ret = ret.strip('"')
            ret = ret.decode("unicode_escape")
            # print(ret)
            str_type = ""

    # 浮点数  
    elif state == 7:
        ret = ret.rstrip()
        ret = ret.rstrip("fF")
        ret = float(ret)
    # 聚合
    elif state == 81:
        # print(aggregate_all)
        ret = []
        if len(aggregate_all) == 1:
            aggregate_all = aggregate_all[0]
            ret = tuple(aggregate_all)
        else:
            for v in aggregate_all:
                one = tuple(v)
                ret.append(one)
            ret = tuple(ret)

    return ret
                


# 检测是否正确定义宏名
def is_valid_defname(defname):
    if not defname: return False
    gotValidPrefix = False
    for c in defname:
        if c in LetterChars + "_":
            gotValidPrefix = True
        elif c in NumberChars:
            if not gotValidPrefix: return False
        else:
            return False
    return True

# 判断宏是否已经定义
def cpreprocess_evaluate_ifdef(state, arg):
    arg = arg.strip()
    if not is_valid_defname(arg):
        state.error("preprocessor: '" + arg + "' is not a valid macro name")
        return False
    if arg in ("__FILE__", "__LINE__"): return True
    return arg in state.macros

def handle_cpreprocess_cmd(state, cmd, arg):

    if cmd == "ifdef":
        state._preprocessIfLevels += [0]
        # 检验
        if any(map(lambda x: x != 1, state._preprocessIfLevels[:-1])): return # we don't really care
        check = cpreprocess_evaluate_ifdef(state, arg)
        
        if check: state._preprocessIfLevels[-1] = 1

    elif cmd == "ifndef":
        state._preprocessIfLevels += [0]
        if any(map(lambda x: x != 1, state._preprocessIfLevels[:-1])): return # we don't really care
        check = not cpreprocess_evaluate_ifdef(state, arg)
        if check: state._preprocessIfLevels[-1] = 1

    elif cmd == "else":
        if any(map(lambda x: x != 1, state._preprocessIfLevels[:-1])): return # we don't really care
        if len(state._preprocessIfLevels) == 0:
            state.error("preprocessor: else without if")
            return
        if state._preprocessIfLevels[-1] >= 1:
            state._preprocessIfLevels[-1] = 2 # we already had True
        else:
            state._preprocessIfLevels[-1] = 1

    elif cmd == "endif":
        if len(state._preprocessIfLevels) == 0:
            state.error("preprocessor: endif without if")
            return
        # 去掉栈顶if标识（0或1)
        state._preprocessIfLevels = state._preprocessIfLevels[0:-1]

    elif cmd == "define":
        # 若不是该条件分支直接return
        if state._preprocessIgnoreCurrent: return
        cpreprocess_handle_def(state, arg)

    elif cmd == "undef":
        if state._preprocessIgnoreCurrent: return
        cpreprocess_handle_undef(state, arg)

    else:
        if state._preprocessIgnoreCurrent: return # we don't really care
        state.error("preprocessor command " + cmd + " unknown")

    # 判断是否进入不符合条件的分支
    state._preprocessIgnoreCurrent = any(map(lambda x: x != 1, state._preprocessIfLevels))

# 定义新的宏
def cpreprocess_handle_def(stateStruct, arg):
    state = 0
    macroname = ""
    args = None
    rightside = ""
    for c in arg:
        if state == 0:
            if c in SpaceChars:
                if macroname != "": state = 3
            elif c == "(":
                state = 2
                args = []
            else: macroname += c
        elif state == 2: # after "("
            if c in SpaceChars: pass
            elif c == ",": args += [""]
            elif c == ")": state = 3
            else:
                if not args: args = [""]
                args[-1] += c
        elif state == 3: # rightside
            rightside += c

    # print("macroname:" + macroname + " rightside:" + rightside)
    
    if not is_valid_defname(macroname):
        stateStruct.error("preprocessor define: '" + macroname + "' is not a valid macro name")
        return

    if macroname in stateStruct.macros:
        stateStruct.error("preprocessor define: '" + macroname + "' already defined.")
        return
        # pass through to use new definition

    macro = Macro(stateStruct, macroname, args, rightside)
    stateStruct.macros[macroname] = macro
    return macro

# 去掉宏
def cpreprocess_handle_undef(state, arg):
    arg = arg.strip()
    if not is_valid_defname(arg):
        state.error("preprocessor: '" + arg + "' is not a valid macro name")
        return
    if not arg in state.macros:
        # This is not an error. Just ignore.
        return
    state.macros.pop(arg)

def macro_parse(stateStruct, line):
    # 指令
    cmd = ""
    # 字符串
    arg = ""

    state = 0
    statebeforecomment = None
    for c in line:
        breakLoop = False
        while not breakLoop:
            breakLoop = True
            if state == 0:
                if c == "#":
                    cmd = ""
                    arg = None
                    state = 1
                elif c == "/":
                    statebeforecomment = 0
                    state = 20
                elif c == '"':
                    state = 10
                elif c == "'":
                    state = 12
                else:
                    pass
            # 预处理指令开始
            elif state == 1:
                # if c in SpaceChars: pass
                if c == "\n":state = 0
                else:
                    cmd = c
                    state = 2
            # 正在读入指令
            elif state == 2:
                if c in SpaceChars:
                    if arg is None: arg = ""
                    else: 
                        if arg != "":
                            arg += c
                # 字符串
                elif c == '"':
                    state = 3
                    if arg is None: arg = ""
                    arg += c
                elif c == "'":
                    state = 4
                    if arg is None: arg = ""
                    arg += c
                # 注释
                elif c == "/":
                    state = 20
                    statebeforecomment = 2
                elif c == "\\": state = 5
                elif c == "\n":
                    # print("cmd = %s, arg = %s" % (cmd, arg) )
                    # cmd = ""
                    # arg = None
                    handle_cpreprocess_cmd(stateStruct, cmd, arg)
                    state = 0
                else:
                    if arg is None: cmd +=c
                    else:
                        arg += c
            elif state == 3:
                arg += c
                if c == "\n":
                    print("Error unfinished str")
                    state = 0
                elif c == "\\": state = 35
                elif c == '"': state = 2
            elif state == 35:
                arg += c
                state = 3
            elif state == 4:
                arg += c
                if c == "\n":
                    print("Error unfinished str")
                    state = 0
                elif c == "\\": state = 45
                elif c == "'": state = 2
            elif state == 45:
                arg += c
                state = 4
            elif state == 5:
                if c == "\n": state = 2
                else:pass
            elif state == 10:
                if not stateStruct._preprocessIgnoreCurrent: pass
                if c == "\\": state = 11
                elif c == '"': state = 0
                else: pass
            elif state == 11:
                print("ignore11")
                state = 10
            elif state == 12:
                print("ignore12")
                if c == "\\": state = 13
                elif c == "'": state = 0
                else:pass
            elif state == 13:
                print("ignore13")
                state = 12
            elif state == 20:
                if c == "*": state = 21
                elif c == "/": state = 25
                else:
                    state = statebeforecomment
                    statebeforecomment = None
                    if state == 0:
                        print("ignore20")
                    elif state == 2:
                        if arg is None: arg = ""
                        arg += "/" + c
                    else:
                        print("Error comment")
                        state = 0 
            elif state == 21:
                if c == "*": state = 22
                else: pass
            elif state == 22:
                if c == "/":
                    state = statebeforecomment
                    statebeforecomment = None
                elif c == "*": pass
                else: state = 21
            elif state == 25:
                if c == "\n":
                    state = statebeforecomment
                    statebeforecomment = None
                    breakLoop = False
                else: pass
            else:
                print("Erro invalid state")
                state = 0


class Macro(object):
    def __init__(self, state=None, macroname=None, args=None, rightside=None):
        self.name = macroname
        self.args = args
        self.rightside = rightside if (rightside is not None) else ""
        # self.defPos = state.curPosAsStr() if state else "<unknown>"
        self._tokens = None

    def dump(self):
        # print(self.name)
        # print(self.rightside if(self.rightside) else None)
        value = self.rightside if(self.rightside) else None
        # print(value)
        value = cdata_parser_in_python(value)
        if value is None:
            value = ""
        elif type(value) == tuple:
            value = self.rightside
        elif type(value) == str:
            value = '"' + value + '"'
        elif type(value) == unicode:
            value = 'L"' + value + '"'
        elif type(value) == bool:
            if value:
                value = "true"
            else:
                value = "false"
        return "#define " + self.name + " " + str(value)

    def eval(self):
        # key_and_value = {}
        value = self.rightside if(self.rightside) else None
        value = cdata_parser_in_python(value)
        # key_and_value[self.name] = value
        # print(key_and_value)
        return self.name, value

class PyMacroParser:
    def __init__(self):
        self.file = ""
        self.macros = {}
        # 指令栈
        self._preprocessIfLevels = []
        # 用于标识是否执行当前分支的语句
        self._preprocessIgnoreCurrent = False

    def reset(self):
        self.macros = {}
        self._preprocessIfLevels = []
        self._preprocessIgnoreCurrent = False

    def error(self, s):
        print(s)

    def load(self, f):
        try:
            self.file = f
            cpy = open(f, "r")
            line = cpy.read()
            macro_parse(self,line)
        except IOError:
            print("文件读取失败，请确认正确的文件路径")
        else:
            cpy.close()

    def preDefine(self, s):
        self.reset()
        def_macro = ""
        
        for c in s:
            if c == ";":
                cpreprocess_handle_def(self, def_macro)
                def_macro = ""
            else:
                def_macro += c

        cpreprocess_handle_def(self, def_macro)
        self.load(self.file)

    def dumpDict(self):
        # print(self.macros)
        dump_dict = {}
        for k in self.macros:
            v = self.macros[k]
            key, val = v.eval()
            dump_dict[key] = val
            if key == "TRACE_REFS":
                print("haved trace_refs")    
            # print(key)
            # print(type(val))
            # print(val)
        return dump_dict


    def dump(self, f):
        with open(f, "w") as f:
            for k in self.macros:
                v = self.macros[k]
                # print(v.dump())
                f.write(v.dump())
                f.write("\n")