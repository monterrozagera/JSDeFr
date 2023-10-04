# TODO: add YARA RULES integration, base64decode, bruteforce
# controlFlowFlattening eg. _0x342234{ 'first': 0x8213(234, 556) } console[0x8213(234, 522)](_0x342234['first])
# FUTURE: mode 3 0x23gb3(333, 777, 888, 999)
#         custom mode (choose args amount, and custom logic)
from colorama import init, Back
# from choice_handle import printChoicesList
from os import path, remove
from pathlib import Path
import random
import argparse
import sys
import re

secrets = ["pipedream", "write", "request", "3044484VIkopN", "1494870HmjQPZ", "end", "from", "60wiAlld", "join", "45728YyfwUd", "net", "https", "5752425cLNRTk", "2017728jHpKdM", "3f241964ab40f0d30260cde55e73b9e4", "POST", "9017196hRyHpo", "base64", "337281XfTlIH", "npm_package_name", "toString", "stringify"]

regex = [r'[a-zA-Z_]*0*_*0x[\da-zA-Z]{1,9}\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,}),\s*(-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'] ## 2 digit
regex2 = [r'[a-zA-Z]*0*_*0x[\da-zA-Z]{1,9}\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'] ## 1 digit
magic_number = 0

class Array_Replace:
    """ Handles different kinds of array-based deobfuscation. """
    def __init__(self, rgx, script_in: str, script_out: str, secrets=[], hex_translate=False, base64_decode=False):
        self.s_name = script_in
        self.o_name = script_out 
        self.s_array = secrets
        self.regex = rgx
        self.t_hex = hex_translate
        self.base64decode = base64_decode

        self.printScriptName()
        if self.t_hex:
            self.hexReplace()
        if not self.s_array:
            self.s_array = self.getSecretsArray()
            if not self.s_array:
                print(Back.RED + "[!] Could not find secrets array, manually replace secrets = [] in script.")
                sys.exit(0)

        self.printSecretsArray()

    def printScriptName(self):
        """ Prints name of the loaded JS script to the screen """
        print(f'[*] Loaded script: {self.s_name}')

    def printSecretsArray(self):
        """ Prints secrets array to the screen """
        new = '['
        limit = 5
        for i in self.s_array:
            new += i + ','
            limit -= 1
            if not limit:
                new += '...'
                break

        print(f'[*] Secrets array: {new}')


    def countIntances(self, regex_to_count) -> int:
        """ Counts the times that the given argument is referenced """
        """ in the script. """
        count = 0
        lines = self.openScript(self.s_name)
        count = len(re.findall(regex_to_count, lines))

        return count


    def hexReplace(self):
        """ Replaces all hex digits to decimals. """
        hex_regex = r'\b0x[0-9A-Fa-f]{1,5}'
        ele = []
        clean = []

        with open(self.s_name, 'r') as wb: ## replace name
            lines = wb.read()
            matches = re.findall(hex_regex, lines)

            for item in matches:
                ele.append(item)
            for item in ele:
                clean.append(int(item, 16))

            try:
                for item in clean:
                    lines = re.sub(hex_regex, str(item), lines, count=1)
            except re.error:
                pass
            
        with open(self.o_name, 'w') as wb:
            wb.write(lines)

        self.s_name = self.o_name

    def getSize(self):
        """ Prints size of the file in KB. """
        kb_size = Path(self.s_name).stat().st_size / 1000
        print(f"[*] Size: {kb_size}KB")

    def beautify(self):
        """ Reformats the script to add newlines and tabs. """
        with open(self.s_name, 'r') as wb: ## replace name
            contents = wb.read()

            tabs = ''
            beautified = ''  

            for c in contents:
                if c == '{':       
                    tabs += '\t'
                    beautified += f'{c}\n' + tabs
                elif c == ';':
                    beautified += f'{c}\n' + tabs
                elif c == '}':
                    brackets_handler = -abs(len(tabs)) + -abs(len(tabs)) # fix to handle brackets {} correctly
                    if beautified[brackets_handler] == '{':
                        beautified = beautified[:brackets_handler] + '{}'
                    else:
                        tabs = tabs[:-1]
                        if beautified[-2] == '}':
                            beautified += f'{tabs}{c}\n'
                        else:
                            beautified = beautified[:-1] + f'{c}\n{tabs}'
                elif c == '=' and beautified[-1] != '=':
                    beautified += f' {c}'
                elif c ==',':
                    beautified += f'{c}'
                elif c == ']':
                    if beautified[-3:] == "!![":
                        beautified = beautified [:-3] + 'true'
                    else:
                        beautified += c
                else:
                    try:
                        if c != '=' and beautified[-1] == '=':
                            beautified += f' {c}'
                        else:
                            beautified += c
                    except IndexError:
                        beautified += c
            
        with open(self.o_name, 'w') as wb:
            wb.write(beautified)

        self.s_name = self.o_name
        print(Back.GREEN + "[!] Beautified script")
        print(Back.YELLOW + "[!!] Beware of any broken { } or ; instances")

    def getSecretsArray(self) -> list:
        """ Attempts to get secrets array. """
        with open(self.s_name, 'r') as wb:
            contents = wb.read()

            count = 0
            array = ''
            for c in contents:
                if c == ' ' or c == '\n':
                    pass
                elif c == '[':
                    count = 1
                elif count > 100:
                    if c != ']':
                        array += c
                    elif c == ']':
                        array += ','
                        return self.splitSecretsArray(array)
                elif c == ']' and count < 100:
                    count = 0
                    array = ''
                elif count > 0:
                    count += 1
                    array += c

    def getMagicNumber(self) -> int:
        """ Attempts to get magic number. """
        regex = r'=*\s*[a-zA-Z]*0*_*0x[\da-zA-Z]{1,9}\s*-\s*\b0*x*[0-9A-Fa-f]{1,5};'

        with open(self.s_name, 'r') as wb:
            contents = wb.read()
            magic_number = re.findall(regex, contents)

            if magic_number:
                magic_number = magic_number[0].split('-')
                magic_number = re.findall(r'^\s*\d+', magic_number[1])
                print(f"[*] Magic number: {int(magic_number[0])}")
                return int(magic_number[0])
            else:
                print(Back.RED + "[!] Could not find magic number.")
                return 0
            

    def splitSecretsArray(self, s_array: str) -> list:
        """ Splits string extracted from getSecretsArray into a usable array. """
        regex = r"[a-zA-Z:()+.\\[\*\?\{\}\]$_\\\s\d\/]{1,80}"
        try:
            secrets = re.sub(r'\\x20', ' ', s_array)
            secrets = re.findall(regex, secrets)
            print("[!] Found secrets array.")

            return secrets
        except:
            print(Back.RED + "[!] Error splitting secrets array. ")

    def concatString(self):
        """ Concatenate split strings from script. """
        with open(self.s_name, 'r') as wb:
            contents = wb.read()

            concatenated = ''
            for c in contents:
                if c == "'" and concatenated[-2:] == "'+":
                    concatenated = concatenated[:-2]
                else:
                    concatenated += c

        with open(self.o_name, 'w') as wb:
            wb.write(concatenated)


    def parseInt(self, secret_item: str) -> int:
        """ Python version of javascript's parseInt() """
        secret_item = re.findall(r'^\d+', secret_item)
        result = ''.join(secret_item) ## check this for errors

        if not result:
            return '0'

        return result


    def pushShift(self, array: list) -> list:
        """ Python version of javascript's [push][shift]: add element from the front to the end of the array """
        front = array[0]
        new = array[1:]
        
        new.append(front)
        return new

    def controlFlowReconstruct(self):
        """ let's first assume we can somehow identify objects in a super-obfuscated Javascript file """
        regex_call = r"[a-zA-Z]*0*_*0x[\da-zA-Z]{1,9}\['[a-zA-Z]{,5}'\]"
        regex_var = r"[a-zA-Z]*0*_*0x[\da-zA-Z]{1,9}"

        print(f"Intances: {self.countIntances(regex_call)}")

    def openScript(self, name_of_script) -> str:
        """ replace boilerplate code for opening JS file as string, return as str """
        full_lines = ''
        with open(name_of_script, 'r') as wb:
            full_lines = wb.read()

        return full_lines

    def decodeB64(self):
        """ Decodes base64 encoding. """
        pass
        
class mode_1(Array_Replace):
    """ Mode 1: Simple array obfuscation with functions of type _0x0000(digit) """ 
    """ regex example: r'_0x446cb2\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'"""
    def __init__(self, rgx, script_in: str, script_out: str, magic_num, secrets: list, hex_translate=False, base64_decode=False):
        super().__init__(rgx, script_in, script_out, secrets, hex_translate, base64_decode)
        self.m_number = magic_num

        if not self.m_number:
            self.m_number = self.getMagicNumber()

    def replace_js(self):
        """ Opens JS script, returns new file with replaced values. """
        ele = []
        clean = []

        for obfs in self.regex:
            with open(self.s_name, 'r') as wb: ## replace name
                lines = wb.read()
                matches = re.findall(obfs, lines)

                for item in matches:
                    ele.append(item)
                for item in ele:
                    clean.append(self.logic_js(number_1=int(item), new_secrets=self.s_array))

                try:
                    for item in clean:
                        lines = re.sub(obfs, "'" + item + "'", lines, count=1)
                except re.error as e:
                    print(Back.RED + '[!!] Error replacing some instances')
                    print(e)
                
            with open(self.o_name, 'w') as wb:
                wb.write(lines)

    def logic_js(self, number_1, new_secrets) -> str:
        """ Recreates logic from array translate function. """
        secret_array = new_secrets
        number_1 = number_1 - self.m_number
        return secret_array[number_1]

    def rotateArray(self) -> list:
        """ Shuffles the array to the correct order for deobfuscation. """
        regex = r'parseInt\((_*0x[\da-zA-Z]{1,9}\(\d{1,3}\))\)'
        verify_regex = r'[a-zA-Z]*_*0x[\da-zA-Z]{1,9},\s*[+/*\-\d]{1,20}' # find the function call with the evaluatory params

        with open(self.s_name, 'r') as wb:
            contents = wb.read()
            
            verify_array = re.findall(verify_regex, contents)
            verify_array = verify_array[0].split(",")
            verify_array = verify_array[1] ## we'll be working with this variable

            new_secrets_array = self.s_array

            parser = '' ## we'll be working with this variable
            count = len(new_secrets_array)
            
            while count:
                #print(parser)
                #print(new_secrets_array)
                try:
                    parser = int(eval(parser.replace(' ', '')))
                except SyntaxError:
                    parser = ''

                if parser == int(verify_array):
                    self.s_array = new_secrets_array
                    print(Back.GREEN + "[!] Successfully rotated array! ")
                    break
                
                #print(parser)
                #print(verify_array)
                new_secrets_array = self.pushShift(new_secrets_array)

                parser = ''
                add = False
                
                for c in contents:
                    if c == '(' and parser[-8:] == 'parseInt' and add == False:
                        if parser[-9:] == '-parseInt':
                            parser = '-parseInt' + c
                        else:
                            parser = 'parseInt' + c
                        
                        add = True
                    elif add == True and c == ';':
                        break
                    elif c != ';':
                        parser += c
                
                parse_match = re.findall(regex, parser)
                if not parse_match:
                    print(Back.RED + '[!!] Not compatible with Mode 1 ex. 0x0da0s(777)')
                    print(Back.RED + '[!!] Check beautified output file ')
                    self.beautify()
                    sys.exit(0)
                new_parse_match = []
                for m in parse_match:
                    new_parse_match.append(
                        self.parseInt(self.logic_js(self.parseIntFilter(m), new_secrets_array))
                        )

                for n in new_parse_match:
                    parser = re.sub(regex, n, parser, count=1)
                
                count -= 1

            if parser != int(verify_array):
                print(Back.RED +  "[!] Could not rotate array. Try replacing secrets = [] variable. ")

    def parseIntFilter(self, string) -> int:
        """ Reworking parseInt.. Mode1 only."""
        buffer = ''
        parenthesis = 0
        passed = False
        for c in string:
            if c == '(' and buffer[-8:] == 'parseInt':
                buffer = ''
                passed = True
            elif passed:
                if c == '(':
                    parenthesis += 1
                elif c == ')':
                    parenthesis -= 1

                if not parenthesis and c == ')':
                    break

                buffer += c

            elif not passed:
                buffer += c

        passed = False
        index = ''
        for c in buffer:
            if c == '(':
                passed = True
            elif passed and c != ')':
                index += c
        
        return int(index)             
                

class mode_2(Array_Replace):
    """ Mode 2: Array obfuscation with functions of type _0x00000(digit1, digit2). """
    """ the arg secrets_index will determine which digit is the one used for the logic. """
    """ regex example: r'_0x47edfc\((\d{2,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'"""
    def __init__(self, rgx, script_in: str, script_out: str, magic_num, secrets: list, hex_translate: bool, secrets_index=0):
        super().__init__(rgx, script_in, script_out, secrets, hex_translate)
        self.m_number = magic_num
        self.i_array = secrets_index

        if not self.m_number:
            self.m_number = self.getMagicNumber()

    def replace_js(self):
        """ Opens JS script, returns new file with replaced values. """
        ele = []
        clean = []

        for obfs in self.regex:
            with open(self.s_name, 'r') as wb: ## replace name
                lines = wb.read()
                matches = re.findall(obfs, lines)

                for item in matches:
                    ele.append(item)
                
                try:
                    for item in ele:
                        clean.append(
                            self.logic_js(
                                number_1=int(
                                    item[int(self.i_array) - 1]
                                    ), 
                                    new_secrets=self.s_array))
                except IndexError as e:
                    print(e)
                    print(Back.RED + "[!] Index is greater than secrets array. Check beautified output and manually replace secrets = [] ")
                    self.beautify()
                    sys.exit(0)

                try:
                    for item in clean:
                        lines = re.sub(obfs, "'" + item + "'", lines, count=1)
                except re.error as e:
                    print(Back.RED + '[!!] Error replacing some instances')
                    print(e)
                
            with open(self.o_name, 'w') as wb:
                wb.write(lines)

    def logic_js(self, number_1, new_secrets) -> str:
        """ Recreates logic from array translate function. """
        secret_array = new_secrets
        number_1 = number_1 - self.m_number
        return secret_array[number_1]

    def rotateArray(self) -> list:
        """ Shuffles the array to the correct order for deobfuscation. """
        regex = r'parseInt\(([a-zA-Z\d_]*_*0x[\da-zA-Z]{1,9}\(\d{1,4},\s*-*\d{1,4}\))\)'
        verify_regex = r'[a-zA-Z]*_*0x[\da-zA-Z]{1,9},\s*[+/*\-\d]{1,20}' # find the function call with the evaluatory params

        with open(self.s_name, 'r') as wb:
            contents = wb.read()
            
            verify_array = re.findall(verify_regex, contents)
            verify_array = verify_array[0].split(",")
            verify_array = verify_array[1] ## we'll be working with this variable

            new_secrets_array = self.s_array

            parser = '' ## we'll be working with this variable
            count = len(new_secrets_array)
            
            while count:
                #print(parser)
                #print(new_secrets_array)
                try:
                    parser = int(eval(parser.replace(' ', '')))
                except SyntaxError:
                    parser = ''

                if parser == int(verify_array):
                    self.s_array = new_secrets_array
                    print(Back.GREEN + "[!] Successfully rotated array! ")
                    break
                
                #print(parser)
                #print(verify_array)
                new_secrets_array = self.pushShift(new_secrets_array)

                parser = ''
                add = False
                
                for c in contents:
                    if c == '(' and parser[-8:] == 'parseInt' and add == False:
                        if parser[-9:] == '-parseInt':
                            parser = '-parseInt' + c
                        else:
                            parser = 'parseInt' + c
                        
                        add = True
                    elif add == True and c == ';':
                        break
                    elif c != ';':
                        parser += c
                
                parse_match = re.findall(regex, parser)
                #print(parser)
                if not parse_match:
                    print(Back.RED + '[!!] Not compatible with Mode 2 ex. 0x0da0s(777, 888)')
                    print(Back.RED + '[!!] Check beautified output file ')
                    self.beautify()
                    sys.exit(0)
                new_parse_match = []
                if not self.i_array:
                    self.i_array = printChoicesList(parse_match[0], 2)

                try:
                    for m in parse_match:
                        new_parse_match.append(
                            self.parseInt(
                                self.logic_js(
                                    self.parseIntFilter(
                                        string=m, 
                                        sacr_number=int(self.i_array) - 1
                                        ), 
                                        new_secrets_array
                                    )
                                )
                            )
                except IndexError as e:
                    print(Back.RED + f"ERROR: {e}")
                    print(Back.RED + "[!] Index is greater than secrets array. Check beautified output and manually replace secrets = [] ")
                    self.beautify()
                    sys.exit(0)

                for n in new_parse_match:
                    parser = re.sub(regex, n, parser, count=1)
                
                count -= 1
            
            if parser != int(verify_array):
                print(Back.RED + "[!] Could not rotate array. Try replacing secrets = [] variable. ")

    def parseIntFilter(self, string, sacr_number) -> int:
        """ Reworking parseInt.. Mode2 """
        buffer = ''
        parenthesis = 0
        passed = False
        for c in string:
            if c == '(' and buffer[-8:] == 'parseInt':
                buffer = ''
                passed = True
            elif passed:
                if c == '(':
                    parenthesis += 1
                elif c == ')':
                    parenthesis -= 1

                if not parenthesis and c == ')':
                    break

                buffer += c

            elif not passed:
                buffer += c

        passed = False
        index = ''
        for c in buffer:
            if c == '(':
                passed = True
            elif passed and c != ')':
                index += c

        if ", " in index:       
            index = index.split(", ")
        elif "," in index:
            index = index.split(",")

        return int(index[sacr_number])

class mode_3(Array_Replace):
    """ Mode 3: Array obfuscation with functions of type _0x00000(digit1, digit2, digit3, digit4). """
    """ the arg secrets_index will determine which digit is the one used for the logic. """
    """ regex example: r'_0x47edfc\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'"""

    def __init__(self, rgx, script_in: str, script_out: str, magic_num, secrets: list, hex_translate: bool, secrets_index=0):
        super().__init__(rgx, script_in, script_out, secrets, hex_translate)
        self.m_number = magic_num
        self.i_array = secrets_index

        if not self.m_number:
            self.m_number = self.getMagicNumber()

    def replace_js(self):
        pass

    def logic_js(self):
        pass

    def rotateArray(self):
        pass

    def parseIntFilter(self):
        pass

def initialize_d(script: str, magic_number = 0, beautify=True):
    init(autoreset=True)
    # save provided script contents to local file
    file_name = f"{str(random.randint(1,999))}-script.txt"
    with open(file_name, 'a') as file:
        file.write(script)

    ArrayDeobfs = mode_1(regex2, file_name, "new.txt", magic_number, secrets, hex_translate=True, base64_decode=True)

    if ArrayDeobfs:
        ArrayDeobfs.getSize()
        ArrayDeobfs.hexReplace()
        ArrayDeobfs.rotateArray()
        ArrayDeobfs.replace_js()
        if beautify:
            ArrayDeobfs.beautify()
            ArrayDeobfs.concatString()

    with open("new.txt", 'r') as file:
        result = file.read()

    if path.exists("new.txt"):
        remove("new.txt")

    if path.exists(file_name):
        remove(file_name)

    return result
        
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Array-based Javascript deobfuscator.')
    parser.add_argument('-js', type=str, help='Dir to JS script.', required=True) ## <-----
    parser.add_argument('-o', type=str, help='Output file name.', required=False)
    parser.add_argument('-mn', '--magicnumber', type=int, help='Decimals used for deobfuscating. If none provided, it will attempt to find automatically.', required=False)
    parser.add_argument('-a', '--array', type=str, help='Path to text file containing the array with secrets. If none provided, it will attempt to find automatically.', required=False)
    parser.add_argument('-b', '--beautify', action='store_true', help='Beautify script.', required=False)
    parser.add_argument('-b64', '--base64', action='store_true', help='Decodes base64 items from secrets array', required=False)
    parser.add_argument('-m1', '--mode1', action='store_true', help='Simple 0x021ab2(777) form deobfuscation.') ## <-----
    parser.add_argument('-m2', '--mode2', action='store_true', help='More advanced 0x021ab2(777, 999) form deobfuscation.') ## <-----
    parser.add_argument('-cf', '--controlflow', action='store_true', help='Attempts to reconstruct control flow.')


    
    args = parser.parse_args()
    init(autoreset=True) # Colorama

    
    js_script = args.js
    new_js_script = 'new.js_'
    ArrayDeobfs = ''

    if args.o:
        new_js_script = args.o
    if args.magicnumber:
        magic_number = args.magicnumber

    if args.mode1:
        ArrayDeobfs = mode_1(regex2, js_script, new_js_script, magic_number, secrets, hex_translate=True, base64_decode=True)
    elif args.mode2:
        ArrayDeobfs = mode_2(regex, js_script, new_js_script, magic_number, secrets, hex_translate=True)
    elif args.controlflow:
        ArrayDeobfs = Array_Replace(regex, js_script, new_js_script, secrets, hex_translate=False)
        ArrayDeobfs.controlFlowReconstruct()
        sys.exit(0)
    else:
        print("[!] Please choose a mode [1,2] ex. -m1, -m2")

    if ArrayDeobfs:
        ArrayDeobfs.getSize()
        ArrayDeobfs.hexReplace()
        ArrayDeobfs.rotateArray()
        ArrayDeobfs.replace_js()
        if args.beautify:
            ArrayDeobfs.beautify()
            ArrayDeobfs.concatString()
        