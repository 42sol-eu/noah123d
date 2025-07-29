"""Main module for Noah123D CLI application."""

import click
from rich.console import Console
from stl import mesh
import numpy as np

console = Console()


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='STL file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def main(file, verbose):
    """Noah123D - Building assemblies from STL models."""
    if verbose:
        console.print("[green]Noah123D started[/green]")
    
    if file:
        console.print(f"[blue]Loading STL file:[/blue] {file}")
        try:
            # Load the STL file
            stl_mesh = mesh.Mesh.from_file(file)
            console.print(f"[green]✓[/green] Successfully loaded STL with {len(stl_mesh.vectors)} triangles")
            
            if verbose:
                console.print(f"[dim]Mesh bounds:[/dim]")
                console.print(f"  X: {stl_mesh.x.min():.2f} to {stl_mesh.x.max():.2f}")
                console.print(f"  Y: {stl_mesh.y.min():.2f} to {stl_mesh.y.max():.2f}")
                console.print(f"  Z: {stl_mesh.z.min():.2f} to {stl_mesh.z.max():.2f}")
                
        except Exception as e:
            console.print(f"[red]✗[/red] Error loading STL file: {e}")
    else:
        console.print("[yellow]No STL file specified. Use --file option.[/yellow]")


if __name__ == "__main__":
    main()
