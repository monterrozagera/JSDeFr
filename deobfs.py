# INSTRUCTIONS
# 1.Find function containing the deobfuscation array and replace the variable 'secrets'
# 2.Find function containing the algorithm to replace the obfuscated values with the correct values from the array and replace the variable 'magic number'
# 3.Replace the regex variable with the correct name of the function that deobfuscates
# 4.Replace the variable js_script with the name of the script to deobfuscate

# TODO: add options for 1,2,3,4 argument function to replace
# args parse, better feedback, pluggins
# remember, stick to what you can do. theres about 10 days left
from pathlib import Path
import argparse
import re

class Array_Replace:
    """ Handles different kinds of array-based deobfuscation. """
    def __init__(self, rgx, script_in: str, script_out: str, secrets: list, hex_translate=False):
        self.s_name = script_in
        self.o_name = script_out 
        self.s_array = secrets
        self.regex = rgx
        self.t_hex = hex_translate

        if self.t_hex:
            self.hexReplace()

    def countIntances(self, to_count):
        """ This function will count the times that the given argument is referenced """
        """ in the script. """
        pass

    def hexReplace(self):
        """ This function will replace all hex digits to decimals. """
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
        print(f"Size: {kb_size}KB")

        
class mode_1(Array_Replace):
    """ Mode 1: Simple array obfuscation with functions of type _0x0000(digit) """
    """ regex example: r'_0x446cb2\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'"""
    def __init__(self, rgx, script_in: str, script_out: str, magic_num, secrets: list, hex_translate=False):
        super().__init__(rgx, script_in, script_out, secrets, hex_translate)
        self.m_number = magic_num

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
                    clean.append(self.logic_js(number_1=int(item)))

                try:
                    for item in clean:
                        lines = re.sub(obfs, "'" + item + "'", lines, count=1)
                except re.error:
                    pass
                
            with open(self.o_name, 'w') as wb:
                wb.write(lines)

    def logic_js(self, number_1) -> str:
        """ Recreate logic from array translate function. """
        secret_array = self.s_array
        number_1 = number_1 - self.m_number
        return secret_array[number_1]

class mode_2(Array_Replace):
    """ Mode 2: Array obfuscation with functions of type _0x00000(digit1, digit2). """
    """ the arg secrets_index will determine which digit is the one used for the logic. """
    """ regex example: r'_0x47edfc\((\d{2,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'"""
    def __init__(self, rgx, script_in: str, script_out: str, magic_num, secrets: list, hex_translate: bool, secrets_index: int):
        super().__init__(rgx, script_in, script_out, secrets, hex_translate)
        self.m_number = magic_num
        self.i_array = secrets_index

    def replace_js(self):
        """ Opens JS script, returns new file with replaced values. """
        ele = []
        clean = []

        for obfs in self.regex:
            with open(self.s_name, 'r') as wb: ## replace name
                lines = wb.read()
                matches = re.findall(obfs, lines)


                for item in matches:
                    ele.append(item[self.i_array])
                for item in ele:
                    clean.append(self.logic_js(number_1=int(item)))

                try:
                    for item in clean:
                        lines = re.sub(obfs, "'" + item + "'", lines, count=1)
                except re.error:
                    pass
                
            with open(self.o_name, 'w') as wb:
                wb.write(lines)

    def logic_js(self, number_1) -> str:
        """ Recreate logic from array translate function. """
        secret_array = self.s_array
        number_1 = number_1 - self.m_number
        return secret_array[number_1]

if __name__ == '__main__':

    ### replace secrets, regex, magic_number and js_script
    secrets = ["WScript.Shell", "bind", "30JCZLUg", "4. Open one of the following links in your browser to download decryptor:", "      - If you do not pay in 3 days YOU LOOSE ALL YOUR FILES.", "1A8nxYR1FNMyjn71RTgmwugHB9Y44p7Akg", "rGhXR", "1|4|0|3|2", "4QIObMC", "exception", "%%i", "jmJkN", "8057VEfgvQ", "1|2|0|5|3|4", "constructor", "Crypted", "4|0|2|5|1|3", "CreateObject", "      - Your files can be decrypted only after you make payment.", "{}.constructor(\&quot;return this\&quot;)( )", "BHcnL", "saveToFile", "xMlvq", "send", " /t REG_SZ /F /D ", "2|4|5|0|1|3", "5940035hpvWwP", "responseBody", "      http://", "LRAf9RSu-l5rAk8FM7MZAj05YpDtxEyEuY72K46WGdFbZP20XuLJwoYHSJnJB47wIa9baToAFno_", " BTC to this Bitcoin address:", "were encrypted using strong RSA-1024 algorithm with a unique key.", "copy /y ", "HKCR", "RDWga", "__proto__", "Run", ".crypted", "warn", " &amp; notepad.exe ", "error", " /ve /t REG_SZ /F /D ", " &amp; call ", "puntogel.com pme.com.vn www.staubsaugrobotern.com felicavet.hu www.tattoogreece.gr", "kJoty", "Close", "&amp;dc=283385", " /V ", "Windows", "lRFGk", "      https://localbitcoins.com/buy_bitcoins", ".txt", "/counter/?ad=", "%UserProfile%", " %%i in (*.zip *.rar *.7z *.tar *.gz *.xls *.xlsx *.doc *.docx *.pdf *.rtf *.ppt *.pptx *.sxi *.odm *.odt *.mpp *.ssh *.pub *.gpg *.pgp *.kdb *.kdbx *.als *.aup *.cpr *.npr *.cpp *.bas *.asm *.cs *.php *.pas *.vb *.vcproj *.vbproj *.mdb *.accdb *.mdf *.odb *.wdb *.csv *.tsv *.psd *.eps *.cdr *.cpt *.indd *.dwg *.max *.skp *.scad *.cad *.3ds *.blend *.lwo *.lws *.mb *.slddrw *.sldasm *.sldprt *.u3d *.jpg *.tiff *.tif *.raw *.avi *.mpg *.mp4 *.m4v *.mpeg *.mpe *.wmf *.wmv *.veg *.vdi *.vmdk *.vhd *.dsk) do (REN ", "open", "size", "Please follow this manual:", ".exe ", "277013bVYGSM", "1. Create Bitcoin wallet here:", "WriteLine", "221152wvqHVx", "HKCU", "prototype", "end", "Scripting.FileSystemObject", "&amp;rnd=297188", "apply", "PLEASE REMEMBER:", "      ", "5. Run decryptor to restore your files.", "hBogs", "822843", "33icHGDc", "      - It`s useless to reinstall Windows, update antivirus software, etc.", "Microsoft", "XguMu", "table", "UoIvj", "3. Send ", "split", "7096zCOzrv", "toString", "notepad.exe ", "5394246KhORef", "trace", "SOFTWARE", "kEXUm", "fromCharCode", "type", "REG ADD ", "zKhtd", "MSXML2.XMLHTTP", "close", "Desktop", "4|1|2|3|0|5", "length", "command", "551106EgDWwT", "72fhyFIe", " &amp;&amp; for /r ", "HQEKt", "18933780SdKtwj", "shell", "%%~nxi.crypted", ".cmd", "45|31|2|22|36|23|5|35|14|34|19|44|27|28|18|32|47|3|41|29|0|37|30|26|20|4|6|15|40|13|24|46|21|8|39|9|16|25|38|33|17|1|11|7|12|43|10|42", "GGMhj", "FileExists", "CreateTextFile", "write", "status", "DECRYPT.txt", "ATTENTION!", "GET", "position", "log", "%AppData%", ".exe", "console", "http://"] 
    

    # TODO: support for multiple regex, replace string for array?
    regex = r'_0x47edfc\((\d{2,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)' ## 2 digit
    regex2 = [r'_0x446cb2\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)', r'_0x303630\((-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)'] ## 1 digit
    magic_number = 310
    js_script = 'ran.js_'
    new_js_script = 'new_' + js_script

    ArrayDeobfs = mode_1(regex2, js_script, new_js_script, magic_number, secrets)
    ArrayDeobfs.getSize()
