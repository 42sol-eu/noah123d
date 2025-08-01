#!/usr/bin/env python3
"""
Utility script to run BDD tests with behave.
This script provides various options for running the BDD test suite.
"""

import subprocess
import sys
from pathlib import Path
import argparse
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()

def run_behave_tests(args_list=None):
    """Run behave tests with the given arguments."""
    if args_list is None:
        args_list = []
    
    # Change to the tests_behave directory
    tests_dir = Path(__file__).parent
    
    # Create a beautiful header
    cmd_text = Text(' '.join(['poetry', 'run', 'behave'] + args_list))
    cmd_text.stylize("bold cyan")
    
    console.print(Panel.fit(
        f"🧪 [bold green]Running BDD Tests[/bold green]\n"
        f"📂 Directory: [yellow]{tests_dir}[/yellow]\n"
        f"🚀 Command: {cmd_text}",
        border_style="blue"
    ))
    
    try:
        # Run behave with poetry to ensure proper environment
        cmd = ['poetry', 'run', 'behave'] + args_list
        
        # Set environment for custom formatters
        import os
        env = os.environ.copy()
        env['PYTHONPATH'] = str(tests_dir)
        
        result = subprocess.run(
            cmd,
            cwd=tests_dir,
            capture_output=False,
            text=True,
            env=env
        )
        
        # Show completion status with colors
        if result.returncode == 0:
            console.print("✅ [bold green]Tests completed successfully![/bold green]")
        else:
            console.print(f"❌ [bold red]Tests failed with exit code {result.returncode}[/bold red]")
        
        return result.returncode
    
    except FileNotFoundError:
        console.print("❌ [bold red]Error:[/bold red] poetry not found. Make sure Poetry is installed and available in PATH.")
        return 1
    except Exception as e:
        console.print(f"❌ [bold red]Error running behave:[/bold red] {e}")
        return 1


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run BDD tests with behave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎨 Colorful Output Examples:
  python run_bdd_tests.py --rich                    # Use Rich formatter (colorful)
  python run_bdd_tests.py --format=allure          # Generate Allure HTML reports
  python run_bdd_tests.py --format=rich            # Same as --rich
  
📋 General Examples:
  python run_bdd_tests.py                          # Run all tests (default colors)
  python run_bdd_tests.py --tags=@slow            # Run only slow tests
  python run_bdd_tests.py --tags="not @slow"      # Run all except slow tests  
  python run_bdd_tests.py --name="CLI"            # Run tests with "CLI" in name
  python run_bdd_tests.py --dry-run               # Show which tests would run
  python run_bdd_tests.py features/cli_basic.feature  # Run specific feature

🚀 Advanced Options:
  python run_bdd_tests.py --rich --verbose        # Rich output with verbose details
  python run_bdd_tests.py --format=allure --allure-results=reports  # Custom report dir
        """
    )
    
    parser.add_argument('features', nargs='*', help='Specific feature files to run')
    parser.add_argument('--tags', '-t', help='Run scenarios with specific tags')
    parser.add_argument('--name', '-n', help='Run scenarios matching name pattern')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Show which tests would run without executing')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--format', '-f', default='pretty', 
                        choices=['pretty', 'rich', 'allure', 'json', 'junit'],
                        help='Output format (pretty, rich, allure, json, junit)')
    parser.add_argument('--no-capture', action='store_true', help='Don\'t capture stdout/stderr')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--allure-results', default='allure-results', 
                        help='Directory for Allure results (default: allure-results)')
    parser.add_argument('--rich', action='store_true', help='Use Rich formatter for colorful output')
    
    args = parser.parse_args()
    
    # Build behave arguments
    behave_args = []
    
    if args.tags:
        behave_args.extend(['--tags', args.tags])
    
    if args.name:
        behave_args.extend(['--name', args.name])
    
    if args.dry_run:
        behave_args.append('--dry-run')
    
    if args.verbose:
        behave_args.append('--verbose')
    
    # Handle different formatters
    if args.rich or args.format == 'rich':
        behave_args.extend(['--format', 'formatters.rich_formatter:RichFormatter'])
    elif args.format == 'allure':
        behave_args.extend(['--format', 'allure_behave.formatter:AllureFormatter'])
        behave_args.extend(['--outdir', args.allure_results])
    elif args.format != 'pretty':
        behave_args.extend(['--format', args.format])
    
    if args.no_capture:
        behave_args.extend(['--no-capture', '--no-capture-stderr'])
    
    if args.no_color:
        behave_args.append('--no-color')
    
    # Add specific feature files if provided
    if args.features:
        behave_args.extend(args.features)
    
    # Run the tests
    exit_code = run_behave_tests(behave_args)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
