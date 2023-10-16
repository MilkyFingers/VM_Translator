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

    def writeComment(self, comment):
        self.output.write(comment)

    def writeBoolSubRoutine(self):
        self.output.write("(False)\n@SP\nA=M-1\nM=0\n@R13\nA=M\n0;JMP\n(True)\n@SP\nA=M-1\nM=-1\n@R13\nA=M\n0;JMP")

    def writeEndLoop(self):
        self.output.write("(LOOP)\n@LOOP\n0;JMP\n")

    def clean(self):
        self.output.close()