# VM_Translator
Translates jack bytecode to hack assembly

To use the application on a Unix-like system;
1) Copy the vm.zip into some directory and run the following commands:

   echo '#!/usr/bin/python3' | cat - vm.zip > vmt
   chmod +x vmt

3) You should now have an exec called vmt that takes a source file foo.vm (in the current directory) and outputs a file foo.asm
4) To make the application accesible from any directory you can copy it into the /usr/local/bin folder on your system
