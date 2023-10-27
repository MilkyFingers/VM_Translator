from vm_parser import Parser
from vm_codewriter import CodeWriter
from constants import *
import argparse
import os
import glob

if __name__ == "__main__":
    
    parg = argparse.ArgumentParser(description="VM translator for jack bytecode into hack assembly")
    parg.add_argument("Source", help="The source must be either a .vm file or a directory containing at least one .vm file.", type=str)

    source_file = parg.parse_args().Source

    # if we have a single file
    if '.vm' in source_file:
        
        out_file = source_file.split(".")[0]+"."+"asm"

        p = Parser(source_file)
        c = CodeWriter(out_file)
        
        while(p.hasMoreCommands()):
            p.advance()
            if p.commandType() == CommandType.C_ARITHMETIC:
                c.writeArithmetic(p.arg1())
            elif p.commandType() == CommandType.C_POP or p.commandType() == CommandType.C_PUSH:
                c.writePushPop(p.commandType(), p.arg1(), p.arg2())
            elif p.commandType() == CommandType.C_LABEL:
                c.writeLabel(p.arg1())
            elif p.commandType() == CommandType.C_GOTO or p.commandType() == CommandType.C_IF:
                c.writeGoto(p.commandType(), p.arg1())
            elif p.commandType() == CommandType.C_FUNCTION:
                c.writeFunction(p.arg1(), p.arg2())
            elif p.commandType() == CommandType.C_RETURN:
                c.writeReturn()
            elif p.commandType() == CommandType.C_CALL:
                c.writeCall(p.arg1(), p.arg2())
        c.writeEndLoop()
        c.writeBoolSubRoutine()
        p.clean()
        c.clean()

    # In the event we have multiple source *.vm files, we create a .asm files for each .vm file to preserve static vars. we then combine them into a single .asm file
    else:
        directory = source_file
        outfile = directory + ".asm"
        # This ill return a list of .vm files in the specified directory
        files = [f for f in os.listdir(directory) if '.vm' in f]
        # Thee first file we open must have bootstap code injected at the top
        flag = None
        # we must inject boolsubroutine into last file translated
        last = False
        # the file created called 'Sys.asm' will have the bootstrap code
        for fname in files:
            # set flag to inject bootstrap code into Sys.asm
            if fname == "Sys.vm":
                flag = True
            else:
                flag = None
            if fname == files[-1]:
                last = True
            source_file = directory + "/" + fname
            p = Parser(source_file)
            c = CodeWriter(fname.split('.')[0] + ".asm", flag)
            flag = None
            while(p.hasMoreCommands()):
                p.advance()
                if p.commandType() == CommandType.C_ARITHMETIC:
                    c.writeArithmetic(p.arg1())
                elif p.commandType() == CommandType.C_POP or p.commandType() == CommandType.C_PUSH:
                    c.writePushPop(p.commandType(), p.arg1(), p.arg2())
                elif p.commandType() == CommandType.C_LABEL:
                    c.writeLabel(p.arg1())
                elif p.commandType() == CommandType.C_GOTO or p.commandType() == CommandType.C_IF:
                    c.writeGoto(p.commandType(), p.arg1())
                elif p.commandType() == CommandType.C_FUNCTION:
                    c.writeFunction(p.arg1(), p.arg2())
                elif p.commandType() == CommandType.C_RETURN:
                    c.writeReturn()
                elif p.commandType() == CommandType.C_CALL:
                    c.writeCall(p.arg1(), p.arg2())
            if last:
                c.writeBoolSubRoutine()
            p.clean()
            c.clean()
        
        files = glob.glob("*.asm")
        files.sort(key=os.path.getatime)
        files.insert(0, files.pop(files.index("Sys.asm")))
        code = []
        for f in files:
            fo = open(f, 'r+')
            for l in fo.readlines():
                code.append(l)
            fo.close()
        with open(directory + "/" + outfile, 'w') as output:
            for c in code:
                output.write(c)

        for f in files:
            os.remove(f)

        