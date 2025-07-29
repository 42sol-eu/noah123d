import sys
from pathlib import Path

# Add the parent directory to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from noah123d import STLConverter
    print("✅ Successfully imported noah123d")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test with a simple case first
stl_objects = [
    {'path': '../_models/multiverse/clip_dual_light.stl', 'count': 1, 'name': 'Light_Clip'},
]

print("🔍 Testing simple case first...")
print("📦 Simple assembly contents:")
for obj in stl_objects:
    stl_path = Path(obj['path'])
    if stl_path.exists():
        print(f"✅ {obj['count']}x {stl_path.name}")
    else:
        print(f"❌ Missing: {stl_path}")
        sys.exit(1)

# Create converter with debug info
converter = STLConverter(include_metadata=True, validate=True)

print("\n🔧 Testing individual STL info retrieval...")
for obj in stl_objects:
    stl_path = Path(obj['path'])
    print(f"Testing {stl_path.name}...")
    
    try:
        stl_info = converter.get_stl_info(stl_path)
        if stl_info and 'error' not in stl_info:
            print(f"✅ STL info retrieved successfully")
            print(f"   - Triangles: {stl_info.get('triangles', 'N/A')}")
            print(f"   - Vertices: {stl_info.get('unique_vertices', 'N/A')}")
            print(f"   - Dimensions: {stl_info.get('dimensions', 'N/A')}")
        else:
            print(f"❌ Failed to get STL info: {stl_info.get('error', 'Unknown error')}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Exception getting STL info: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("\n🔧 Testing assembly creation...")
try:
    success = converter.convert_multiple_stl_with_counts(
        stl_objects=stl_objects,
        output_path='test_simple.3mf',
        layout_mode='grid',
        spacing_factor=1.1,
        center_layout=True
    )
    
    if success:
        output_file = Path('test_simple.3mf')
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ Successfully created: {output_file.name} ({size_mb:.2f} MB)")
        else:
            print("❌ Function returned success but file was not created")
    else:
        print("❌ Assembly creation failed")
        
        # Get error details
        stats = converter.get_conversion_stats()
        if 'test_simple.3mf' in stats:
            if 'error' in stats['test_simple.3mf']:
                print(f"Error details: {stats['test_simple.3mf']['error']}")
            else:
                print(f"Stats: {stats['test_simple.3mf']}")
        
except Exception as e:
    print(f"❌ Exception during conversion: {e}")
    import traceback
    traceback.print_exc()
