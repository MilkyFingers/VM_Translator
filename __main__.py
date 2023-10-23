from vm_parser import Parser
from vm_codewriter import CodeWriter
from constants import *
import argparse

if __name__ == "__main__":
    parg = argparse.ArgumentParser(description="VM translator for jack bytecode into hack assembly")
    parg.add_argument("Source_file", help="The source file must be a .vm file", type=str)
    source_file = parg.parse_args().Source_file
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
    c.writeEndLoop()
    c.writeBoolSubRoutine()
    p.clean()
    c.clean()