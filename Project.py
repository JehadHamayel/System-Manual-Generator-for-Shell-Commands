# Jehad Hamayel 1200348
import re
import shutil
import stat
import subprocess
import xml.etree.ElementTree as ET
import os
import xml.dom.minidom

# A class specialized in extracting command information from the Linux manual
class CommandManual:
    " When you create an Instant from it and give it a specific command name, this class creates the Manual content for the command "
    def __init__(self,command):
        self.command = command
    # Through this function, the command name is extracted and stored
    def getCommandName(self):
        "extracte the Name of the command"
        command1 = f""" man "{self.command}" """
        Name=""
        # Extract the name appropriately
        def extract_and_process_text(text):
            lines = text.split('\n')
            Name_to_DESCRIPTION = []
            in_range = False
            # Take the name where it falls between the NAME and the DESCRIPTION or SYNOPSIS in the man of the command
            for line in lines:
                if line.strip() == 'NAME':
                    in_range = True
                    continue  
                elif line.strip() == 'DESCRIPTION' or line.strip() == 'SYNOPSIS' :
                    break    
                elif in_range == True:
                    Name_to_DESCRIPTION.append(line)
                    
                    
            # Replace multiple spaces with a single space
            processed_lines = [' '.join(line.split()) for line in Name_to_DESCRIPTION]
            Name = '\n'.join(processed_lines)
            newLines=[]
            for line in Name.split('\n'):
                    if line.startswith(' '):
                        newLine = line[1:]
                        newLines.append(newLine)
                    else:
                        newLine = line
                        newLines.append(newLine)
            Name = '\n'.join(newLines)
            return Name
        try:
            # Execute the man command to extract the name of a specific command
            Name = subprocess.check_output(command1, shell=True, text=True)
            Name = f"""{Name}"""
            Name = extract_and_process_text(Name)
        # If the command fails to execute, the error will be dealt with    
        except subprocess.CalledProcessError as e:
            result = f"An error occurred: {e.output}"
            print (result)
        
        return Name
    # Through this function, the command DESCRIPTION is extracted and stored
    def getCommandDESCRIPTION(self):
        "extracte the DESCRIPTION of the command"
        command1 = f"""man "{self.command}" """
        DESCRIPTION=""
        # Extract the DESCRIPTION appropriately
        def extract_and_process_text(text, line_range=(1, 4)):
            lines = text.split('\n')
            description_to_options = []
            in_range = False

            # Extract lines between DESCRIPTION and OPTIONS or SEE ALSO(exclusive)
            for line in lines:
                if line.strip() == 'DESCRIPTION':
                    in_range = True
                    continue  # Skip the DESCRIPTION line
                if in_range and (line.strip() == 'OPTIONS' or line.strip() == 'SEE ALSO') :
                    break
                if in_range:
                    description_to_options.append(line)

            # get the range of the DESCRIPTION
            start, end = line_range
            start, end = start - 1, end 
            selected_lines = description_to_options[start:end]

            # Replace multiple spaces with a single space
            processed_lines = [' '.join(line.split()) for line in selected_lines]
            Description = '\n'.join(processed_lines)
            newLines=[]
            for line in Description.split('\n'):
                    if line.startswith(' '):
                        newLine = line[1:]
                        newLines.append(newLine)
                    else:
                        newLine = line
                        newLines.append(newLine)
            DESCRIPTION = '\n'.join(newLines)
            return DESCRIPTION
        try:
            # The man command is executed to extract the Description of the command
            DESCRIPTION = subprocess.check_output(command1, shell=True, text=True)
            Description = f"""{DESCRIPTION}"""
            DESCRIPTION = extract_and_process_text(Description)
            # Extract the desired Description in an organized manner
            if self.command == "grep":
                DESCRIPTION = extract_and_process_text(Description,line_range=(1, 100))
            elif self.command in [ "awk", "sed", "mv","find","cat","lscpu","lspci","column","rev"]:
                DESCRIPTION = extract_and_process_text(Description,line_range=(1, 4))
            elif self.command == "rename":
                DESCRIPTION = extract_and_process_text(Description,line_range=(1, 5))
            elif self.command in ["touch","tac","echo","printf","sort","uname","pwd"]:
                DESCRIPTION = extract_and_process_text(Description,line_range=(1, 2))
            elif self.command in ["chmod","id"]:
                DESCRIPTION = extract_and_process_text(Description,line_range=(1, 3))
            
        except subprocess.CalledProcessError as e:
            result = f"An error occurred: {e.output}"
            print (result)
        
        return DESCRIPTION
        
    # Through this function, the command VERSION is extracted and stored.
    def getCommandVERSION(self):
        "extracte the VERSION of the command"
        if self.command in ["grep","sed","mv","rename","touch","chmod","find","cat","tac","sort","uname","id","lspci","lscpu","rev","column"]:
            command1 = f"""{self.command} --version"""
        elif self.command == "awk":
            command1 = """awk -W version 2>&1"""
        elif self.command in ["echo", "printf","pwd"]:
            command1 = f"""vers=$(which {self.command}) && $vers --version """
        
        VERSION=""
        try:
            # Implementing the special command to extract the VERSION of the commnad
            VERSION = subprocess.check_output(command1, shell=True, text=True)
            if self.command in ["grep","awk","sed","mv","rename","touch","chmod","find","cat","tac","sort","echo", "printf","pwd","uname","id","lspci","lscpu"]:
                VERSION = VERSION.split('\n')[0]
            elif self.command == "rename":
                VERSION = re.search(r'File::Rename version (\d+\.\d+)', VERSION).group(1)
            elif self.command in ["rev","column"]:
                pass
        except subprocess.CalledProcessError as e:
            result = f"An error occurred:{self.command} {e.output}"
            print (result)
        
        return VERSION
    # Through this function, the command EXAMPLE with the output is extracted and stored.
    def getCommandEXAMPLE(self):
        "extracte the EXAMPLE with the output of the command"
        # An example is prepared and executed for each given command as follows
        if self.command == "grep":
            command1 = """ grep "Israel" Data1.txt """
            EXAMPLE='echo -e "The Israeli occupation is a brutal occupation\\nJerusalem is Palestines capital\\nIsrael is a war criminal" > Data1.txt'+"\n"+'grep "Israel" Data1.txt"'
        
        elif self.command == "awk":
            command1 ="""awk '/^Israel:$/,/^Palestine:$/' Data1.txt"""
            EXAMPLE='echo -e "Israel:\\nThe Israeli occupation is a brutal occupation\\nIsrael is a war criminal\\nPalestine:\\nJerusalem is Palestines capital" > Data1.txt '+"\n"+"awk '/^Israel:$/,/^Palestine:$/' Data1.txt"
        elif self.command == "sed":
            command1 ="""sed -n "2,3p" Data1.txt """
            EXAMPLE='echo -e "Israel:\\nThe Israeli occupation is a brutal occupation\\nIsrael is a war criminal\\nPalestine:\\nJerusalem is Palestines capital" > Data1.txt '+"\n"+'sed -n "2,3p" Data1.txt'
        elif self.command == "mv":
            # Prepare some files and things for the Command application
            with open('File1.txt', 'w') as file1:
                pass
            res1 = os.path.exists('File1.txt')
            
            command1 = """ mv File1.txt File2.txt"""
            
            res2 = os.path.exists('File1.txt')
            res3 = os.path.exists('File2.txt')
            if res1 and res3:
                res1 = "Zero"
                res3 = "Zero"
            if not res2 :
                res2 = "Positive " 			
            # Arrange the result to print and store
            res = f"output1(echo \$?):{res1}, output2(echo \$?):{res2}, output3(echo \$?):{res3}"
            
            EXAMPLE='touch File1.txt'+"\n"+'ls File1.txt > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+'mv File1.txt File2.txt'+"\n"+'ls File1.txt > /dev/null 2>&1'+"\n"+'echo $?' 
        elif self.command == "rename":
            # Prepare some files and things for the Command application
            with open('File1.csv', 'w') as file1:
                pass
            with open('File2.csv', 'w') as file2:
                pass

            res1 = os.path.exists('File1.csv')
            res2 = os.path.exists('File2.csv')
            command1 = """rename 's/\.csv$/.txt/' *.csv"""
            res3 = os.path.exists('File1.csv')
            res4 = os.path.exists('File2.csv')
            res5 = os.path.exists('File1.txt')
            res6 = os.path.exists('File2.txt')

            if res1 and res2 and res5 and res6:
                res1 = "Zero"
                res2 = "Zero"
                res5 = "Zero"
                res6 = "Zero"

            if not res2 :
                res3 = "Positive " 
                res4 = "Positive "
            # Arrange the result to print and store
            res = f"output1,2(echo \$?):{res1},{res2}, output3,4(echo \$?):{res3},{res4}, output5,6(echo \$?):{res5},{res6}"
            
            EXAMPLE='touch File1.csv'+"\n"+'touch File2.csv'+"\n"+'ls File1.csv > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+'ls File2.csv > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+"rename 's/\.csv$/.txt/' *.csv"+"\n"+'ls File1.csv > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+'ls File2.csv > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+'ls File1.txt > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+'ls File2.txt > /dev/null 2>&1'+"\n"+'echo $?'
        elif self.command == "touch":
            # Prepare some files and things for the Command application
            with open('File.txt', 'w') as file:
                pass
            res1 = os.path.exists('File.txt')
            command1 ="""touch File.txt"""
            res2 = os.path.exists('File.txt')
            if res2:
                res2 = "Zero"
            if res1:
                res1 = "Positive"
            # Arrange the result to print and store
            res=f"output1(echo \$?):{res1}, output2(echo \$?):{res2}"
            
            EXAMPLE='rm File.txt > /dev/null 2>&1'+"\n"+'ls File.txt > /dev/null 2>&1'+"\n"+'echo $?'+"\n"+'touch File.txt'+"\n"+'File.txt > /dev/null 2>&1'+"\n"+'echo $?'
        elif self.command == "find":
            # Prepare some files and things for the Command application
            os.mkdir("dirictore")
            with open('dirictore/File1.csv', 'w') as file1:
                pass
            with open('dirictore/File2.csv', 'w') as file2:
                pass
            command1 =""" find ./dirictore -type f -name "*.csv" """
            
            
            EXAMPLE= 'mkdir dirictore'+"\n"+'touch dirictore/file1.csv'+"\n"+'touch dirictore/file2.csv'+"\n"+'find . -type f -name "dirictore/*.csv"'
        elif self.command == "cat":
            with open('test.txt', 'w') as file1:
                file1.write("Hello World")
                pass
            command1 ="""cat test.txt """
            
            EXAMPLE='echo "Hello World" > test.txt'+"\n"+'cat test.txt'
        elif self.command == "rev":
            # Prepare some files and things for the Command application
            with open('test.txt', 'w') as file1:
                file1.write("Hello World\nGood Job")
                pass
            command1 ="""rev test.txt"""
            
            EXAMPLE='echo -e "Hello World\\nGood Job" > test.txt'+"\n"+'rev test.txt'
        elif self.command == "tac":
            # Prepare some files and things for the Command application
            with open('test.txt', 'w') as file1:
                file1.write("Hello World\nGood Job")
                pass
            command1 ="""tac test.txt"""
            
            EXAMPLE='echo -e "Hello World\\nGood Job" > test.txt'+"\n"+'rev test.txt'
        elif self.command == "echo":
            command1 ="""echo "Hello World\nGood Job" """
            EXAMPLE='echo -e "Hello World\\nGood Job"'
        elif self.command == "printf":
            command1 ="""printf "The hexadecimal value for %d is %x" 30 30 """
            EXAMPLE='printf "The hexadecimal value for %d is %x" 30 30'
        elif self.command == "column":
            # Prepare some files and things for the Command application
            with open('data.txt', 'w') as file1:
                file1.write("NAME: ID:\nJehadHamayel 1200348\nBasheerArouri 1201141")
                pass
            command1 ="""column -t data.txt """
            
            EXAMPLE='echo "NAME: ID:\\nJehadHamayel 1200348\\nBasheerArouri 1201141" > data.txt'+"\n"+'column -t data.txt'
        elif self.command == "sort":
            # Prepare some files and things for the Command application
            with open('data.txt', 'w') as file1:
                file1.write("JehadHamayel 1200348\nBasheerArouri 1201141\nAhmadNasser 1235556")
                pass
            command1 ="""sort data.txt"""
            
            EXAMPLE='echo "JehadHamayel 1200348\\nBasheerArouri 1201141\\nAhmadNasser 1235556" > data.txt'+"\n"+'sort data.txt'
        elif self.command == "chmod":
            # Prepare some files and things for the Command application
            with open('file', 'w') as file1:
                pass
            file_status = os.stat("file")
            # Extract the file permissions
            res1 = stat.filemode(file_status.st_mode)
    
            command1 ="""chmod +x file"""
        
            EXAMPLE= "rm file > /dev/null 2>&1"+"\n"+"touch file"+"\n"+"ls -l file | cut -d" " -f1 > touch"+"\n"+"res1=$(cat touch)"+"\n"+"chmod +x file"+"\n"+"ls -l file | cut -d" " -f1 > touch"+"\n"+"res2=$(cat touch)"+"\n"+'res="output1:"$res1", output2:"$res2'+"\n"+"echo $res "+"\n"+"rm touch" +"\n"+"rm file"
           
        elif self.command == "uname":
            command1 ="""uname"""
            EXAMPLE="""uname"""
        elif self.command == "pwd":
            command1 ="""pwd"""
            EXAMPLE="""pwd"""
        elif self.command == "id":
            command1 ="""id"""
            EXAMPLE="""id"""
        elif self.command == "lspci":
            command1 ="""lspci"""
            EXAMPLE="""lspci"""
        elif self.command == "lscpu":
            command1 ="""lscpu"""
            EXAMPLE="""lscpu"""
        
        try:     
            #Executing the command to extract results
            result = subprocess.check_output(command1, shell=True, text=True)
            if self.command in ["mv", "rename", "touch"]:
                result = res
        except subprocess.CalledProcessError as e:
            result = f"An error occurred: {e.output}"
            print (result)
        # Get rid of the files on which the experiment was performed
        if os.path.exists('File2.txt'):
            os.remove('File2.txt')
        if os.path.exists('File1.txt'):
            os.remove('File1.txt')
        if os.path.exists('File.txt'):
            os.remove('File.txt')    
        if os.path.exists("dirictore") and os.path.isdir("dirictore"):
            # Remove the directory and all its contents
            shutil.rmtree("dirictore")
        if os.path.exists('test.txt'):
            os.remove('test.txt') 
        if os.path.exists('data.txt'):
            os.remove('data.txt')
        if os.path.exists('file'):
            file_status = os.stat("file")
            # Extract the file permissions
            res2 = stat.filemode(file_status.st_mode)
            # Arrange the result to print and store
            res=f"output1:{res1}, output2:{res2}"
            result = res
            os.remove('file')
        return EXAMPLE,result
    
    # Through this function, the command Related Commands of The Command is extracted and stored.
    def getRelatedCommandsOfTheCommand(self):
        "extracte the RelatedCommandsOfTheCommand of the command"
        command1 = f"""bash -c ' compgen -c {self.command}'"""
        try:
            # Executing the command to extract results
            RelatedCommands = subprocess.check_output(command1, shell=True, text=True)
            RelatedCommandsOld = f"""{RelatedCommands}"""
            RelatedCommands=[]
            for line in RelatedCommandsOld.split('\n'):
                if line != "":
                    RelatedCommands.append(line)
            RelatedCommandsNew = list(set(RelatedCommands))
            RelatedCommands = ""
            for i in RelatedCommandsNew:
                RelatedCommands += i + "\n" 
            
        except subprocess.CalledProcessError as e:
            result = f"An error occurred: {e.output}"
            print(result)

        return RelatedCommands
# A class specialized in creating manuals for commands 
class CommandManualGenerator:
    "Through this function, all commands are passed through, and the manual data for each command is created."
    def __init__(self, commandsFile,type):
        self.commandsFile = commandsFile
        self.type = type
# Through this function, all commands are passed through, where the manual data for each command is created and sent to the XmlSerializer "
    def manualsGenerator(self):
        " Generat the commands manuals "
        with open(self.commandsFile,"r") as commands:
            # Prepare a file in order to use it in creating examples for commands
            DataForExamples = open("Data1.txt","w+")
            DataForExamples.write("Israel:\nThe Israeli occupation is a brutal occupation\nIsrael is a war criminal\nPalestine:\nJerusalem is Palestines capital")
            DataForExamples.close()
            os.makedirs(self.type, exist_ok=True)
            # Walk over all the commands and create their own manual
            for commandName in commands:
                command = commandName.strip()
                commandManual = CommandManual(command)
                # Create an XML file
                XmlSerializerCommand = XmlSerializer(commandManual,self.type)
                XMLFILE = XmlSerializerCommand.serialize()

                file_path = f"{self.type}/{commandManual.command}_Command_{self.type}.xml"
                
                # Write the XML string to the file
                with open(file_path, 'w') as file:
                    file.write(XMLFILE)

            os.remove("Data1.txt")    
            commands.close()
    # Through this function, a command manual is created for only one command   
    def manualsGeneratorForCommand(self,commandName):
        "Generate Command Manual for one command "
        DataForExamples = open("Data1.txt","w+")
        DataForExamples.write("Israel:\nThe Israeli occupation is a brutal occupation\nIsrael is a war criminal\nPalestine:\nJerusalem is Palestines capital")
        DataForExamples.close()
        os.makedirs("Commands", exist_ok=True)
        command = commandName.strip()
        commandManual = CommandManual(command)

        XmlSerializerCommand = XmlSerializer(commandManual,"Commands")
        XMLFILE = XmlSerializerCommand.serialize()

        file_path = f"Commands/{commandManual.command}_Command_Commands.xml"
        
        #    Write the XML string to the file
        with open(file_path, 'w') as file:
            file.write(XMLFILE)
        yes_or_no = input("Do you want to show the contant of the manual (yes or enter any thing for no)? ")
        if yes_or_no == "yes":
            XmlSerializerCommand.readXMLFile()
            print("\n--------------------------------------------------------------------------------------\n")
        os.remove("Data1.txt")

# A class specialized in creating and reading an XML file
class XmlSerializer:
    "Create and reading XML files"
    def __init__(self,commandManual,type):
        self.command = commandManual.command
        self.commandName = commandManual.getCommandName()
        self.type=type
        self.DESCRIPTION = commandManual.getCommandDESCRIPTION()
        self.VERSION = commandManual.getCommandVERSION()
        self.EXAMPLE,self.OUTPUTOFEXAMPLE=commandManual.getCommandEXAMPLE()
        self.RelatedCommands = commandManual.getRelatedCommandsOfTheCommand()
    # :  Function specializes in creating an XML file, where it arranges the data inside it in an orderly, beautiful, and hierarchical manner
    def serialize(self):
       "Creating an XML file" 
       rootFile = ET.Element(f"Command_Manual_of_{self.command}_command")
       ET.SubElement(rootFile, "Name").text = self.commandName
       ET.SubElement(rootFile, "Description").text = self.DESCRIPTION
       ET.SubElement(rootFile, "Version").text = self.VERSION
       ET.SubElement(rootFile, "Example").text = self.EXAMPLE
       ET.SubElement(rootFile, "Output_of_the_Example").text = self.OUTPUTOFEXAMPLE
       ET.SubElement(rootFile, "Related_Commands").text = self.RelatedCommands

       commandXML = ET.tostring(rootFile)
       notPrettyxml = xml.dom.minidom.parseString(commandXML)
       # Arrange the file beautifully
       Prettyxml = notPrettyxml.toprettyxml()
       return Prettyxml
    # Function specializes in reading XML files and printing their content.
    def readXMLFile(self):
        "reading XML files and printing their content"
        CommandManualXMLFILE = xml.dom.minidom.parse(f"{self.type}/{self.command}_Command_{self.type}.xml")
        COMAND = CommandManualXMLFILE.documentElement
         
        command = COMAND.getElementsByTagName('Name')[0].childNodes[0].nodeValue
        DESCRIPTION = COMAND.getElementsByTagName('Description')[0].childNodes[0].nodeValue
        VERSION = COMAND.getElementsByTagName('Version')[0].childNodes[0].nodeValue
        EXAMPLE= COMAND.getElementsByTagName('Example')[0].childNodes[0].nodeValue
        OUTPUTOFEXAMPLE= COMAND.getElementsByTagName('Output_of_the_Example')[0].childNodes[0].nodeValue
        RelatedCommands = COMAND.getElementsByTagName('Related_Commands')[0].childNodes[0].nodeValue
        print("\n--------------------------------------------------------------------------------------\n")
        print(f"{self.command} Manual:\n\n")
        print("\nName:\n")
        print(f"{command}")
        print("\nDESCRIPTION:\n")
        print(f"{DESCRIPTION}")
        print("\nVERSION:\n")
        print(f"{VERSION}")
        print("\nEXAMPLE:\n")
        print(f"{EXAMPLE}")
        print("\nOUTPUT OF EXAMPLE:\n")
        print(f"{OUTPUTOFEXAMPLE}")
        print("\nRelatedCommands:\n")
        print(f"{RelatedCommands}")
# It is a function that creates lists so that they are classified based on functionality.
def recomndation(commandsFile,rename_Array,Filtering_Search_Scanning_Array,Change_Modifay_Array,Sort_In_spicificWay,Print_Standard):
    directory_path = commandsFile

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        command = filename.split('_')[0]+"_"+filename.split('_')[1]  
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                # Iterate over each line in the file
                flag1=False
                flag2=False
                flag3=False
                flag4=False
                flag5=False
                for line_number, line in enumerate(file, start=1):
                    # Check if the word is in the line
                    if "rename" in line:
                        flag1=True
                    if "scan" in line or "search" in line or "filter" in line:
                        flag2 = True  
                    if "change" in line :
                        flag3 = True  
                    if "sort" in line or "lines" in line or "reverse" in line:
                        flag4 = True
                    if "print" in line or "display" in line or "standard output" in line or "list " in line:
                        flag5 = True
                if flag1:
                    rename_Array.append(command)
                if flag2:
                    Filtering_Search_Scanning_Array.append(command)
                if flag3:
                    Change_Modifay_Array.append(command)
                if flag4:
                    Sort_In_spicificWay.append(command)
                if flag5:
                    Print_Standard.append(command)
                
                    
# Function prints the commands index divided by functionality
def commands_index(rename_Array,Filtering_Search_Scanning_Array,Change_Modifay_Array,Sort_In_spicificWay,Print_Standard):
    print("Special commands for printing, display, standard output, and listing information:")
    for num, command in enumerate(Print_Standard,start=1):
        print(f"{num}) {command}")
    print("\nSpecial commands in sorting and printing in specific way:")
    for num, command in enumerate(Sort_In_spicificWay,start=1):
        print(f"{num}) {command}")
    print("\nSpecial commands for creating files and changing the file mode:")
    for num, command in enumerate(Change_Modifay_Array,start=1):
        print(f"{num}) {command}")
    print("\nSpecial commands in filtering, searching, and scanning:")
    for num, command in enumerate(Filtering_Search_Scanning_Array,start=1):
        print(f"{num}) {command}")
    print("\nSpecial commands in renaming and moving the file location:")
    for num, command in enumerate(rename_Array,start=1):
        print(f"{num}) {command}")
# Function searches for the specific manual in a specific command and then prints it   
def SearchForCommand(commandsFile,SearchedCommand,rename_Array,Filtering_Search_Scanning_Array,Change_Modifay_Array,Sort_In_spicificWay,Print_Standard):
    directory_path = commandsFile
    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        Command = filename.split('_')[0]+"_"+filename.split('_')[1]
        # Check if it's a file and not a directory
        if os.path.isfile(file_path) and (Command == (SearchedCommand+"_Command")):
            print("the command founded")
            CommandManualXMLFILE = xml.dom.minidom.parse(file_path)
            COMAND = CommandManualXMLFILE.documentElement
            command = COMAND.getElementsByTagName('Name')[0].childNodes[0].nodeValue
            DESCRIPTION = COMAND.getElementsByTagName('Description')[0].childNodes[0].nodeValue
            VERSION = COMAND.getElementsByTagName('Version')[0].childNodes[0].nodeValue
            EXAMPLE= COMAND.getElementsByTagName('Example')[0].childNodes[0].nodeValue
            OUTPUTOFEXAMPLE= COMAND.getElementsByTagName('Output_of_the_Example')[0].childNodes[0].nodeValue
            RelatedCommands = COMAND.getElementsByTagName('Related_Commands')[0].childNodes[0].nodeValue 
            print("\n--------------------------------------------------------------------------------------\n")
            print(f"{SearchedCommand} Manual:\n\n")
            print("\nName:\n")
            print(f"{command}")
            print("\nDESCRIPTION:\n")
            print(f"{DESCRIPTION}")
            print("\nVERSION:\n")
            print(f"{VERSION}")
            print("\nEXAMPLE:\n")
            print(f"{EXAMPLE}")
            print("\nOUTPUT OF EXAMPLE:\n")
            print(f"{OUTPUTOFEXAMPLE}")
            print("\nRelatedCommands:\n")
            print(f"{RelatedCommands}")
            
            print("The Recommended Commands:")
            # Apply the recommendation feature
            if Command in rename_Array:
                for commandIn in rename_Array:
                    print("\nSpecial commands in renaming and moving the file location:")
                    print(commandIn)
            if Command in Filtering_Search_Scanning_Array:
                print("\nSpecial commands in filtering, searching, and scanning:")
                for commandIn in Filtering_Search_Scanning_Array:
                    print(commandIn)
            if Command in Change_Modifay_Array:
                print("\nSpecial commands for creating files and changing the file mode:")
                for commandIn in Change_Modifay_Array:
                    print(commandIn)
            if Command in Sort_In_spicificWay:
                print("\nSpecial commands in sorting and printing in specific way:")
                for commandIn in Sort_In_spicificWay:
                    print(commandIn)
            if Command in Print_Standard:
                print("\nSpecial commands for printing, display, standard output, and listing information:")
                for commandIn in Print_Standard:
                    print(commandIn)
            print("_______________________")
            return
    # If the command is not present, we will prepare a command similar to the one for which the manual was made
    print("the command found Not founded")
    flagPrint = False
    for filename in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        command = filename.split('_')[0]+"_"+filename.split('_')[1]
        # Check if it's a file and not a directory
        if os.path.isfile(file_path) :
            CommandManualXMLFILE = xml.dom.minidom.parse(file_path)
            COMAND = CommandManualXMLFILE.documentElement
            RelatedCommands = COMAND.getElementsByTagName('Related_Commands')[0].childNodes[0].nodeValue
            RelatedCommands = RelatedCommands.split("\n")
            if SearchedCommand in RelatedCommands :
                if flagPrint == False:
                    print("The Recommended Commands:")
                    flagPrint = True
                print(command)
    
    command1 = f"""bash -c ' compgen -c {SearchedCommand}'"""
    try:
        RelatedCommands = subprocess.check_output(command1, shell=True, text=True)
        RelatedCommandsOld = f"""{RelatedCommands}"""
        RelatedCommands = []
        for line in RelatedCommandsOld.split('\n'):
            if line != "":
                RelatedCommands.append(line)
        RelatedCommandsNew = list(set(RelatedCommands))
        RelatedCommands = ""
        for i in RelatedCommandsNew:
            if flagPrint == False:
                print("The Recommended Commands:")
                flagPrint = True
            print(i)   
    except subprocess.CalledProcessError as e:
        result = f"An error occurred: {e.output}"

# Verify the correctness of the generated content.
def Verification(VerificationedCommand,commandsFile):
    directory_path = commandsFile
    Verifed = True
    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        command = filename.split('_')[0]+"_"+filename.split('_')[1]
        # Check if it's a file and not a directory
        if os.path.isfile(file_path) and (command == (VerificationedCommand+"_Command")):
            
            VerificationCommandManualXMLFILE = xml.dom.minidom.parse(file_path)
            VerificationCOMAND = VerificationCommandManualXMLFILE.documentElement
            Verificationcommand = VerificationCOMAND.getElementsByTagName('Name')[0].childNodes[0].nodeValue
            VerificationDESCRIPTION = VerificationCOMAND.getElementsByTagName('Description')[0].childNodes[0].nodeValue
            VerificationVERSION = VerificationCOMAND.getElementsByTagName('Version')[0].childNodes[0].nodeValue
            VerificationEXAMPLE= VerificationCOMAND.getElementsByTagName('Example')[0].childNodes[0].nodeValue
            VerificationOUTPUTOFEXAMPLE= VerificationCOMAND.getElementsByTagName('Output_of_the_Example')[0].childNodes[0].nodeValue
            VerificationRelatedCommands = VerificationCOMAND.getElementsByTagName('Related_Commands')[0].childNodes[0].nodeValue
            
            CommandManualXMLFILE = xml.dom.minidom.parse(f"Commands/{command}_Commands.xml")
            COMAND = CommandManualXMLFILE.documentElement
            command = COMAND.getElementsByTagName('Name')[0].childNodes[0].nodeValue
            DESCRIPTION = COMAND.getElementsByTagName('Description')[0].childNodes[0].nodeValue
            VERSION = COMAND.getElementsByTagName('Version')[0].childNodes[0].nodeValue
            EXAMPLE= COMAND.getElementsByTagName('Example')[0].childNodes[0].nodeValue
            OUTPUTOFEXAMPLE= COMAND.getElementsByTagName('Output_of_the_Example')[0].childNodes[0].nodeValue
            RelatedCommands = COMAND.getElementsByTagName('Related_Commands')[0].childNodes[0].nodeValue 

            # Compare the two files and print the difference, if any
            if  Verificationcommand != command:
                Verifed = False
                print("Not Verifed in command Name")
                print("command Name Before:") 
                print(command)
                print("command Name After:") 
                print(Verificationcommand) 
            if  VerificationDESCRIPTION != DESCRIPTION:
                Verifed = False
                print("Not Verifed in command DESCRIPTION")
                print("command DESCRIPTION Before:") 
                print(DESCRIPTION)
                print("command DESCRIPTION After:") 
                print(VerificationDESCRIPTION)
            if  VerificationVERSION != VERSION:
                Verifed = False
                print("Not Verifed in command VERSION")
                print("command VERSION Before:") 
                print(VERSION)
                print("command VERSION After:") 
                print(VerificationVERSION)
            if  VerificationOUTPUTOFEXAMPLE != OUTPUTOFEXAMPLE:
                Verifed = False
                print("Not Verifed in OUTPUT OF command EXAMPLE")
                print("command EXAMPLE:")
                print(EXAMPLE)
                print("command OUTPUT OF command EXAMPLE Before:") 
                print(OUTPUTOFEXAMPLE)
                print("command OUTPUT OF command EXAMPLE After:") 
                print(VerificationOUTPUTOFEXAMPLE)
            if  VerificationRelatedCommands != RelatedCommands:
                Verifed = False
                print("Not Verifed in RelatedCommands of the command")
                print("atedCommands of the command Before:") 
                print(RelatedCommands)
                print("atedCommands of the command After:") 
                print(VerificationRelatedCommands)
            if Verifed == True:
                print("Verifed command")
            return
    print("The command not found")



flagRec= False
flagExit = False
while True:
    commandsFile = input("Enter the name of an input file: ") 
    if os.path.exists(commandsFile):
        # Check if the file is not empty
        if os.path.getsize(commandsFile) > 0:
            print ("Choose what you want from the following list by choosing the number of it:")
            print ("1)Generate Linux/Unix Commands Manual")
            print ("2)Verification The Commands.")
            print ("3)Print the Commands index.")
            print ("4)Search for Command.")
            print ("5)exit")
            choice = input("Choose: ")
            
            while True:
                
                if os.path.isdir("Commands") and not flagRec:
                    
                    flagRec = True
                    rename_Array=[]
                    Filtering_Search_Scanning_Array=[]
                    Change_Modifay_Array=[]
                    Sort_In_spicificWay=[]
                    Print_Standard=[]
                    recomndation("Commands",rename_Array,Filtering_Search_Scanning_Array,Change_Modifay_Array,Sort_In_spicificWay,Print_Standard)
                if choice == "1":
                    print ("Choose what you want from Generate Linux/Unix Command Manual:")
                    print ("1)Generate Linux/Unix Command Manual For all commands.")
                    print ("2)Generate Linux/Unix Command Manual For one command.")
                    print ("3)exit")
                    choice2 = input("Choose: ")
                    while True:
                        CommandManualGenerator1 = CommandManualGenerator(commandsFile,"Commands")

                        if choice2 == "1":
                            print ("Please wait for the files of the Commands Manuals to be created")
                            CommandManualGenerator1.manualsGenerator()
                            flagRec = False
                            print ("__________________________________________________________________________________________")
                            print ("The Generation of the Commands Manuals Done")
                            print ("__________________________________________________________________________________________")
                        elif choice2 == "2":
                            command = input("Choose command: ")
                            print ("Please wait for the files of the Command Manual to be created")
                            CommandManualGenerator1.manualsGeneratorForCommand(command)

                            flagRec = False
                            print ("__________________________________________________________________________________________")
                            print ("The Generation of the Command Manual Done")
                            print ("__________________________________________________________________________________________")
                        elif choice2 == "3":
                            break
                        print ("Choose what you want from Generate Linux/Unix Command Manual:")
                        print ("1)Generate Linux/Unix Command Manual For all commands.")
                        print ("2)Generate Linux/Unix Command Manual For one command.")
                        print ("3)exit")
                        choice2 = input("Choose: ")
                    
                elif choice == "2":
                    if not os.path.isdir("Commands"):
                        print ("Please Generate Linux/Unix Command Manual First")
                            
                    else:
                        print ("Please wait for the files of the Verificate Commands Manuals to be created")
                        CommandManualGenerator2 = CommandManualGenerator(commandsFile,"Verification")
                        CommandManualGenerator2.manualsGenerator()
                        print ("Choose what you want from Verification Commands:")
                        print ("1)Verification Linux/Unix Command Manual For all commands.")
                        print ("2)Verification Linux/Unix Command Manual For one command.")
                        print ("3)exit")
                        while True:
                            choice2 = input("Choose: ")
                            if choice2 == "1":

                                with open(commandsFile,"r") as commands:
                                    for commandName in commands: 
                                        commandName = commandName.strip()
                                        print ("__________________________________________________________________________________________")
                                        print(f"Verification For {commandName} command")
                                        Verification(commandName,"Verification")
                                        print ("__________________________________________________________________________________________")
                                print ("__________________________________________________________________________________________")
                                print ("The Verification of the Commands Manuals Done")
                                print ("__________________________________________________________________________________________")
                            elif choice2 == "2":
                                commandName = input("Choose command: ")
                                commandName = commandName.strip()
                                print ("__________________________________________________________________________________________")
                                print(f"Verification For {commandName} command")
                                Verification(commandName,"Verification")
                                print ("__________________________________________________________________________________________")
                                print ("The Verification of the Command Manual Done")
                                print ("__________________________________________________________________________________________")
                            elif choice2 == "3":
                                break
                            print ("Choose what you want from Verification Commands:")
                            print ("1)Verification Linux/Unix Command Manual For all commands.")
                            print ("2)Verification Linux/Unix Command Manual For one command.")
                            print ("3)exit")
                        
                    
                    
                elif choice == "3":
                    if not os.path.isdir("Commands"):
                        print ("Please Generate Linux/Unix Command Manual First")
                    else:
                        commands_index(rename_Array,Filtering_Search_Scanning_Array,Change_Modifay_Array,Sort_In_spicificWay,Print_Standard)
                        
                elif choice == "4":
                    if not os.path.isdir("Commands"):
                        print ("Please Generate Linux/Unix Command Manual First")     
                    else:
                        SearchCommand=input("Enter The name of the command that you want to find:")
                        SearchCommand = SearchCommand.strip()
                        print(SearchCommand)
                        SearchForCommand("Commands",SearchCommand,rename_Array,Filtering_Search_Scanning_Array,Change_Modifay_Array,Sort_In_spicificWay,Print_Standard)
                elif choice == "5":
                    flagExit = True
                    break
                else: 
                    print("Please choose one of the choices") 
                print ("Choose what you want from the following list by choosing the number of it:")
                print ("1)Generate Linux/Unix Commands Manual")
                print ("2)Verification The Commands.")
                print ("3)Print the Commands index.")
                print ("4)Search for Command.")
                print ("5)exit")
                choice = input("Choose: ")
            if flagExit:
                break
            
        else:
            print("File exists but is empty.")
    else:
        print("File does not exist.")



