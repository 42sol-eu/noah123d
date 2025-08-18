#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
COG automation runner for noah123d project.
----
file:
    name:        run_cog.py  
    uuid:        8a1c9e5f-3d2b-4c8e-a9f7-1b8d4e6c2a9f
description:     COG automation runner for noah123d project
authors:         felix@42sol.eu
project:
    name:        a7d
    uuid:        2cc2a024-ae2a-4d2c-91c2-f41348980f7f
    url:         https://github.com/42sol-eu/a7d
"""

# %% [External imports]
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from click import (
    command,
    argument,
    option,
    secho,
    echo,
    style,
    Path as ClickPath,
)

# %% [Classes]
@dataclass
class COGFile:
    """Represents a file with COG automation."""
    path: Path
    relative_path: Path
    has_checksum: bool
    cog_blocks: int
    description: str = ""

@dataclass 
class COGResult:
    """Result of running COG on a file."""
    file: COGFile
    success: bool
    changed: bool
    error_message: str = ""
    warning_message: str = ""

# %% [Functions]
def find_cog_files(folder: Path) -> List[COGFile]:
    """Find all files with COG automation in the given folder."""
    cog_files = []
    
    # Recursively search for files with COG markers
    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.py', '.md', '.txt', '.rst']:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Check for COG markers
                if "# [[[cog" in content or ".. [[[cog" in content:
                    # Count COG blocks
                    cog_blocks = content.count("[[[cog")
                    
                    # Check for checksums
                    has_checksum = "(sum:" in content
                    
                    # Try to determine description from file type
                    description = get_file_description(file_path, content)
                    
                    try:
                        relative_path = file_path.relative_to(folder)
                    except ValueError:
                        relative_path = file_path
                    
                    cog_files.append(COGFile(
                        path=file_path,
                        relative_path=relative_path,
                        has_checksum=has_checksum,
                        cog_blocks=cog_blocks,
                        description=description
                    ))
                    
            except (UnicodeDecodeError, PermissionError):
                # Skip files that can't be read
                continue
                
    return sorted(cog_files, key=lambda f: str(f.relative_path))

def get_file_description(file_path: Path, content: str) -> str:
    """Determine a description for the COG file based on its content and location."""
    if file_path.name == "__init__.py":
        return "Package initialization and exports"
    elif "update_init" in content or "collect_init" in content:
        return "__init__.py management automation"
    elif file_path.suffix == ".md":
        return "Documentation generation"
    elif "dataclass" in content:
        return "Dataclass automation"
    elif "test_" in file_path.name:
        return "Test code generation"
    else:
        return "Code generation"

def run_cog_check(file_path: Path, show_diff: bool = False) -> COGResult:
    """Run COG check on a single file."""
    cog_file = COGFile(
        path=file_path,
        relative_path=file_path,
        has_checksum="(sum:" in file_path.read_text(),
        cog_blocks=file_path.read_text().count("[[[cog"),
    )
    
    try:
        # Run COG check
        cmd = ["cog", "--check"]
        if show_diff:
            cmd.append("--diff")
        cmd.append(str(file_path))
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=file_path.parent
        )
        
        if result.returncode == 0:
            return COGResult(
                file=cog_file,
                success=True,
                changed=False
            )
        else:
            return COGResult(
                file=cog_file,
                success=False,
                changed=True,
                error_message=result.stdout + result.stderr
            )
            
    except FileNotFoundError:
        return COGResult(
            file=cog_file,
            success=False,
            changed=False,
            error_message="COG not found. Install with: pip install cogapp"
        )
    except Exception as e:
        return COGResult(
            file=cog_file,
            success=False,
            changed=False,
            error_message=f"Error running COG: {e}"
        )

def run_cog_generate(file_path: Path, with_checksum: bool = True) -> COGResult:
    """Run COG generation on a single file."""
    cog_file = COGFile(
        path=file_path,
        relative_path=file_path,
        has_checksum="(sum:" in file_path.read_text(),
        cog_blocks=file_path.read_text().count("[[[cog"),
    )
    
    try:
        # Run COG generation
        cmd = ["cog"]
        if with_checksum:
            cmd.append("-c")
        cmd.extend(["-r", str(file_path)])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=file_path.parent
        )
        
        if result.returncode == 0:
            changed = "(changed)" in result.stdout
            return COGResult(
                file=cog_file,
                success=True,
                changed=changed
            )
        else:
            # Check if it's a checksum protection error
            if "Output has been edited!" in result.stderr:
                return COGResult(
                    file=cog_file,
                    success=False,
                    changed=False,
                    warning_message="File has manual edits - checksum protection active"
                )
            else:
                return COGResult(
                    file=cog_file,
                    success=False,
                    changed=False,
                    error_message=result.stdout + result.stderr
                )
                
    except FileNotFoundError:
        return COGResult(
            file=cog_file,
            success=False,
            changed=False,
            error_message="COG not found. Install with: pip install cogapp"
        )
    except Exception as e:
        return COGResult(
            file=cog_file,
            success=False,
            changed=False,
            error_message=f"Error running COG: {e}"
        )

def print_results_summary(results: List[COGResult], mode: str):
    """Print a colorful summary of COG results."""
    if not results:
        secho("No COG files found.", fg="yellow")
        return
        
    total = len(results)
    successful = sum(1 for r in results if r.success)
    changed = sum(1 for r in results if r.changed)
    errors = sum(1 for r in results if not r.success and not r.warning_message)
    warnings = sum(1 for r in results if r.warning_message)
    
    echo()
    secho("=" * 60, fg="cyan")
    secho(f"COG {mode.title()} Summary", fg="cyan", bold=True)
    secho("=" * 60, fg="cyan")
    
    secho(f"📁 Total files: {total}", fg="white")
    
    if mode == "check":
        if successful == total:
            secho(f"✅ All files up-to-date: {successful}", fg="green")
        else:
            secho(f"✅ Up-to-date: {successful}", fg="green")
            if changed > 0:
                secho(f"🔄 Need regeneration: {changed}", fg="yellow")
    else:  # generate mode
        if successful > 0:
            secho(f"✅ Successfully processed: {successful}", fg="green")
        if changed > 0:
            secho(f"🔄 Files changed: {changed}", fg="blue")
            
    if warnings > 0:
        secho(f"⚠️  Protected files (manual edits): {warnings}", fg="yellow")
    if errors > 0:
        secho(f"❌ Errors: {errors}", fg="red")
        
    echo()

def print_file_result(result: COGResult, mode: str, verbose: bool = False):
    """Print the result for a single file."""
    file_path = result.file.relative_path
    
    if result.success:
        if mode == "check":
            if result.changed:
                secho(f"🔄 {file_path}", fg="yellow")
                if verbose:
                    echo(f"   Needs regeneration")
            else:
                secho(f"✅ {file_path}", fg="green")
                if verbose:
                    echo(f"   Up-to-date")
        else:  # generate mode
            if result.changed:
                secho(f"🔄 {file_path}", fg="blue")
                if verbose:
                    echo(f"   Generated and updated")
            else:
                secho(f"✅ {file_path}", fg="green")
                if verbose:
                    echo(f"   No changes needed")
                    
    elif result.warning_message:
        secho(f"⚠️  {file_path}", fg="yellow")
        if verbose:
            echo(f"   {result.warning_message}")
            
    else:
        secho(f"❌ {file_path}", fg="red")
        if verbose and result.error_message:
            for line in result.error_message.split('\n')[:3]:  # Show first 3 lines
                if line.strip():
                    echo(f"   {line}")

@command()
@argument("folder", type=ClickPath(exists=True, file_okay=False, dir_okay=True))
@option(
    "--check",
    is_flag=True,
    default=False,
    help="Check if files need regeneration instead of generating."
)
@option(
    "--no-checksum",
    is_flag=True,
    default=False,
    help="Generate without checksum protection (not recommended)."
)
@option(
    "--diff",
    is_flag=True,
    default=False,
    help="Show diff output when checking (only with --check)."
)
@option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Show detailed output for each file."
)
def cli(folder, check, no_checksum, diff, verbose):
    """Discover and run COG automation in the specified folder.
    
    This script finds all files with COG markers and either checks if they
    need regeneration or runs the COG generation process.
    
    Examples:
        ./a7d/run_cog.py src/noah123d           # Generate all COG files
        ./a7d/run_cog.py src/noah123d --check   # Check if files need updates
        ./a7d/run_cog.py . --verbose            # Generate with detailed output
    """
    folder_path = Path(folder).resolve()
    
    # Header
    secho("🔧 COG Automation Runner", fg="cyan", bold=True)
    secho("=" * 60, fg="cyan")
    
    mode = "check" if check else "generate"
    secho(f"Mode: {mode.title()}", fg="white")
    secho(f"Folder: {folder_path}", fg="white")
    if not check:
        checksum_status = "disabled" if no_checksum else "enabled"
        secho(f"Checksum protection: {checksum_status}", fg="white")
    echo()
    
    # Find all COG files
    secho("🔍 Discovering COG files...", fg="cyan")
    cog_files = find_cog_files(folder_path)
    
    if not cog_files:
        secho("No files with COG automation found.", fg="yellow")
        return
        
    secho(f"Found {len(cog_files)} files with COG automation:", fg="green")
    
    for cog_file in cog_files:
        checksum_icon = "🔒" if cog_file.has_checksum else "🔓"
        blocks_info = f"({cog_file.cog_blocks} block{'s' if cog_file.cog_blocks != 1 else ''})"
        secho(f"  {checksum_icon} {cog_file.relative_path} {blocks_info}", fg="white")
        if verbose and cog_file.description:
            secho(f"     {cog_file.description}", fg="dim_white")
    
    echo()
    
    # Process files
    if check:
        secho("🔍 Checking COG consistency...", fg="cyan")
    else:
        secho("⚙️  Running COG generation...", fg="cyan")
    
    results = []
    for cog_file in cog_files:
        if check:
            result = run_cog_check(cog_file.path, show_diff=diff)
        else:
            result = run_cog_generate(cog_file.path, with_checksum=not no_checksum)
        
        results.append(result)
        print_file_result(result, mode, verbose)
    
    # Summary
    print_results_summary(results, mode)
    
    # Exit with appropriate code
    if any(not r.success and not r.warning_message for r in results):
        sys.exit(1)  # Errors occurred
    elif check and any(r.changed for r in results):
        sys.exit(1)  # Files need regeneration

if __name__ == "__main__":
    cli()
