
import re

def translate_hex(script_in, regex, script_out='out.js_'):
    ele = []
    clean = []

    with open(script_in, 'r') as wb: ## replace name
        lines = wb.read()
        matches = re.findall(regex, lines)

        for item in matches:
            ele.append(item)
        for item in ele:
            clean.append(int(item, 16))

        try:
            for item in clean:
                lines = re.sub(regex, str(item), lines, count=1)
        except re.error:
            pass
        
    with open(script_out, 'w') as wb:
        wb.write(lines)

if __name__ == '__main__':
    regex = r'\b0x[0-9A-Fa-f]{1,5}'
    name = 'ran.js_'

    translate_hex(name, regex)