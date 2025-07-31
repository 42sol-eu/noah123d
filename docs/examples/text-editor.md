# 3MF text editor

A powerful utility for modifying text content in 3MF files. This tool allows you to edit text strings stored in slicer metadata, such as object names and embedded text elements created by CAD software or slicers like PrusaSlicer.

## Overview

The **3MF Text Editor** can modify text strings that are stored as metadata in 3MF files. This is particularly useful for:

- Changing object names that appear in slicer software
- Modifying embedded text created by CAD programs
- Customizing text elements for different languages or purposes
- Batch processing of 3MF files with text content

## Features

- ✅ **List Text Content**: Display all modifiable text in a 3MF file
- ✅ **Single Text Replacement**: Replace one text string with another
- ✅ **Interactive Mode**: Replace multiple text strings in one session
- ✅ **Automatic Backup**: Creates backup files before modification
- ✅ **Verbose Output**: Detailed logging for troubleshooting
- ✅ **Multiple Config Support**: Works with various slicer metadata formats

## Installation

Make sure you have the noah123d library installed and the required dependencies:

```bash
pip install numpy-stl
```

## Usage

### 1. list text content

Display all modifiable text in a 3MF file:

```bash
python text_3mf_editor.py input.3mf --list-text
```

**Example Output:**
```
🔍 Searching for text content in: text.3mf
============================================================
✅ Found 3 text string(s):

 1. "Form-Kubus"
    Location: Metadata/Slic3r_PE_model.config
 2. "Rissen text"
    Location: Metadata/Slic3r_PE_model.config
 3. "Sunken text"
    Location: Metadata/Slic3r_PE_model.config
```

### 2. single text replacement

Replace one text string with another:

```bash
python text_3mf_editor.py input.3mf output.3mf "Old Text" "New Text"
```

**Example:**
```bash
python text_3mf_editor.py text.3mf custom_text.3mf "Rissen Text" "Raised Text"
```

### 3. interactive mode

Replace multiple text strings in one session:

```bash
python text_3mf_editor.py input.3mf output.3mf --interactive
```

**Example Session:**
```
🎯 Interactive Text Editor Mode
========================================
Found 3 unique text string(s):

 1. "Form-Kubus"
 2. "Rissen text"
 3. "Sunken text"

Enter text to replace (or press Enter to finish):
> Rissen Text
Enter new text to replace 'Rissen Text':
> Custom Raised Text
✅ Added replacement: 'Rissen Text' → 'Custom Raised Text'

Enter text to replace (or press Enter to finish):
> Sunken Text
Enter new text to replace 'Sunken Text':
> Custom Engraved Text
✅ Added replacement: 'Sunken Text' → 'Custom Engraved Text'

Enter text to replace (or press Enter to finish):
> 
✅ Successfully created modified 3MF: output.3mf
```

## Command line options

| Option | Description |
|--------|-------------|
| `input_file` | Path to the input 3MF file |
| `output_file` | Path for the output 3MF file (required for modifications) |
| `old_text` | Text to replace (for single replacement mode) |
| `new_text` | New text to use as replacement |
| `--list-text` | List all text content in the file |
| `--interactive` | Enter interactive mode for multiple replacements |
| `--verbose`, `-v` | Enable verbose output |
| `--no-backup` | Skip creating a backup file |

## How it works

The 3MF Text Editor works by:

1. **Opening the 3MF archive** (3MF files are ZIP archives internally)
2. **Locating metadata files** that contain text definitions:
   - `Metadata/Slic3r_PE_model.config`
   - `Metadata/PrusaSlicer_model.config`
   - `Metadata/model.config`
3. **Parsing XML content** to find text strings in:
   - Volume name attributes: `<metadata key="name" value="Text Here"/>`
   - Text elements: `<slic3rpe:text text="Text Here" .../>`
4. **Applying replacements** to the metadata
5. **Recreating the 3MF file** with modified metadata

## Important notes

### What can be modified
- ✅ Object names and labels stored in slicer metadata
- ✅ Embedded text created by CAD software
- ✅ Text elements added in slicer programs
- ✅ Volume names and descriptions

### What cannot be modified
- ❌ Text that is part of the actual 3D mesh geometry
- ❌ Text "carved" or "embossed" as 3D shapes
- ❌ Texture-based text on surfaces
- ❌ Text in build plate instructions

### Compatibility
- **Slicer software**: PrusaSlicer, Slic3r PE, and compatible slicers
- **CAD software**: Any software that stores text as 3MF metadata
- **File types**: Standard 3MF files with metadata

### Backup and safety
- Automatic backup files are created (unless `--no-backup` is used)
- Original 3D geometry is never modified
- Changes only affect metadata/display names
- Reversible by restoring from backup

## Examples

### Example 1: Translate text to another language

```bash
# List current text
python text_3mf_editor.py model.3mf --list-text

# Translate from german to english
python text_3mf_editor.py model.3mf model_english.3mf "Gehäuse" "Housing"
python text_3mf_editor.py model_english.3mf model_final.3mf "Deckel" "Cover"
```

### Example 2: Customize product names

```bash
# Change generic names to specific product names
python text_3mf_editor.py template.3mf product_v1.3mf --interactive
# Then interactively replace "Part A" with "Motor mount", etc.
```

### Example 3: Batch processing with scripts

```bash
#!/bin/bash
for file in *.3mf; do
    python text_3mf_editor.py "$file" "processed_$file" "Draft" "Final"
done
```

## Troubleshooting

### "No modifiable text content found"
- The 3MF file may not contain slicer metadata
- Text might be part of the 3D geometry (not modifiable)
- Try opening the file in a slicer to see if text appears

### "No matching text found to replace"
- Use `--list-text` to see available text
- Check for exact spelling and capitalization
- Text might be in a different metadata format

### File corruption warnings
- Duplicate name warnings are normal and don't affect functionality
- Always test the output file before using in production

## Technical details

- **File Format**: 3MF (3D Manufacturing Format) 
- **Metadata Location**: ZIP archive metadata files
- **Text Storage**: XML attributes and elements
- **Encoding**: UTF-8 text encoding
- **Backup Strategy**: Copy original file with `.backup` extension

## License

MIT License - Free to use and modify.

## Contributing

This tool is part of the noah123d project. Contributions welcome!

---

**Need Help?** Run `python text_3mf_editor.py --help` for quick reference.
