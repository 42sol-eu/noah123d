#!/usr/bin/env python3
"""
Script to convert title case headings and numbered lists to sentence case
in markdown documentation files.
----
project:
    name:        a7d
    uuid:        2cc2a024-ae2a-4d2c-91c2-f41348980f7f
    url:         https://github.com/42sol-eu/a7d
"""

import os
import re
from pathlib import Path
no = False
yes = True 

P_debug = no
G_file_changed_count = 0

# Preserve these words as they are (proper nouns, acronyms, technical terms)
PRESERVE_WORDS = {
    # Project/Company names
    'Noah123d', 'GitHub', 'PyPI', 'MkDocs', 'Python', 'Poetry', 'License', 'MIT',
    
    # File formats and protocols
    'STL', '3MF', 'API', 'CLI', 'JSON', 'XML', 'HTML', 'CSS', 'JS', 'TS',
    
    # Technical terms
    'ASCII', 'UUID', 'OOP', 'IDE', 'VS', 'Code', 'URL', 'URI', 'HTTP', 'HTTPS',
    'TCP', 'UDP', 'IP', 'DNS', 'SSL', 'TLS', 'SSH', 'FTP', 'SMTP', 'POP', 'IMAP',
    
    # Programming related
    'pip', 'npm', 'git', 'pytest', 'black', 'isort', 'mypy', 'flake8', 'tox',
    'virtualenv', 'conda', 'venv', 'docker', 'kubernetes', 'mysql', 'postgresql',
    
    # Common abbreviations
    'OS', 'CPU', 'GPU', 'RAM', 'SSD', 'HDD', 'USB', 'CD', 'DVD', 'PDF', 'ZIP',
    'PNG', 'JPG', 'JPEG', 'GIF', 'SVG', 'BMP', 'ICO', 'TIFF', 'WEBP',
    
    # Units and measurements  
    'KB', 'MB', 'GB', 'TB', 'PB', 'Hz', 'KHz', 'MHz', 'GHz', 'DPI', 'PPI',
    
    # Version control
    'PR', 'MR', 'CI', 'CD', 'QA', 'UAT', 'SLA', 'SLO', 'KPI',
    
    # 3D Printing specific
    'CAD', 'CAM', 'CNC', 'FDM', 'SLA', 'SLS', 'PLA', 'ABS', 'PETG', 'TPU',
}

def is_preserve_word(word):
    """Check if a word should be preserved as-is."""
    return word in PRESERVE_WORDS

def convert_to_sentence_case(text):
    """Convert title case text to sentence case while preserving certain words."""
    # Split into words
    words = text.split()
    if not words:
        return text
    
    result = []
    
    for i, word in enumerate(words):
        # Remove any markdown formatting temporarily
        clean_word = re.sub(r'[*_`]', '', word)
        
        # Preserve words that should not be changed
        if is_preserve_word(clean_word):
            result.append(word)
        # First word should be capitalized (except after markdown bold/italic)
        elif i == 0 or (i > 0 and words[i-1].endswith(':')):
            # Keep original formatting but ensure first letter is uppercase
            if word and word[0].islower():
                result.append(word[0].upper() + word[1:])
            else:
                result.append(word)
        else:
            # For other words, convert to lowercase unless they're preserve words
            # But keep any markdown formatting
            if clean_word.isupper() and len(clean_word) <= 4:
                # Likely an acronym, keep it
                result.append(word)
            elif clean_word and clean_word[0].isupper() and not is_preserve_word(clean_word):
                # Convert to lowercase but preserve markdown formatting
                new_word = word.replace(clean_word, clean_word.lower())
                result.append(new_word)
            else:
                result.append(word)
    
    return ' '.join(result)

def process_line(line):
    """Process a single line to convert title case to sentence case."""
    stripped = line.strip()
    
    # Handle markdown headings (# ## ### etc.)
    heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
    if heading_match:
        prefix = heading_match.group(1)
        title = heading_match.group(2)
        new_title = convert_to_sentence_case(title)
        return line.replace(stripped, f"{prefix} {new_title}")
    
    # Handle numbered lists (1. 2. etc.)
    list_match = re.match(r'^(\s*)(\d+\.)\s+(.+)$', stripped)
    if list_match:
        indent = list_match.group(1)
        number = list_match.group(2)
        content = list_match.group(3)
        new_content = convert_to_sentence_case(content)
        return line.replace(stripped, f"{indent}{number} {new_content}")
    
    return line

def process_file(file_path):
    """Process a single markdown file."""
    global G_file_changed_count
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    file_changed_count = 0
    new_lines = []
    
    for line in lines:
        new_line = process_line(line)
        if new_line != line:
            modified = True
            if P_debug:
                file_changed_count +=1
                print(f"  Changed: {line.strip()} -> {new_line.strip()}")
        new_lines.append(new_line)
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"  ✅ Updated {file_path} {file_changed_count}")
        G_file_changed_count += file_changed_count
    else:
        print(f"  ⏭️  No changes needed for {file_path}")

def main():
    """Main function to process all markdown files in docs/."""
    docs_dir = Path("docs")
    
    if not docs_dir.exists():
        print("Error: docs/ directory not found")
        return
    
    # Find all markdown files
    md_files = list(docs_dir.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to process\n")
    
    for md_file in sorted(md_files):
        process_file(md_file)
        print()

    print(f"✅ Title case conversion completed!\n- {len(md_files)} files processed\n- {G_file_changed_count} lines changed.")

if __name__ == "__main__":
    main()
