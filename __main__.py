from vm_parser import Parser
from vm_codewriter import CodeWriter
from constants import *
import argparse
import os

if __name__ == "__main__":
    parg = argparse.ArgumentParser(description="VM translator for jack bytecode into hack assembly")
    parg.add_argument("Source", help="The source must be either a .vm file or a directory containing at least one .vm file.", type=str)

    source_file = parg.parse_args().Source
    directory = source_file
    # passed to the codewriter. if the input is a directory, we must enbale writing bootstap code in its constructor
    flag = None

    # if we have a file
    if '.vm' in source_file:
        out_file = source_file.split(".")[0]+"."+"asm"

    else:
        # we need to create a single file for the parser and codewriter
        # this will return all .vm files in files
        files = [f for f in os.listdir(source_file) if '.vm' in f]
        out_file = source_file + ".asm"
        source_file += ".vm"
        with open(source_file, 'w') as outfile:
            for fname in files:
                with open(directory+"/"+fname) as infile:
                    for line in infile:
                        outfile.write(line)
        flag = 1

    p = Parser(source_file)
    c = CodeWriter(out_file, flag)
    
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
    c.writeBoolSubRoutine()
    p.clean()
    c.clean()
    try:
        os.remove(directory+".vm")
    except:
        pass