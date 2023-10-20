from constants import *
import uuid

class CodeWriter:
    
    def __init__(self, outputfile):
        try:
            self.output = open(outputfile, "w")
        except:
            print("Could not open a file stream for output file!")
        # here 'None' value will be replaced with the computation
        self.file = outputfile.strip('.asm')

    # The conditional operations have a return address as they all jump to a shared True/False subroutine at the end of the program.
    # This is to simplify having multiple unique (true)/(false) and instead use one label for (return)
    def writeArithmetic(self, cmd):
        exit_point = str(uuid.uuid1())
        self.output.write(arithmetic_translations[cmd].replace("return", exit_point))

    def writePushPop(self, cmd, arg1, arg2):

        if cmd == CommandType.C_POP:
            
            if arg1 == "static":
                ins = pop_static_translation.replace("file.i", self.file + "." + arg2)
                self.output.write(ins)

            elif arg1 == "temp":
                ins = pop_temp_translation.replace("i", arg2)
                self.output.write(ins)

            elif arg1 == "pointer":
                if arg2 == "0":
                    ins = pop_pointer_translation.replace("seg", "THIS")
                    self.output.write(ins)
                else:
                    ins = pop_pointer_translation.replace("seg", "THAT")
                    self.output.write(ins)
            else:
                ins = pop_latt_translation.replace("seg", segment_pointers[arg1])
                ins = ins.replace("i", arg2)
                self.output.write(ins)

        else:
            
            if arg1 == "static":
                ins = push_static_translation.replace("file.i", self.file + "." + arg2)
                self.output.write(ins)
            
            elif arg1 == "temp":
                ins = push_temp_translation.replace("i", arg2)
                self.output.write(ins)

            elif arg1 == "pointer":
                if arg2 == "0":
                    ins = push_pointer_translation.replace("seg", "THIS")
                    self.output.write(ins)
                else:
                    ins = push_pointer_translation.replace("seg", "THAT")
                    self.output.write(ins)         

            elif arg1 == "constant":
                ins = push_constant_translation.replace("i", arg2)
                self.output.write(ins)

            else:
                ins = push_latt_translation.replace("seg", segment_pointers[arg1])
                ins = ins.replace("i", arg2)
                self.output.write(ins)

    def writeLabel(self, arg1):
        self.output.write("(" + arg1 + ")\n")

    # This method will be used to write for both the goto and the if-goto commands by taking the cmd_type as an argument 
    def writeGoto(self, cmd, arg1):
        if cmd == CommandType.C_GOTO:
            # we first address the label location and then perform an unconditional jump
            self.output.write("@" + arg1 + "\n")
            self.output.write("0;JMP\n")
        # For if-goto commands, we need to first check the top stack value and only jump if it is -1 (true)
        else:
            # first retrive the top stack value and store it in the D register
            self.output.write("@SP\nA=M-1\nD=M\n")
            # next we address the jump location that is the label stored in arg1 and jump if D is less than 0 
            self.output.write("@" + arg1 + "\nD;JLT\n")

    def writeComment(self, comment):
        self.output.write(comment)

    def writeBoolSubRoutine(self):
        self.output.write("(False)\n@SP\nA=M-1\nM=0\n@R13\nA=M\n0;JMP\n(True)\n@SP\nA=M-1\nM=-1\n@R13\nA=M\n0;JMP")

    def writeEndLoop(self):
        self.output.write("(LOOP)\n@LOOP\n0;JMP\n")

    def clean(self):
        self.output.close()