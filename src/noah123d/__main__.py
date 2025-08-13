"""Main module for Noah123d CLI application."""

import click
from rich.console import Console
from stl import mesh
import numpy as np
from pathlib import Path 

console = Console()

__version__ = "0.1.0"

G_all_models = {}


def process_model(model : Path, verbose : bool =False):
    """Process a single STL model file."""
    global G_all_models
    if model in G_all_models.keys():
        console.print(f"[yellow]Skipping already loaded model:[/yellow] {model}")
        return
    mesh = load_model(model, verbose)
    mesh = move_model_origin(mesh, verbose)
    if mesh:
        G_all_models[model] = mesh

def load_model(model : Path, verbose : bool =False):
    """Load an STL model file and print its details."""
    if not model.is_file():
        console.print(f"[red]\u2717[/red] Model file not found: {model}")
        return None
    console.print(f"[blue]Loading STL model file:[/blue] {model}")
    try:
        # Load the STL file
        stl_mesh = mesh.Mesh.from_file(model)
        console.print(f"[green]\u2713[/green] Successfully loaded STL with {len(stl_mesh.vectors)} triangles")
        
        if verbose:
            show_mesh_bounds(f"[dim]Mesh bounds:[/dim]", stl_mesh)
            
    except Exception as e:
        console.print(f"[red]\u2717[/red] Error loading STL file: {e}")

    return stl_mesh 

def center_model_origin(stl_mesh: mesh.Mesh, verbose: bool = False):
    """Center the model at the origin."""
    if not isinstance(stl_mesh, mesh.Mesh):
        console.print(f"[red]\u2717[/red] Invalid model type: {type(stl_mesh)}")
        return None
    center = np.mean(stl_mesh.vectors, axis=(0, 1))
    stl_mesh.vectors -= center
    console.print(f"[green]\u2713[/green] Model centered at origin: {center}")
    
    if verbose:
        show_mesh_bounds("[dim]New mesh bounds[/dim]", stl_mesh)
    return stl_mesh

def move_model_origin(stl_mesh: mesh.Mesh, verbose: bool =False):
    """This moves the bounding box to the origin point (0,0,0)"""
    if not isinstance(stl_mesh, mesh.Mesh):
        console.print(f"[red]\u2717[/red] Invalid model type: {type(stl_mesh)}")
        return None
    min = np.min(stl_mesh.vectors, axis=(0, 1))
    stl_mesh.vectors -= min
    console.print(f"[green]\u2713[/green] Model moved to origin: {min}")

    if verbose:
        show_mesh_bounds("[dim]New mesh bounds[/dim]", stl_mesh)

    return stl_mesh

def show_mesh_bounds(title: str, stl_mesh: mesh.Mesh):
    console.print(title)
    console.print(f"  X: {stl_mesh.x.min():.2f} to {stl_mesh.x.max():.2f}")
    console.print(f"  Y: {stl_mesh.y.min():.2f} to {stl_mesh.y.max():.2f}")
    console.print(f"  Z: {stl_mesh.z.min():.2f} to {stl_mesh.z.max():.2f}")    




@click.command()
@click.option('--model', '-m', multiple=True, type=click.Path(exists=True), help='STL file path (can be used multiple times)')
@click.option('--directory', '-d', multiple=True, type=click.Path(exists=True), help='Directory containing multiple model files (can be used multiple times).')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--version', '-V', is_flag=True, help='Show version information')
def main(model, directory, verbose, version):
    """Noah123d - CLI for building assemblies from STL models."""
    global G_all_models
    
    if verbose:
        console.print("[green]noah123d started[/green]")
    if version:
        console.print(f"[blue]noah123d version:[/blue] {__version__}")
    if model:
        for model_path in model:
            process_model(Path(model_path), verbose)
    if directory:
        for dir_path in directory:
            console.print(f"[blue]Searching directory:[/blue] {dir_path}")
            for model_path in Path(dir_path).rglob("*.stl"):
                process_model(Path(model_path), verbose)

    if len(G_all_models) == 0:
        console.print("[yellow]No models loaded. Use --model {file-path} or --directory {path} option.[/yellow]")


if __name__ == "__main__":
    main()

