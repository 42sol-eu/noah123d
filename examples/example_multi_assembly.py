import sys
from pathlib import Path

# Add the parent directory to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from noah123d import multi_stl_to_3mf
    print("✅ Successfully imported noah123d")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure dependencies are installed: poetry install")
    sys.exit(1)

# Check if STL files exist
stl_objects = [
    {'path': '../_models/multiverse/clip_dual_light.stl', 'count': 2},
    {'path': '../_models/multiverse/clip_dual.stl', 'count': 2},
    {'path': '../_models/multiverse/tile_2x2_border.stl', 'count': 1}  # Fixed filename
]

print("🔍 Checking STL files...")
valid_objects = []
for obj in stl_objects:
    stl_path = Path(obj['path'])
    if stl_path.exists():
        print(f"✅ Found: {stl_path.name}")
        valid_objects.append(obj)
    else:
        print(f"❌ Missing: {stl_path}")

if not valid_objects:
    print("❌ No valid STL files found!")
    sys.exit(1)

print(f"\n🔧 Creating assembly with {len(valid_objects)} different STL types...")
print("📦 Assembly contents:")
for obj in valid_objects:
    print(f"   - {obj['count']}x {Path(obj['path']).name}")

try:
    success = multi_stl_to_3mf(
        valid_objects, 
        'ark_kit.3mf', 
        layout_mode='grid',
        include_metadata=True  # Explicitly enable metadata
    )
    
    if success:
        output_file = Path('ark_kit.3mf')
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ Successfully created: {output_file.name} ({size_mb:.2f} MB)")
        else:
            print("❌ Function returned success but file was not created")
    else:
        print("❌ Assembly creation failed")
        
        # Try to get more information about the failure
        from noah123d import STLConverter
        converter = STLConverter()
        stats = converter.get_conversion_stats()
        if 'ark_kit.3mf' in stats and 'error' in stats['ark_kit.3mf']:
            print(f"Error details: {stats['ark_kit.3mf']['error']}")

except Exception as e:
    print(f"❌ Error during conversion: {e}")
    import traceback
    traceback.print_exc()