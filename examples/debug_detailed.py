import sys
from pathlib import Path

# Add the parent directory to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from noah123d import STLConverter

def debug_detailed_conversion():
    """Debug the multi-STL conversion process in detail."""
    
    stl_objects = [
        {'path': '../_models/multiverse/clip_dual_light.stl', 'count': 2, 'name': 'Light_Clip'},
        {'path': '../_models/multiverse/clip_dual.stl', 'count': 2, 'name': 'Regular_Clip'},
        {'path': '../_models/multiverse/tile_2x2_border.stl', 'count': 1, 'name': 'Border_Tile'}
    ]
    
    print("🔍 Detailed debugging of multi-STL conversion...")
    
    # Create converter
    converter = STLConverter(include_metadata=True, validate=True)
    
    # Test STL info for each file
    print("\n📋 STL File Analysis:")
    processed_objects = []
    total_expected_objects = 0
    
    for obj_spec in stl_objects:
        stl_path = Path(obj_spec['path'])
        count = obj_spec['count']
        name = obj_spec['name']
        
        print(f"\n🔍 Processing: {name}")
        print(f"   File: {stl_path.name}")
        print(f"   Count: {count}")
        
        if not stl_path.exists():
            print(f"   ❌ File not found!")
            continue
            
        stl_info = converter.get_stl_info(stl_path)
        if stl_info and 'error' not in stl_info:
            print(f"   ✅ STL loaded successfully")
            print(f"   📊 Triangles: {stl_info['triangles']:,}")
            print(f"   📊 Vertices: {stl_info['unique_vertices']:,}")
            print(f"   📐 Dimensions: {stl_info['dimensions']}")
            
            processed_objects.append({
                'path': stl_path,
                'count': count,
                'name': name,
                'info': stl_info
            })
            total_expected_objects += count
        else:
            print(f"   ❌ Failed to load STL: {stl_info.get('error', 'Unknown error')}")
    
    print(f"\n🎯 Expected total objects: {total_expected_objects}")
    
    # Test layout calculation
    print(f"\n🧮 Testing layout calculation...")
    layout_positions = converter._calculate_multi_object_layout(
        processed_objects, 'grid', 1.1, True
    )
    
    print(f"   Calculated positions: {len(layout_positions)}")
    for i, pos in enumerate(layout_positions):
        print(f"   Position {i+1}: {pos}")
    
    if len(layout_positions) != total_expected_objects:
        print(f"   ❌ Position count mismatch! Expected {total_expected_objects}, got {len(layout_positions)}")
        return False
    
    print(f"\n🔧 Attempting conversion...")
    try:
        success = converter.convert_multiple_stl_with_counts(
            stl_objects=processed_objects,
            output_path='debug_assembly.3mf',
            layout_mode='grid',
            spacing_factor=1.1,
            center_layout=True
        )
        
        if success:
            print("✅ Conversion reported success")
            
            # Get detailed stats
            stats = converter.get_conversion_stats()
            if 'debug_assembly.3mf' in stats:
                assembly_stats = stats['debug_assembly.3mf']
                print(f"\n📊 Conversion Statistics:")
                print(f"   Total STL Files: {assembly_stats.get('total_stl_files', 'N/A')}")
                print(f"   Total Objects: {assembly_stats.get('total_objects', 'N/A')}")
                print(f"   Object Details Count: {len(assembly_stats.get('object_details', []))}")
                
                # Show object details
                for detail in assembly_stats.get('object_details', []):
                    print(f"   Object {detail['id']}: {detail['name']} (copy {detail['copy_number']})")
                    print(f"      Position: {detail['position']}")
                    print(f"      Triangles: {detail['triangles']:,}")
            
            # Verify file exists
            output_file = Path('debug_assembly.3mf')
            if output_file.exists():
                size_mb = output_file.stat().st_size / (1024 * 1024)
                print(f"\n✅ File created: {output_file.name} ({size_mb:.2f} MB)")
                return True
            else:
                print(f"\n❌ File was not created!")
                return False
        else:
            print("❌ Conversion failed")
            stats = converter.get_conversion_stats()
            if 'debug_assembly.3mf' in stats and 'error' in stats['debug_assembly.3mf']:
                print(f"Error: {stats['debug_assembly.3mf']['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during conversion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_detailed_conversion()
