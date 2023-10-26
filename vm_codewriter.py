from constants import *
import uuid

class CodeWriter:
    
    def __init__(self, outputfile, directory=None):
        try:
            self.output = open(outputfile, "w")
        except:
            print("Could not open a file stream for output file!")
        # here 'None' value will be replaced with the computation
        self.file = outputfile.strip('.asm')
        # The first thing we do is write the bootstap code if the directory argument is a 1
        if directory != None:
            ins = "@256\nD=A\n@SP\nM=D\n"
            self.output.write(ins)
            self.writeCall("Sys.init", "0")

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
            # first retrive the top stack value and store it in the D register and decrement the stack pointer
            self.output.write("@SP\nM=M-1\nA=M\nD=M\n")
            # next we address the jump location that is the label stored in arg1 and jump if D is less than 0 
            self.output.write("@" + arg1 + "\nD;JNE\n")

    def writeFunction(self, arg1, arg2):
        # step 1 is to inject a label into the program signalling the start of the function
        ins = "(" + arg1 + ")\n"
        # next we have to add local args (the number of these is arg2) onto the stack and increment the stack pointer. i is LCL offset
        for i in range(int(arg2)):
            ins += "@SP\nM=M+1\n@"+str(i)+"\nD=A\n@LCL\nA=M\nA=D+A\nM=0\n"
        self.output.write(ins)

    def writeReturn(self):
        # First we must save the value of the return address which is stored at LCL - 5. We will save this value in R14
        ins = "@5\nD=A\n@LCL\nA=M\nA=A-D\nD=M\n@R14\nM=D\n"
        # Next, the top value of the stack should be saved as this is the return value of the callee
        ins += "@SP\nA=M-1\nD=M\n"
        # Next, we want to copy this value into the callees ARG[0]
        ins += "@ARG\nA=M\nM=D\n"
        # Next, we want to set the value of SP to ARG + 1
        ins += "@ARG\nA=M\nD=A+1\n@SP\nM=D\n"
        # Finally, we must restore the callers values of THAT, THIS, ARG and LCL which are stored at LCL-1, LCL-2, LCL-3 and LCL-4 respectively
        # Restore THAT
        ins += "@LCL\nA=M\nA=A-1\nD=M\n@THAT\nM=D\n"
        # Restore THIS
        ins += "@2\nD=A\n@LCL\nA=M\nA=A-D\nD=M\n@THIS\nM=D\n"
        # Restore ARG
        ins += "@3\nD=A\n@LCL\nA=M\nA=A-D\nD=M\n@ARG\nM=D\n"
        # Restore LCL
        ins+= "@4\nD=A\n@LCL\nA=M\nA=A-D\nD=M\n@LCL\nM=D\n"
        # Finally, we jump to the return address that we stored in R14
        ins += "@R14\nA=M\n0;JMP\n"
        self.output.write(ins)

    def writeCall(self, function_name, nArgs):
        # The first thing to do is to create a label that will be used as the return address once the function call is completed and increment SP
        retAdd = str(uuid.uuid1())
        ins = "@" + retAdd + "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n"
        # Next, we must save the callers values for LCL, ARG, THIS and THAT and increment the SP by 4
        ins += "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        ins += "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        ins += "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        ins += "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
        # Next, we have to reposition the values of ARG and LCL for the callee
        # Arg is located at @retAdd - nArgs
        ins += "@5\nD=A\n@" + nArgs + "\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n"
        # LCL is set to the value of the SP
        ins += "@SP\nD=M\n@LCL\nM=D\n"
        # Lastly, we jump to the function
        ins += "@" + function_name + "\n0;JMP\n"
        ins += "(" + retAdd + ")\n"
        self.output.write(ins)


    def writeComment(self, comment):
        self.output.write(comment)

    def writeBoolSubRoutine(self):
        self.output.write("(False)\n@SP\nA=M-1\nM=0\n@R13\nA=M\n0;JMP\n(True)\n@SP\nA=M-1\nM=-1\n@R13\nA=M\n0;JMP")

    def writeEndLoop(self):
        self.output.write("(LOOP)\n@LOOP\n0;JMP\n")

    def clean(self):
        self.output.close()