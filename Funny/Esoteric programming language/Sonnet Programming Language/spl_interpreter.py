# Sonnet Programming Language (SPL) Interpreter - ENHANCED VERSION
# Now with real output capability!

import sys
import re

# Expanded Shakespearean variables
variables = {
    "thee": 0, "thou": 0, "love": 0, "time": 0, "heart": 0,
    "rose": 0, "beauty": 0, "summer": 0, "eye": 0, "death": 0,
    "fair": 0, "foul": 0, "sweet": 0, "gold": 0, "day": 0,
    "heaven": 0, "shade": 0, "line": 0, "breath": 0, "world": 0
}

positive_words = ["fair", "sweet", "bright", "gold", "eternal", "true", "lovely", "gentle", "warm", "temperate", "darling", "heaven"]
negative_words = ["foul", "dark", "false", "cold", "cruel", "base", "rough", "harsh", "short", "death", "fade", "lose"]
multiplier_words = ["more", "twice", "double", "thrice", "every"]

output_buffer = []
proclaim_var = "thee"  # Default variable to output in the couplet

def count_syllables(word):
    word = word.lower().strip(".,!?;")
    if not word: return 0
    count = len(re.findall(r'[aeiouy]+', word))
    if len(word) > 2 and word.endswith('e'): count -= 1
    if word.endswith('es') or word.endswith('ed'): count -= 1
    return max(1, count)

def evaluate_phrase_strength(line_lower):
    words = re.findall(r'\w+', line_lower)
    strength = 0
    mult = 1
    for word in words:
        if word in multiplier_words:
            mult += 1
        elif word in positive_words:
            strength += mult
            mult = 1
        elif word in negative_words:
            strength -= mult
            mult = 1
    return strength if strength != 0 else 1

def parse_line(line, line_num):
    global proclaim_var
    line_lower = line.lower()
    
    # Detect which variable to proclaim in couplet
    if line_num >= 12:
        if any(word in line_lower for word in ["proclaim", "sing", "tell", "speak", "voice", "say"]):
            for var in variables:
                if var in line_lower:
                    proclaim_var = var
    
    # Assignment: common Shakespearean patterns
    for var in variables:
        if var in line_lower:
            if any(p in line_lower for p in ["art ", "art more ", "be ", "is ", "hath ", "shall ", "grow", "ow"]):
                variables[var] += evaluate_phrase_strength(line_lower)
            # Special boost for direct address
            if "thy " + var in line_lower or "thou " + var in line_lower:
                variables[var] += 2

    # Addition: "sum of X and Y"
    sum_match = re.search(r'sum of (\w+) and (\w+)', line_lower)
    if sum_match:
        a, b = sum_match.groups()
        if a in variables and b in variables:
            variables[a] += variables[b]

    # Multiplication: "more", "twice", etc. already handled in strength

def check_poetic_structure(lines):
    if len(lines) != 14:
        raise ValueError("A sonnet must have exactly 14 lines, no more, no less!")

    for i, line in enumerate(lines):
        words = re.findall(r'\w+', line)
        syllables = sum(count_syllables(w) for w in words)
        if not 8 <= syllables <= 12:
            print(f"(Poetic note: Line {i+1} has {syllables} syllables — close to iambic pentameter)")

    # Safe last word extraction
    last_words = []
    for line in lines:
        match = re.search(r'(\w+)[^\\w]*$', line.lower())
        last_words.append(match.group(1) if match else "")

    expected = [0,2,0,2, 4,6,4,6, 8,10,8,10, 12,12]
    seen = {}
    for i in range(14):
        word = last_words[i]
        group = expected[i]
        if group in seen and seen[group] != word and word:
            print(f"(Gentle rhyme note: lines {seen[group]} and {i+1} end '{seen[group]}' vs '{word}')")
        seen[group] = i+1 if not word else word

def run_sonnet(source_code):
    lines = [line.strip() for line in source_code.split('\n') if line.strip()]
    check_poetic_structure(lines)

    for i, line in enumerate(lines):
        parse_line(line, i)

    # Output in the volta (couplet)
    if any(word in " ".join(lines[12:]).lower() for word in ["proclaim", "sing", "tell", "speak", "voice", "say", "lives", "breath"]):
        value = variables[proclaim_var]
        # Convert numbers to string: split into chars (positive for ASCII)
        while value > 0:
            char_code = (value % 95) + 32  # Printable ASCII: space to ~
            output_buffer.append(chr(char_code))
            value //= 95
        if not output_buffer and variables[proclaim_var] != 0:
            output_buffer.append(chr(72))  # fallback 'H' for hello

    result = ''.join(output_buffer)
    print("\nOutput:", f'"{result}"' if result else "(silent contemplation)")
    print("\nVariables eternalized:")
    for k, v in sorted(variables.items()):
        if v != 0:
            print(f"  {k.capitalize():8}: {v}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python spl_interpreter.py <sonnet_file.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        run_sonnet(code)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        print("\nTry saving Shakespeare's Sonnet 18 as sonnet18.txt")