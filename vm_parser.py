from constants import *

class Parser:
    
    def __init__(self, filepath):
        try:
            self.input_file = open(filepath, 'r')
            # this will be the value that indicates the EOF
            self.EOF = self.input_file.seek(0, 2)
            # must return to the begining of the file
            self.input_file.seek(0)
        except Exception as e:
            print(e)
        self.current_command = None
   
    """
    Returns true when the file has more commands to be parsed, false otherwise.
    """
    def hasMoreCommands(self):
        return not (self.input_file.tell() == self.EOF)
    
    def advance(self):
        while(True):
            if self.hasMoreCommands():
                self.current_command = self.input_file.readline()
                # if the current 'command' is a comment or empty line we want to continue with the loop
                if self.current_command[0] in ["/", "\n"]:
                    continue
                else:
                    break
            else:
                self.current_command = None
                break

    def commandType(self):
        c_type = self._parse_fields()[0]
        if c_type in STACK_OPERATIONS:
            if c_type == 'push':
                return CommandType.C_PUSH
            else:
                return CommandType.C_POP
        elif c_type in ARITHMETIC_OPERATIONS:
            return CommandType.C_ARITHMETIC
    
    def arg1(self):
        cmd = self._parse_fields()
        cmd_type = self.commandType()
        if cmd_type == CommandType.C_RETURN:
            return
        elif cmd_type == CommandType.C_ARITHMETIC:
            return cmd[0]
        else:
            return cmd[1]
        
    def arg2(self):
        cmd = self._parse_fields()
        cmd_type = self.commandType()
        if cmd_type not in [CommandType.C_POP, CommandType.C_PUSH, CommandType.C_FUNCTION, CommandType.C_CALL]:
            return
        else:
            return cmd[2]

    def _parse_fields(self):
        if self.current_command != None:
            fields = self.current_command.split(" ")
        # in the event there is a in-line comment we remove it
        if len(fields) >= 3:
            fields = fields[:3]
            fields[2] = fields[2].strip("\n")
        # here we remove the '\n' from arithmetic operations
        if len(fields) == 1:
            fields[0] = fields[0].strip("\n")
        return fields
    
    def clean(self):
        self.input_file.close()