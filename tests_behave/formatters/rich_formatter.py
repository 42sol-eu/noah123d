"""
Custom colorful formatter for behave using rich.
This provides enhanced colorful output for BDD test results.
"""

from behave.formatter.base import Formatter
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import sys


class RichFormatter(Formatter):
    """A colorful formatter using Rich library."""
    
    name = 'rich'
    description = 'Colorful formatter using Rich library'
    
    def __init__(self, stream_opener, config):
        super(RichFormatter, self).__init__(stream_opener, config)
        self.console = Console(file=sys.stdout, force_terminal=True)
        self.feature_count = 0
        self.scenario_count = 0
        self.step_count = 0
        self.failed_scenarios = []
        self.failed_steps = []
        
    def uri(self, uri):
        """Called when a new feature file is processed."""
        pass
        
    def feature(self, feature):
        """Called when a feature starts."""
        self.feature_count += 1
        
        # Create feature header
        feature_text = Text(f"Feature: {feature.name}")
        feature_text.stylize("bold blue")
        
        # Handle description properly - it might be a list
        description_text = ""
        if feature.description:
            if isinstance(feature.description, list):
                description_text = "\n".join(feature.description)
            else:
                description_text = str(feature.description)
        
        description = Text(description_text)
        description.stylize("dim")
        
        self.console.print()
        self.console.print(Panel.fit(
            f"{feature_text}\n{description}",
            border_style="blue",
            padding=(0, 1)
        ))
        
    def background(self, background):
        """Called when a background starts."""
        bg_text = Text("Background:")
        bg_text.stylize("bold yellow")
        self.console.print(f"  {bg_text}")
        
    def scenario(self, scenario):
        """Called when a scenario starts."""
        self.scenario_count += 1
        scenario_text = Text(f"Scenario: {scenario.name}")
        scenario_text.stylize("bold cyan")
        self.console.print(f"  {scenario_text}")
        
    def step(self, step):
        """Called when a step starts."""
        self.step_count += 1
        
        # Format step with appropriate colors
        keyword_color = {
            'Given': 'blue',
            'When': 'yellow', 
            'Then': 'green',
            'And': 'white',
            'But': 'white'
        }.get(step.keyword.strip(), 'white')
        
        keyword = Text(step.keyword)
        keyword.stylize(f"bold {keyword_color}")
        
        step_text = Text(step.name)
        step_text.stylize("white")
        
        # Show step status with icons
        if step.status == 'passed':
            icon = "✅"
            status_color = "green"
        elif step.status == 'failed':
            icon = "❌"
            status_color = "red"
            self.failed_steps.append(step)
        elif step.status == 'skipped':
            icon = "⏭️"
            status_color = "yellow"
        elif step.status == 'undefined':
            icon = "❓"
            status_color = "magenta"
        else:
            icon = "⏸️"
            status_color = "white"
            
        duration = f"({step.duration:.3f}s)" if hasattr(step, 'duration') and step.duration else ""
        
        self.console.print(f"    {icon} {keyword}{step_text} [{status_color}]{duration}[/{status_color}]")
        
        # Show error details for failed steps
        if step.status == 'failed' and step.exception:
            error_text = Text(str(step.exception))
            error_text.stylize("red")
            self.console.print(Panel.fit(
                error_text,
                title="Error Details",
                border_style="red",
                padding=(0, 1)
            ))
    
    def match(self, match):
        """Called when a step definition is matched."""
        pass
        
    def result(self, result):
        """Called when a step result is available."""
        pass
        
    def eof(self):
        """Called at the end of processing."""
        # Create summary table
        table = Table(title="🧪 BDD Test Summary", show_header=True, header_style="bold blue")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Count", style="green", justify="right")
        table.add_column("Status", style="yellow")
        
        # Calculate totals
        passed_scenarios = self.scenario_count - len(self.failed_scenarios)
        passed_steps = self.step_count - len(self.failed_steps)
        
        table.add_row("Features", str(self.feature_count), "✅" if self.feature_count > 0 else "❌")
        table.add_row("Scenarios", str(self.scenario_count), "✅" if len(self.failed_scenarios) == 0 else "❌")
        table.add_row("- Passed", str(passed_scenarios), "✅")
        table.add_row("- Failed", str(len(self.failed_scenarios)), "❌" if len(self.failed_scenarios) > 0 else "✅")
        table.add_row("Steps", str(self.step_count), "✅" if len(self.failed_steps) == 0 else "❌")
        table.add_row("- Passed", str(passed_steps), "✅")
        table.add_row("- Failed", str(len(self.failed_steps)), "❌" if len(self.failed_steps) > 0 else "✅")
        
        self.console.print()
        self.console.print(table)
        
        # Overall result
        if len(self.failed_scenarios) == 0 and len(self.failed_steps) == 0:
            self.console.print("\n🎉 [bold green]All tests passed![/bold green] 🎉")
        else:
            self.console.print(f"\n❌ [bold red]{len(self.failed_scenarios)} scenario(s) and {len(self.failed_steps)} step(s) failed[/bold red]")
    
    def close(self):
        """Called to close the formatter."""
        pass
