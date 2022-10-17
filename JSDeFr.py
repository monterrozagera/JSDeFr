# TODO: add YARA RULES integration, base64decode, bruteforce
# controlFlowFlattening eg. _0x342234{ 'first': 0x8213(234, 556) } console[0x8213(234, 522)](_0x342234['first])
# FUTURE: mode 3 0x23gb3(333, 777, 888, 999)
#         custom mode (choose args amount, and custom logic)
from colorama import init, Back
from choice_handle import printChoicesList
from pathlib import Path
import argparse
import sys
import re


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


    def countIntances(self, to_count):
        """ Counts the times that the given argument is referenced """
        """ in the script. """
        pass

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

if __name__ == '__main__':
    banner = """
       █████  █████████                     
      ░░███  ███░░░░░███                    
       ░███ ░███    ░░░                     
       ░███ ░░█████████                     
       ░███  ░░░░░░░░███                    
 ███   ░███  ███    ░███                    
░░████████  ░░█████████                     
 ░░░░░░░░    ░░░░░░░░░                                                        
                                            
 ██████████            ███████████          
░░███░░░░███          ░░███░░░░░░█          
 ░███   ░░███  ██████  ░███   █ ░  ████████ 
 ░███    ░███ ███░░███ ░███████   ░░███░░███
 ░███    ░███░███████  ░███░░░█    ░███ ░░░ 
 ░███    ███ ░███░░░   ░███  ░     ░███     
 ██████████  ░░██████  █████       █████    
░░░░░░░░░░    ░░░░░░  ░░░░░       ░░░░░     
𝘵𝘩𝘦 𝘑𝘢𝘷𝘢𝘴𝘤𝘳𝘪𝘱𝘵 𝘋𝘦𝘰𝘣𝘧𝘶𝘴𝘤𝘢𝘵𝘪𝘰𝘯 𝘍𝘳𝘢𝘮𝘦𝘸𝘰𝘳𝘬 𝘷1.0                             
                                            
                                            
    """
    parser = argparse.ArgumentParser(description='Array-based Javascript deobfuscator.')
    parser.add_argument('-js', type=str, help='Dir to JS script.', required=True)
    parser.add_argument('-o', type=str, help='Output file name.', required=False)
    parser.add_argument('-mn', '--magicnumber', type=int, help='Decimals used for deobfuscating. If none provided, it will attempt to find automatically.', required=False)
    parser.add_argument('-a', '--array', type=str, help='Path to text file containing the array with secrets. If none provided, it will attempt to find automatically.', required=False)
    parser.add_argument('-b', '--beautify', action='store_true', help='Beautify script.', required=False)
    parser.add_argument('-b64', '--base64', action='store_true', help='Decodes base64 items from secrets array', required=False)
    parser.add_argument('-m1', '--mode1', action='store_true', help='Simple 0x021ab2(777) form deobfuscation.')
    parser.add_argument('-m2', '--mode2', action='store_true', help='More advanced 0x021ab2(777, 999) form deobfuscation.')

    secrets = ['\x0a<html>\x0a\x09<head>\x0a\x09\x09<title>Your Files Have Been Encrypted</title>\x0a\x09</head>\x0a\x09<body>\x0a\x09\x09<h1>Your files have been encrypted!</h1>\x0a\x09\x09<p>Please send 0.3 Ethereum to the following address: 0xDEADBEEFDEADBEEFDEADBEEFDEADBEEFDDEADBEEF</p>\x0a\x09\x09<em>For the sake of the project, please DO NOT send any real ethereum to this address!</em>\x0a\x09\x09<br>\x0a\x09\x09<p>Make sure you send this:\x0a\x09\x09<br>\x0a\x09\x09<p><em>', 'encrypt.js', '444853DZYvyf', 'encrypt.elf', 'decrypt.elf', '11812430VPfLUf', '.iv', 'exit', 'log', '9cYppBJ', '1139330EgIpFB', 'encrypt.app', 'execPath', 'hex', '345079NDoWoE', 'path', '718521DqYxMC', '</em></p>\x0a\x09\x09<p>Along with your transaction as a message input. We will soon get in touch</p>\x0a\x09\x09<br>\x0a\x09\x09<h1>Warning: Any tampering with any of the files in this directory will result in permanent loss of the file</h1>\x0a\x09</body>\x0a</html>\x0a', 'NOTICE.html', 'decrypt.js', '2174888qWETkn', 'isFile', 'encrypt.exe', '.encrypted', 'pkg', 'device_key_encrypted.dat', '96AbDBCm', 'aes-192-cbc', 'toString', 'forEach', '-----BEGIN PUBLIC KEY-----\x0aMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoK+jQ8f3O3Ug4GdLEK5X\x0aMixXGi72NMIhU2lEE/BXF3C42J/fjVNYPXvZPzX/Cz3atGBX7D2nK28YntVvAII0\x0adEZMvcmkR5Y4ZYahFWYyU4NcOWU/TEMv2w3IsQ4Eageu+1D+qS9rCIbj619wYCeJ\x0ancpMwYD2b0fGpyHZUEfNLX2Qf8QRZPKRtQx05MUPNjgRO/nnXDjq6xs7hEYZB6Nd\x0afvGjOaggtmY0/7X+wnojkZXyjkbbRRUPiB3/rgXhXsv89T9ioQZO2enK4A6JWn/s\x0abFYyUBmQ+uzhADy3HcQZkfMGGwZho6FFtOQNZv1fPVbAMPxAGm61yG46uWgiqJUV\x0a8QIDAQAB\x0a-----END PUBLIC KEY-----', 'pipe', '88GnaEVx', 'crypto', 'You have already encrypted your files once, are you sure you want to pay more?', '6685oBLNit']
    args = parser.parse_args()
    init(autoreset=True) # Colorama

    regex = [r'[a-zA-Z_]*0*_*0x[\da-zA-Z]{1,9}\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,}),\s*(-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'] ## 2 digit
    regex2 = [r'[a-zA-Z]*0*_*0x[\da-zA-Z]{1,9}\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'] ## 1 digit
    magic_number = 0
    js_script = args.js
    new_js_script = 'new.js_'
    ArrayDeobfs = ''
    print(banner)

    if args.o:
        new_js_script = args.o
    if args.magicnumber:
        magic_number = args.magicnumber

    if args.mode1:
        ArrayDeobfs = mode_1(regex2, js_script, new_js_script, magic_number, secrets, hex_translate=True, base64_decode=True)
    elif args.mode2:
        ArrayDeobfs = mode_2(regex, js_script, new_js_script, magic_number, secrets, hex_translate=True)
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
        