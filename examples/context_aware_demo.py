"""Demo showing the improved context-aware Model class methods."""

from pathlib import Path
from rich import print
from rich.console import Console
from noah123d import Archive3mf, Directory, Model


def demo_context_aware_methods():
    """Demonstrate the context-aware Model class methods."""
    console = Console()
    console.print("[bold blue]🎯 Context-Aware Model Methods Demo[/bold blue]")
    
    console.print("\n[green]The Model class now uses the proper context system:[/green]")
    console.print("• Methods work within existing Archive3mf and Directory contexts")
    console.print("• No duplicate context creation")
    console.print("• Proper separation of concerns")
    console.print("• Better integration with the library's architecture")
    
    console.print(f"\n[yellow]Available Methods:[/yellow]")
    console.print("🔧 Instance methods (work within existing context):")
    console.print("   • model.load_stl_with_info(stl_path)")
    console.print("   • model.analyze_model_content()")
    console.print("   • model.add_conversion_metadata(stl_path)")
    
    console.print("\n🏗️ Class methods (create their own context):")
    console.print("   • Model.convert_stl_to_3mf(stl_path, output_path)")
    console.print("   • Model.analyze_3mf_content(file_path)")
    console.print("   • Model.batch_convert_stl_files(input_dir, output_dir)")
    
    console.print(f"\n[cyan]Context Usage Examples:[/cyan]")
    
    # Example 1: Using instance methods within context
    console.print("\n1️⃣ Working within existing context:")
    console.print("```python")
    console.print("with Archive3mf('output.3mf', 'w') as archive:")
    console.print("    with Directory('3D') as models_dir:")
    console.print("        with Model() as model:")
    console.print("            obj_id = model.load_stl_with_info(Path('model.stl'))")
    console.print("            model.analyze_model_content()")
    console.print("            model.add_conversion_metadata(Path('model.stl'))")
    console.print("```")
    
    # Example 2: Using class methods (self-contained)
    console.print("\n2️⃣ Using class methods (handles context internally):")
    console.print("```python")
    console.print("# Single conversion")
    console.print("Model.convert_stl_to_3mf(Path('input.stl'), Path('output.3mf'))")
    console.print("")
    console.print("# Analysis")
    console.print("Model.analyze_3mf_content(Path('output.3mf'))")
    console.print("")
    console.print("# Batch processing")
    console.print("Model.batch_convert_stl_files(Path('stl_dir'), Path('3mf_dir'))")
    console.print("```")
    
    # Create a simple demo if we have the directory
    output_file = Path("demo_empty.3mf")
    console.print(f"\n[blue]Creating demo file: {output_file}[/blue]")
    
    result = Model.create_empty_3mf(output_file)
    if result:
        console.print(f"✅ Demo file created: {result}")
        
        # Analyze the created file
        console.print("\n[blue]Analyzing the created file:[/blue]")
        Model.analyze_3mf_content(result)
        
        # Clean up
        try:
            result.unlink()
            console.print(f"🧹 Cleaned up demo file: {result}")
        except:
            pass
    
    console.print(f"\n[bold green]✨ Context-aware integration completed![/bold green]")


def demo_advanced_context_usage():
    """Show advanced usage of context-aware methods."""
    console = Console()
    console.print("\n[bold magenta]🚀 Advanced Context Usage Demo[/bold magenta]")
    
    # This would be used when you need more control over the process
    console.print("\n[yellow]Advanced usage with custom context management:[/yellow]")
    console.print("```python")
    console.print("# Create archive with custom structure")
    console.print("with Archive3mf('custom.3mf', 'w') as archive:")
    console.print("    # Add multiple models in the same directory")
    console.print("    with Directory('3D') as models_dir:")
    console.print("        ")
    console.print("        # First model")
    console.print("        with Model('model1.model') as model1:")
    console.print("            model1.load_stl_with_info(Path('part1.stl'))")
    console.print("            model1.add_conversion_metadata(Path('part1.stl'))")
    console.print("        ")
    console.print("        # Second model")
    console.print("        with Model('model2.model') as model2:")
    console.print("            model2.load_stl_with_info(Path('part2.stl'))")
    console.print("            model2.add_conversion_metadata(Path('part2.stl'))")
    console.print("    ")
    console.print("    # Add custom metadata")
    console.print("    with Directory('Metadata') as meta_dir:")
    console.print("        meta_dir.create_file('assembly_info.xml', xml_content)")
    console.print("```")
    
    console.print("\n[green]Benefits of this approach:[/green]")
    console.print("✅ Proper context management - no resource leaks")
    console.print("✅ Consistent with library architecture")
    console.print("✅ Flexible - can work within existing contexts or create new ones")
    console.print("✅ Maintainable - single responsibility principle")
    console.print("✅ Extensible - easy to add new context-aware methods")


if __name__ == "__main__":
    demo_context_aware_methods()
    demo_advanced_context_usage()
