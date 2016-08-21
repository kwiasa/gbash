#!/usr/bin/python3
#
# Copyright (C) 2015-2016 Perilbrain
# Author: Perilbrain


from abc import ABCMeta, abstractmethod
import os
import stat
import urllib.parse

FLAG_PARAM = 1
ARG_PARAM = 2
MUTEX_PARAM = 3
INVALID_INPUT = 10

PROG_DESC = "Created using gbash.py from https://github.com/perilbrain/gbash"

class COLOR:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def err(msg, end="\t"):
        print("{0}{1}{2}{3}".format(COLOR.FAIL, msg, COLOR.END, end))

    def blue(msg, show= False, end="\t"):
        text = "{0}{1}{2}{3}".format(COLOR.BLUE, msg, COLOR.END, end)
        if show:
            print(text)
        else:
            return text

    def green(msg, show= False, end="\t"):
        text = "{0}{1}{2}{3}".format(COLOR.GREEN, msg, COLOR.END, end)
        if show:
            print(text)
        else:
            return text

    def yellow(msg, show= False, end="\t"):
        text = "{0}{1}{2}{3}".format(COLOR.WARNING, msg, COLOR.END, end)
        if show:
            print(text)
        else:
            return text

    def bold(msg, show= False, end="\t"):
        text = "{0}{1}{2}{3}".format(COLOR.BOLD, msg, COLOR.END, end)
        if show:
            print(text)
        else:
            return text

class Util:
    inputRecord = []
    
    def getInput(optMsg):
        content = input(optMsg)
        Util.inputRecord.append(content)
        return content;

    def getInputLog(urlEncode = True):        
        content = "\n".join(Util.inputRecord)
        return urllib.parse.quote(content) if urlEncode else content
        
    def choice(optMsg, isEmpty = False, defVal = False, length = 0):
        inpVal = Util.getInput(optMsg)
        if len(inpVal) == 0:
            if defVal:
                return defVal
            else:
                if isEmpty:
                    return False
                else:
                    COLOR.err("Input can't be blank, please re-enter")
                    return Util.choice(optMsg, isEmpty, defVal)
        elif length > 0 and (len(inpVal) != length):
            COLOR.err("Maximum allowed length is {0}".format(length))
            return Util.choice(optMsg, isEmpty, defVal)
        else:
            return inpVal
        
    def boolChoice(optMsg, defVal = True):
        newMsg = "{0} ({1}/{2}):".format(optMsg, 'Y' if defVal else 'y', 'n' if defVal else 'N')
        userChoice = Util.choice(newMsg, defVal = 'y' if defVal else 'n')
        return userChoice.lower().startswith('y')
    
    def numChoice(optMsg, defVal = 0):
        try:
            inpVal = int(Util.getInput(optMsg))
            return inpVal
        except ValueError:
            return defVal

    def make_executable(path):
        mode = os.stat(path)
        os.chmod(path, mode.st_mode | stat.S_IEXEC | stat.S_IXUSR)

class SelfCreate():
    sOptMsg = COLOR.yellow("Enter Flag value (single character):")
    optNameMsg = COLOR.blue("Enter name for function (default = {0}_func):")
    argParamMsg = COLOR.blue("PROTOTYPE for argument (default = <ANY>):")
    descMsg = COLOR.blue("Tell what this option does (default = <TODO>):")
    commitMsg = COLOR.blue("If all is fine above should I commit?")
    
    def __init__(self, pType):
        self.pType = FLAG_PARAM
        self.sOpt = ''
        self.optName = ''
        self.desc = '<TODO>'
        self.commit = True

    def isValid(self):
        return self.commit;
        
    @abstractmethod
    def ask(self):
        pass

class FlagParam(SelfCreate):
    
    def __init__(self):
        SelfCreate.__init__(self, FLAG_PARAM)
        
    def ask(self):
        self.sOpt = Util.choice(SelfCreate.sOptMsg, length = 1)
        self.optName = Util.choice(SelfCreate.optNameMsg.format(self.sOpt), defVal=self.sOpt+"_func")
        self.desc = Util.choice(SelfCreate.descMsg, defVal = self.desc)
        self.commit = Util.boolChoice(SelfCreate.commitMsg)
        return self
    
class ArgParam(SelfCreate):
    def __init__(self):
        SelfCreate.__init__(self, ARG_PARAM)
        self.argParam = '<TODO>'
        
    def ask(self):
        self.sOpt = Util.choice(SelfCreate.sOptMsg, length = 1)
        self.optName = Util.choice(SelfCreate.optNameMsg.format(self.sOpt), defVal = self.sOpt+"_func")
        self.argParam = Util.choice(SelfCreate.argParamMsg, defVal = self.argParam)
        self.desc = Util.choice(SelfCreate.descMsg, defVal = self.desc)
        self.commit = Util.boolChoice(SelfCreate.commitMsg)
        return self

        
class MutexParam():
    inpHelp = COLOR.blue('''Now choose one of them(1/2/7/0 without '.')
1. Flag parameters, no options.
2. Argument parameters, having one parameter.
7. (dangerous)**Clear mutex entries in this session**
0. To break out
''', end="\n")
    commitMsg = COLOR.blue("If all is fine above should I commit? 'No' will start fresh mutex parameter ")
    def __init__(self, optStage = 0):
        self.subParams = []
        self.optStageName = "optStage_{0}".format(optStage)        
        self.commit = True

    def isValid(self):
        return self.commit;
    
    def ask(self):
        inpNum = Util.numChoice(MutexParam.inpHelp, defVal = INVALID_INPUT)
        while (inpNum != 0) or (len(self.subParams) < 2) :
            if inpNum == 1:
                fP = FlagParam().ask()
                if fP.isValid():
                    self.subParams.append(fP)
            elif inpNum == 2:
                aP = ArgParam().ask()
                if aP.isValid():
                    self.subParams.append(aP)
            elif inpNum == 7:
                self.subParams.clear()
            else:
                COLOR.err("Invalid Choice, please re-enter (this needs atleast two flags)\n")
            
            inpNum = Util.numChoice(MutexParam.inpHelp, defVal = INVALID_INPUT)
        
        self.commit = Util.boolChoice(MutexParam.commitMsg)
            
        return self

class ScriptProps:
    
    def __init__(self):
        self.options = []
        self.cases = []
        self.progDesc = '<TODO>'
        self.genParams = []

class BashGen:
    inpHelp = COLOR.blue('''
Choose your argument type(1/2/3/0 without '.')
1. Flag option, having no following argument like "b" in `cmd -b`.
2. Argument option, having one following option like "c" in `cmd -b -c param1`.
3. Mutually exclusive parameters, combination of above 1 & 2 like `cmd [-b|-c param1|-d param2] `.
0. To break out
''', end= "\n")
    def __init__(self):
        self.name = ''
        self.progDesc = '<TODO>'
        self.mutexCount = 0
        self.genParams = []
        # Text Specific
        self.helpSecTop = ''
        self.helpSecBottom = ''
        self.getOpts = ''
        self.gParams = ''
        self.caseStmnt = ''
        self.funcs = ''

    def genTemplate(self):
        inputLog = Util.getInputLog(True)
        return """#!/bin/bash
# {7}

err() {{
    local FAIL="\\033[91m"
    local END="\\033[0m"
    local msg="$1"
    echo -e "$FAIL$msg$END" >&2
}}

show_help() {{
cat << EOF
{0}
Usage: ${{0##*/}} {1}
{2}
EOF
}}

dump_input() {{
    local PARSER=$(python -c "import sys; print( 'urllib.parse' if (sys.version_info[0] == 3) else 'urllib' )")
    python -c "import $PARSER; print($PARSER.unquote('{8}'))"
}}

{3}

{4}

if [ "$1" == "--dumpinput" ]; then
    dump_input >&1
    exit 0
fi

GETOPT_RAN=false
while getopts ":{5}" opt; do
    GETOPT_RAN=true
    case $opt in {6}
        \?)
            err "Invalid option: -$OPTARG"
            show_help >&2
            exit 1
            ;;
        :)
            err "Option -$OPTARG requires an argument."
            show_help >&2
            exit 1
            ;;
    esac
done

if [ "$GETOPT_RAN" = false ] ; then
    show_help >&2
    exit 1
fi

## Copy to create shorthand for /dev/stdout or /dev/stdin using hyphen "-"
#     if [ "$1" == "-" ]; then
#         OUTPUT_FILE="/dev/stdout"
#     else
#         if [ -z "$1" ]; then
#             OUTPUT_FILE="/dev/stdout"
#         else
#             OUTPUT_FILE=$1
#         fi
#     fi

""".format(self.progDesc, self.helpSecTop, self.helpSecBottom, self.funcs, self.gParams, self.getOpts, self.caseStmnt, PROG_DESC, inputLog)

#Handle FLAG type

    def handleFlag(self, param):
        self.helpSecTop = self.helpSecTop + " -{0}".format(param.sOpt)
        self.helpSecBottom = self.helpSecBottom + "\n    -{0}\t{1}".format(param.sOpt, param.desc)
        self.funcs = self.funcs + """
{0}() {{
    err "Unimplemented -{1} ({0})"
}}
""".format(param.optName, param.sOpt)
        self.getOpts = self.getOpts + param.sOpt
        self.caseStmnt = self.caseStmnt + """
        {0})
            {1}
            ;;""".format(param.sOpt, param.optName)

#Handle ARGUMENT type

    def handleArg(self, param):
        self.helpSecTop = self.helpSecTop + " -{0} {1}".format(param.sOpt, param.argParam)
        self.helpSecBottom = self.helpSecBottom + "\n    -{0}\t{1}".format(param.sOpt, param.desc)
        self.funcs = self.funcs + """
{0}() {{
    local param_{0}=$1
    err "Unimplemented -{1} ({0}) with param $param_{0}"
}}
""".format(param.optName, param.sOpt)
        self.getOpts = self.getOpts + param.sOpt+':'
        self.caseStmnt = self.caseStmnt + """
        {0})
            {1} "$OPTARG"
            ;;""".format(param.sOpt, param.optName)

#Handle MUTEX type

    def handleMutex(self, mutexParam):
        helpSecTp = []
        optList = []
        self.gParams = self.gParams + "\n{0}=true".format(mutexParam.optStageName)
        for param in mutexParam.subParams:
            self.helpSecBottom = self.helpSecBottom + "\n    -{0}\t{1}".format(param.sOpt, param.desc)
            optList.append(param.sOpt)
            if isinstance(param, FlagParam):
                helpSecTp.append("-{0}".format(param.sOpt))
                self.getOpts = self.getOpts + param.sOpt
                self.funcs = self.funcs + """
{0}() {{
    err "Unimplemented -{1} ({0})"
}}
""".format(param.optName, param.sOpt)                
            else:
                helpSecTp.append("-{0} {1}".format(param.sOpt, param.argParam))
                self.getOpts = self.getOpts + param.sOpt+':'
                self.funcs = self.funcs + """
{0}() {{
    local param_{0}=$1
    err "Unimplemented -{1} ({0}) with param $param_{0}"
}}
""".format(param.optName, param.sOpt)
            
        for param in mutexParam.subParams:
            if isinstance(param, FlagParam):
                self.caseStmnt = self.caseStmnt + """
        {0})
            if [ "${1}" = true ] ; then
                {1}=false
                {2}
            else
                err "Only one in {3} is allowed, ignoring -$opt $OPTARG"
            fi
            ;;""".format(param.sOpt, mutexParam.optStageName, param.optName, ', '.join(optList) )                
            else:
                self.caseStmnt = self.caseStmnt + """
        {0})
            if [ "${1}" = true ] ; then
                {1}=false
                {2} "$OPTARG"
            else
                err "Only one in {3} is allowed, ignoring -$opt $OPTARG"
            fi
            ;;""".format(param.sOpt, mutexParam.optStageName, param.optName, ', '.join(optList) )

        self.helpSecTop = self.helpSecTop + "[{0}] ".format('|'.join(helpSecTp))
            
            

    def start(self):
        inpNum = Util.numChoice(BashGen.inpHelp, defVal = INVALID_INPUT)
        while inpNum != 0 :
            if inpNum == 1:
                fP = FlagParam().ask()
                if fP.isValid():
                    self.genParams.append(fP)
            elif inpNum == 2:
                aP = ArgParam().ask()
                if aP.isValid():
                    self.genParams.append(aP)            
            elif inpNum == 3:
                mP = MutexParam(self.mutexCount).ask()
                if mP.isValid():
                    self.genParams.append(mP)
                    self.mutexCount = self.mutexCount + 1
            else:
                COLOR.err("Invalid Choice, please re-enter")
            inpNum = Util.numChoice(BashGen.inpHelp, defVal = INVALID_INPUT)
            
        self.name = Util.choice(COLOR.blue("Enter File Name (empty for one screen dump)"), isEmpty = True)
        self.progDesc = Util.choice(COLOR.blue("What this script does?"), defVal = self.progDesc)
        self.dumpGen()

    def dumpGen(self):
        for obj in self.genParams:
            if isinstance(obj, FlagParam):
                self.handleFlag(obj)
            elif isinstance(obj, ArgParam):
                self.handleArg(obj)
            elif isinstance(obj, MutexParam):
                self.handleMutex(obj)
            else:
                print("Encountered unknown type")
        if self.name == False or (len(self.name) < 1):
            print(self.genTemplate())
        else:
            with open(self.name, 'w') as f:
                f.write(self.genTemplate())
            f.close()
            Util.make_executable(self.name)
            COLOR.green("\nwrote file:\t"+self.name, show=True)
        

if __name__ == '__main__':
    BashGen().start()
    
