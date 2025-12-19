# Sonnet Programming Language (SPL) Interpreter - FIXED VERSION
# Original creation by Grok (December 2025) - Bugfix applied

import sys
import re

# Built-in variables (Shakespearean theme)
variables = {
    "thee": 0, "thou": 0, "love": 0, "time": 0, "heart": 0,
    "rose": 0, "beauty": 0, "summer": 0, "eye": 0, "death": 0,
    "fair": 0, "foul": 0, "sweet": 0, "gold": 0, "day": 0
}

# Sentiment words for value calculation
positive = ["fair", "sweet", "bright", "gold", "eternal", "true", "lovely", "gentle", "warm"]
negative = ["foul", "dark", "false", "cold", "cruel", "base", "rough", "harsh"]
multipliers = ["twice", "double", "thrice", "triple"]

output_buffer = []

def count_syllables(word):
    word = word.lower()
    if not word: return 0
    count = len(re.findall(r'[aeiouy]+', word))
    if word.endswith('e') and len(word) > 2: count -= 1
    if word.endswith('es') or word.endswith('ed'): count -= 1
    return max(1, count)

def evaluate_phrase(line):
    words = re.findall(r'\w+', line.lower())
    value = 0
    mult = 1
    for word in words:
        if word in multipliers:
            mult *= 2 if "twice" in word or "double" in word else 3
        elif word in positive:
            value += mult
            mult = 1
        elif word in negative:
            value -= mult
            mult = 1
    return value if value != 0 else 1  # default increment

def parse_line(line, line_num):
    line_lower = line.lower()
    
    # Assignment: "Thou art fair", "Let love be sweet", etc.
    for var in variables:
        if var in line_lower:
            if any(phrase in line_lower for phrase in ["art ", "be ", "is ", "let ", "shall "]):
                variables[var] = evaluate_phrase(line)
    
    # Addition: "the sum of thee and love"
    sum_match = re.search(r'sum of (\w+) and (\w+)', line_lower)
    if sum_match:
        a, b = sum_match.groups()
        if a in variables and b in variables:
            variables[a] += variables[b]
    
    # Multiplication hint: "twice thy heart"
    if "twice" in line_lower or "double" in line_lower:
        for var in variables:
            if var in line_lower:
                variables[var] *= 2
    
    # Output trigger in the final couplet (lines 13-14)
    if line_num >= 12:
        if any(word in line_lower for word in ["speak", "tell", "sing", "proclaim", "say", "voice"]):
            for val in variables.values():
                if val != 0:
                    char_code = abs(val) % 95 + 32  # printable ASCII range
                    output_buffer.append(chr(char_code))

def check_poetic_structure(lines):
    if len(lines) != 14:
        raise ValueError("Error: A true sonnet must have exactly 14 lines!")
    
    # Rough iambic pentameter check (8–12 syllables per line)
    for i, line in enumerate(lines):
        words = re.findall(r'\w+', line)
        syllables = sum(count_syllables(w) for w in words)
        if not 8 <= syllables <= 12:
            print(f"Warning: Line {i+1} has {syllables} syllables (ideal: 10 for iambic pentameter)")
    
    # FIXED: Safe extraction of last word (ignore trailing punctuation)
    last_words = []
    for line in lines:
        # Remove trailing punctuation and get the last sequence of word characters
        match = re.search(r'(\w+)\W*$', line.lower())
        last_words.append(match.group(1) if match else "")
    
    # Very basic rhyme check
    expected_rhymes = [0,2,0,2, 4,6,4,6, 8,10,8,10, 12,12]
    rhymes_seen = {}
    for i in range(14):
        word = last_words[i]
        group = expected_rhymes[i]
        if group not in rhymes_seen:
            rhymes_seen[group] = word
        elif rhymes_seen[group] != word and word != "":
            print(f"Note: Rhyme suggestion — lines ending with '{rhymes_seen[group]}' and '{word}' (line {i+1})")

def run_sonnet(source_code):
    lines = [line.strip() for line in source_code.split('\n') if line.strip()]
    check_poetic_structure(lines)
    
    for i, line in enumerate(lines):
        parse_line(line, i)
    
    result = ''.join(output_buffer)
    print("\nOutput:", result if result else "(silent contemplation)")
    print("\nFinal variable state:")
    for k, v in variables.items():
        if v != 0:
            print(f"  {k}: {v}")

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