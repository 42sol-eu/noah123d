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
    Path as ClickPath,
)
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.status import Status
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

# %% [Constants]
console = Console()

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
        # Run COG check with checksum verification from project root to avoid path issues
        cmd = ["cog", "-c", "--check"]
        if show_diff:
            cmd.append("--diff")
        cmd.append(str(file_path))  # Use full path when running from project root
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            # Run from project root to ensure consistent paths
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            return COGResult(
                file=cog_file,
                success=True,
                changed=False
            )
        else:
            # Check if it's a checksum protection warning
            error_output = result.stdout + result.stderr
            if "Output has been edited!" in error_output:
                return COGResult(
                    file=cog_file,
                    success=False,
                    changed=True,
                    warning_message="Manual edits detected - checksum protection active"
                )
            else:
                return COGResult(
                    file=cog_file,
                    success=False,
                    changed=True,
                    error_message=error_output
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
        # Run COG generation from project root to avoid path issues
        cmd = ["cog"]
        if with_checksum:
            cmd.append("-c")
        cmd.extend(["-r", str(file_path)])  # Use full path when running from project root
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            # Run from project root to ensure consistent paths
            cwd=Path.cwd()
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

# %% [Functions]
def get_status_icon(status: str) -> str:
    """Get the appropriate icon for a status."""
    icons = {
        "file": "📁",
        "generate": "⚙️",
        "check": "🔍", 
        "success": "✅",
        "change": "🔄",
        "warning": "⚠️",
        "error": "❌",
        "summary": "📊"
    }
    return icons.get(status, "•")

def get_status_color(status: str) -> str:
    """Get the appropriate color for a status."""
    colors = {
        "file": "cyan",
        "generate": "blue",
        "check": "yellow", 
        "success": "green",
        "change": "blue",
        "warning": "yellow",
        "error": "red",
        "summary": "magenta",
        "info": "bright_black"
    }
    return colors.get(status, "white")

def create_file_table(cog_file: COGFile, result: COGResult, mode: str, verbose: bool = False) -> Table:
    """Create a Rich table for a single file's COG processing."""
    
    table = Table(
        title=f"[bold cyan]{cog_file.relative_path}[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("Step", justify="right", style="dim", width=4)
    table.add_column("Status", justify="center", width=6)
    table.add_column("Description", style="white")
    
    step = 1
    
    # Step 1: File discovery
    table.add_row(
        str(step),
        get_status_icon("file"),
        "Discovered COG file",
        style=get_status_color("file")
    )
    step += 1
    
    if verbose:
        table.add_row(
            "",
            "",
            f"[{get_status_color('info')}]Blocks: {cog_file.cog_blocks}, Checksum: {'Yes' if cog_file.has_checksum else 'No'}[/{get_status_color('info')}]"
        )
        if cog_file.description:
            table.add_row(
                "",
                "",
                f"[{get_status_color('info')}]Type: {cog_file.description}[/{get_status_color('info')}]"
            )
    
    # Step 2: Processing
    if mode == "check":
        table.add_row(
            str(step),
            get_status_icon("check"),
            "Checking consistency",
            style=get_status_color("check")
        )
    else:
        table.add_row(
            str(step),
            get_status_icon("generate"),
            "Running generation",
            style=get_status_color("generate")
        )
    step += 1
    
    # Step 3: Result
    if result.success:
        if mode == "check":
            if result.changed:
                table.add_row(
                    str(step),
                    get_status_icon("change"),
                    "Needs regeneration",
                    style=get_status_color("change")
                )
                if verbose:
                    table.add_row(
                        "",
                        "",
                        f"[{get_status_color('info')}]File content differs from expected[/{get_status_color('info')}]"
                    )
            else:
                table.add_row(
                    str(step),
                    get_status_icon("success"),
                    "Up-to-date",
                    style=get_status_color("success")
                )
                if verbose:
                    table.add_row(
                        "",
                        "",
                        f"[{get_status_color('info')}]File matches expected content[/{get_status_color('info')}]"
                    )
        else:  # generate mode
            if result.changed:
                table.add_row(
                    str(step),
                    get_status_icon("success"),
                    "Generated and updated",
                    style=get_status_color("change")
                )
                if verbose:
                    table.add_row(
                        "",
                        "",
                        f"[{get_status_color('info')}]File content was updated[/{get_status_color('info')}]"
                    )
            else:
                table.add_row(
                    str(step),
                    get_status_icon("success"),
                    "No changes needed",
                    style=get_status_color("success")
                )
                if verbose:
                    table.add_row(
                        "",
                        "",
                        f"[{get_status_color('info')}]File already up-to-date[/{get_status_color('info')}]"
                    )
                    
    elif result.warning_message:
        table.add_row(
            str(step),
            get_status_icon("warning"),
            "Protected (manual edits)",
            style=get_status_color("warning")
        )
        if verbose:
            table.add_row(
                "",
                "",
                f"[{get_status_color('info')}]{result.warning_message}[/{get_status_color('info')}]"
            )
            
    else:
        # Determine error type for better messaging
        error_type = "Error occurred"
        if result.error_message:
            if "ModuleNotFoundError" in result.error_message:
                error_type = "Import error"
            elif "NameError" in result.error_message:
                error_type = "Python error"
            elif "FileNotFoundError" in result.error_message:
                error_type = "File not found"
            elif "Check failed" in result.error_message:
                error_type = "Content mismatch"
        
        table.add_row(
            str(step),
            get_status_icon("error"),
            error_type,
            style=get_status_color("error")
        )
        if verbose and result.error_message:
            # Show first 2 lines of error
            error_lines = result.error_message.split('\n')[:2]
            for line in error_lines:
                if line.strip():
                    table.add_row(
                        "",
                        "",
                        f"[{get_status_color('error')}]{line[:60]}[/{get_status_color('error')}]"
                    )
    
    return table

def create_summary_table(results: List[COGResult], mode: str) -> Table:
    """Create a Rich summary table for all results."""
    
    if not results:
        return None
        
    total = len(results)
    successful = sum(1 for r in results if r.success)
    changed = sum(1 for r in results if r.changed)
    errors = sum(1 for r in results if not r.success and not r.warning_message)
    warnings = sum(1 for r in results if r.warning_message)
    
    table = Table(
        title=f"[bold magenta]COG {mode.title()} Summary[/bold magenta]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Step", justify="right", style="dim", width=4)
    table.add_column("Status", justify="center", width=6)
    table.add_column("Description", style="white")
    
    step = 1
    table.add_row(
        str(step),
        get_status_icon("summary"),
        f"Total files processed: {total}",
        style=get_status_color("summary")
    )
    step += 1
    
    if mode == "check":
        if successful == total:
            table.add_row(
                str(step),
                get_status_icon("success"),
                f"All files up-to-date: {successful}",
                style=get_status_color("success")
            )
        else:
            table.add_row(
                str(step),
                get_status_icon("success"),
                f"Up-to-date: {successful}",
                style=get_status_color("success")
            )
            step += 1
            if changed > 0:
                table.add_row(
                    str(step),
                    get_status_icon("change"),
                    f"Need regeneration: {changed}",
                    style=get_status_color("change")
                )
    else:  # generate mode
        if successful > 0:
            table.add_row(
                str(step),
                get_status_icon("success"),
                f"Successfully processed: {successful}",
                style=get_status_color("success")
            )
            step += 1
        if changed > 0:
            table.add_row(
                str(step),
                get_status_icon("change"),
                f"Files changed: {changed}",
                style=get_status_color("change")
            )
            step += 1
            
    if warnings > 0:
        table.add_row(
            str(step),
            get_status_icon("warning"),
            f"Protected files (manual edits): {warnings}",
            style=get_status_color("warning")
        )
        step += 1
    if errors > 0:
        table.add_row(
            str(step),
            get_status_icon("error"),
            f"Errors: {errors}",
            style=get_status_color("error")
        )
        
    return table

@command()
@argument("folder", type=ClickPath(exists=True, file_okay=False, dir_okay=True))

def print_table_footer(width: int = 80):
    """Print a table footer."""
    secho("└" + "─" * (width - 2) + "┘", fg="cyan")

def print_file_table(cog_file: COGFile, result: COGResult, mode: str, verbose: bool = False, step_counter: int = 1):
    """Print a table for a single file's COG processing."""
    width = 80
    
    # Table header with file name
    title = f"{cog_file.relative_path}"
    print_table_header(title, width)
    
    current_step = step_counter
    
    # Step 1: File discovery
    print_table_row(current_step, "�", f"Discovered COG file", width, "white")
    current_step += 1
    
    if verbose:
        print_table_detail_row(f"    Blocks: {cog_file.cog_blocks}, Checksum: {'Yes' if cog_file.has_checksum else 'No'}", width)
        if cog_file.description:
            print_table_detail_row(f"    Type: {cog_file.description}", width)
    
    # Step 2: Processing
    if mode == "check":
        print_table_row(current_step, "?", "Checking consistency", width, "cyan")
    else:
        print_table_row(current_step, "G", "Running generation", width, "cyan")
    current_step += 1
    
    # Step 3: Result
    if result.success:
        if mode == "check":
            if result.changed:
                print_table_row(current_step, "!", "Needs regeneration", width, "yellow")
                if verbose:
                    print_table_detail_row("    File content differs from expected", width)
            else:
                print_table_row(current_step, "+", "Up-to-date", width, "green")
                if verbose:
                    print_table_detail_row("    File matches expected content", width)
        else:  # generate mode
            if result.changed:
                print_table_row(current_step, "+", "Generated and updated", width, "blue")
                if verbose:
                    print_table_detail_row("    File content was updated", width)
            else:
                print_table_row(current_step, "+", "No changes needed", width, "green")
                if verbose:
                    print_table_detail_row("    File already up-to-date", width)
                    
    elif result.warning_message:
        print_table_row(current_step, "W", "Protected (manual edits)", width, "yellow")
        if verbose:
            print_table_detail_row(f"    {result.warning_message}", width)
            
    else:
        # Determine error type for better messaging
        error_type = "Error occurred"
        if result.error_message:
            if "ModuleNotFoundError" in result.error_message:
                error_type = "Import error"
            elif "NameError" in result.error_message:
                error_type = "Python error"
            elif "FileNotFoundError" in result.error_message:
                error_type = "File not found"
            elif "Check failed" in result.error_message:
                error_type = "Content mismatch"
                
        print_table_row(current_step, "X", error_type, width, "red")
        if verbose and result.error_message:
            for line in result.error_message.split('\n')[:2]:  # Show first 2 lines
                if line.strip():
                    print_table_detail_row(f"    {line[:width-8]}", width)
    
    print_table_footer(width)
    echo()  # Add spacing between tables

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
    
    width = 80
    print_table_header(f"COG {mode.title()} Summary", width)
    
    step = 1
    print_table_row(step, "S", f"Total files processed: {total}", width, "white")
    step += 1
    
    if mode == "check":
        if successful == total:
            print_table_row(step, "+", f"All files up-to-date: {successful}", width, "green")
        else:
            print_table_row(step, "+", f"Up-to-date: {successful}", width, "green")
            step += 1
            if changed > 0:
                print_table_row(step, "!", f"Need regeneration: {changed}", width, "yellow")
    else:  # generate mode
        if successful > 0:
            print_table_row(step, "+", f"Successfully processed: {successful}", width, "green")
            step += 1
        if changed > 0:
            print_table_row(step, "!", f"Files changed: {changed}", width, "blue")
            step += 1
            
    if warnings > 0:
        print_table_row(step, "W", f"Protected files (manual edits): {warnings}", width, "yellow")
        step += 1
    if errors > 0:
        print_table_row(step, "X", f"Errors: {errors}", width, "red")
        
    print_table_footer(width)

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
    
    # Header with Rich
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🔧 COG Automation Runner[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    mode = "check" if check else "generate"
    
    # Info panel
    info_content = [
        f"[bold]Mode:[/bold] {mode.title()}",
        f"[bold]Folder:[/bold] {folder_path}",
    ]
    if not check:
        checksum_status = "disabled" if no_checksum else "enabled"
        info_content.append(f"[bold]Checksum protection:[/bold] {checksum_status}")
    
    console.print(Panel("\n".join(info_content), title="Configuration", border_style="blue"))
    console.print()
    
    # Find all COG files
    with Status("[cyan]🔍 Discovering COG files...", console=console) as status:
        cog_files = find_cog_files(folder_path)
    
    if not cog_files:
        console.print("[yellow]No files with COG automation found.[/yellow]")
        return
    
    # Show discovered files
    console.print(f"[green]Found {len(cog_files)} files with COG automation:[/green]")
    console.print()
    
    files_table = Table(box=box.SIMPLE)
    files_table.add_column("File", style="cyan")
    files_table.add_column("Blocks", justify="center", style="yellow")
    files_table.add_column("Checksum", justify="center", style="green")
    if verbose:
        files_table.add_column("Description", style="bright_black")
    
    for cog_file in cog_files:
        checksum_icon = "🔒" if cog_file.has_checksum else "🔓"
        row = [
            str(cog_file.relative_path),
            str(cog_file.cog_blocks),
            checksum_icon
        ]
        if verbose:
            row.append(cog_file.description or "")
        files_table.add_row(*row)
    
    console.print(files_table)
    console.print()
    
    # Process files
    if check:
        console.print("[cyan]🔍 Checking COG consistency...[/cyan]")
    else:
        console.print("[cyan]⚙️ Running COG generation...[/cyan]")
    console.print()
    
    results = []
    for i, cog_file in enumerate(cog_files, 1):
        if check:
            result = run_cog_check(cog_file.path, show_diff=diff)
        else:
            result = run_cog_generate(cog_file.path, with_checksum=not no_checksum)
        
        results.append(result)
        
        # Show individual file table
        file_table = create_file_table(cog_file, result, mode, verbose)
        console.print(file_table)
        console.print()
    
    # Summary
    summary_table = create_summary_table(results, mode)
    if summary_table:
        console.print(summary_table)
        console.print()
    
    # Exit with appropriate code
    if any(not r.success and not r.warning_message for r in results):
        sys.exit(1)  # Errors occurred
    elif check and any(r.changed for r in results):
        sys.exit(1)  # Files need regeneration

if __name__ == "__main__":
    cli()
