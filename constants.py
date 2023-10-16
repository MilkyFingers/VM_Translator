"""
This file contains all of the constants to be used by the parser and codewriter
"""
import enum

# a data structure to store the values of C_ARITHMERIC commands
arithmetic_translations = {"add": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M\n",
                          "sub" : "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n",
                          "neg" : "@SP\nA=M-1\nM=-M\n",
                          "eq"  : "@return\nD=A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@False\nD;JNE\n@True\n0;JMP\n(return)\n",
                          "gt"  : "@return\nD=A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@False\nD;JLE\n@True\n0;JMP\n(return)\n",
                          "lt"  : "@return\nD=A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@False\nD;JGE\n@True\n0;JMP\n(return)\n", 
                          "and" : "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M\n",
                          "or"  : "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M\n",
                          "not" : "@SP\nA=M-1\nM=!M\n"}

# the translation for pushing a constant to the stack
push_constant_translation = "@i\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n"

# the translation for pushing/popping to segments local, argument, this and that. i and seg get replaced with relevant values in codewriter
push_latt_translation = "@i\nD=A\n@seg\nA=D+M\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
pop_latt_translation = "@i\nD=A\n@seg\nD=D+M\n@SP\nM=M-1\nA=M+1\nM=D\nA=A-1\nD=M\nA=A+1\nA=M\nM=D\n"

push_static_translation = "@file.i\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
pop_static_translation = "@file.i\nD=A\n@SP\nM=M-1\nA=M+1\nM=D\nA=A-1\nD=M\nA=A+1\nA=M\nM=D\n"

push_temp_translation = "@5\nD=A\n@i\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
pop_temp_translation = "@5\nD=A\n@i\nD=D+A\n@SP\nM=M-1\nA=M+1\nM=D\nA=A-1\nD=M\nA=A+1\nA=M\nM=D\n"

push_pointer_translation = "@seg\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
pop_pointer_translation = "@SP\nM=M-1\nA=M\nD=M\n@seg\nM=D\n"

# Arithmetic operations
ARITHMETIC_OPERATIONS = ['add', 'sub', 'neg', 'eq', 'gt',
                         'lt', 'and', 'or', 'not']

STACK_OPERATIONS = ['push', 'pop']

# memory segment pointers
segment_pointers = {'local': 'LCL',
                    'argument': 'ARG',
                    'this': 'THIS',
                    'that': 'THAT',
                    }

class CommandType(enum.Enum):
    """Command type enum to simplify command names"""
    C_ARITHMETIC = 1
    C_PUSH = "push"
    C_POP = "pop"
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9
    COMMENT = 10
