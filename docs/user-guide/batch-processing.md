# Batch processing

Noah123d provides powerful batch processing capabilities for handling multiple STL files and creating large-scale 3D printing production runs.

## Overview

Batch processing features:

1. **Multiple file processing**: Convert entire directories of STL files
2. **Production workflows**: Automated grid generation for manufacturing
3. **Parallel processing**: Multi-threaded conversion for speed
4. **Progress tracking**: Real-time progress monitoring
5. **Error handling**: Robust error recovery and reporting

## Core functions

### `batch_convert_stl_to_3mf()`

Convert multiple STL files to individual 3MF files:

```python
from noah123d import batch_convert_stl_to_3mf

# Convert all STL files in a directory
results = batch_convert_stl_to_3mf(
    input_dir="stl_files/",
    output_dir="3mf_files/",
    include_metadata=True,
    validate=True,
    max_workers=4  # Parallel processing
)

# Check results
successful = sum(1 for r in results if r['success'])
print(f"Converted {successful}/{len(results)} files successfully")
```

### `batch_create_grids()`

Create grid layouts for multiple STL files:

```python
from noah123d import batch_create_grids

# Batch grid creation
grid_configs = [
    {"stl_path": "part1.stl", "count": 4, "grid_cols": 2},
    {"stl_path": "part2.stl", "count": 9, "grid_cols": 3},
    {"stl_path": "part3.stl", "count": 6, "grid_cols": 2},
]

results = batch_create_grids(
    configs=grid_configs,
    output_dir="production_grids/",
    spacing_factor=1.2,
    center_grid=True,
    max_workers=2
)
```

## Directory processing

### Process entire directories

```python
import os
from noah123d import STLConverter

def process_directory(input_dir, output_dir, **kwargs):
    """Process all STL files in a directory"""
    
    converter = STLConverter(include_metadata=True, validate=True)
    
    # Find all STL files
    stl_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.stl'):
                stl_files.append(os.path.join(root, file))
    
    print(f"Found {len(stl_files)} STL files")
    
    # Process each file
    results = []
    for i, stl_path in enumerate(stl_files, 1):
        print(f"Processing {i}/{len(stl_files)}: {os.path.basename(stl_path)}")
        
        # Generate output path
        relative_path = os.path.relpath(stl_path, input_dir)
        output_path = os.path.join(output_dir, relative_path.replace('.stl', '.3mf'))
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert file
        success = converter.convert(stl_path, output_path, **kwargs)
        results.append({
            'input_path': stl_path,
            'output_path': output_path,
            'success': success
        })
    
    return results

# Example usage
results = process_directory(
    input_dir="models/",
    output_dir="converted/",
    include_metadata=True,
    validate=True
)
```

### Filtered processing

```python
import fnmatch

def process_filtered_directory(input_dir, output_dir, pattern="*.stl", **kwargs):
    """Process files matching a specific pattern"""
    
    converter = STLConverter(include_metadata=True)
    
    # Find matching files
    matching_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if fnmatch.fnmatch(file.lower(), pattern.lower()):
                matching_files.append(os.path.join(root, file))
    
    print(f"Found {len(matching_files)} files matching '{pattern}'")
    
    # Process files
    for file_path in matching_files:
        output_path = file_path.replace(input_dir, output_dir).replace('.stl', '.3mf')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        success = converter.convert(file_path, output_path, **kwargs)
        status = "✅" if success else "❌"
        print(f"{status} {os.path.basename(file_path)}")

# Example: Process only "part_*.stl" files
process_filtered_directory(
    input_dir="designs/",
    output_dir="output/",
    pattern="part_*.stl"
)
```

## Production workflows

### Manufacturing batch

```python
from noah123d import STLConverter
from concurrent.futures import ThreadPoolExecutor
import time

def production_batch(stl_files, copies_per_part=12, grid_cols=3):
    """Create production batches with grids"""
    
    converter = STLConverter(include_metadata=True, validate=True)
    
    def process_part(stl_path):
        start_time = time.time()
        
        # Generate output path
        base_name = os.path.splitext(os.path.basename(stl_path))[0]
        output_path = f"production/{base_name}_batch_{copies_per_part}.3mf"
        
        # Create grid
        success = converter.convert_with_copies(
            stl_path=stl_path,
            output_path=output_path,
            count=copies_per_part,
            grid_cols=grid_cols,
            spacing_factor=1.15,
            center_grid=True
        )
        
        processing_time = time.time() - start_time
        
        # Get statistics
        stats = converter.get_conversion_stats() if success else None
        
        return {
            'stl_path': stl_path,
            'output_path': output_path,
            'success': success,
            'processing_time': processing_time,
            'stats': stats
        }
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_part, stl_files))
    
    # Generate summary
    successful = [r for r in results if r['success']]
    total_time = sum(r['processing_time'] for r in results)
    total_objects = sum(r['stats']['copies'] for r in successful if r['stats'])
    
    print(f"\n📊 Production Batch Summary:")
    print(f"   Processed: {len(successful)}/{len(stl_files)} files")
    print(f"   Total Objects: {total_objects:,}")
    print(f"   Total Time: {total_time:.1f}s")
    print(f"   Average Time per File: {total_time/len(stl_files):.1f}s")
    
    return results

# Example usage
stl_files = ["part1.stl", "part2.stl", "part3.stl"]
results = production_batch(stl_files, copies_per_part=16, grid_cols=4)
```

### Quality control batch

```python
def quality_control_batch(stl_files, test_counts=[1, 4, 9]):
    """Create multiple test grids for quality control"""
    
    converter = STLConverter(include_metadata=True, validate=True)
    
    for stl_path in stl_files:
        base_name = os.path.splitext(os.path.basename(stl_path))[0]
        
        print(f"\n🔍 Processing QC batch: {base_name}")
        
        for count in test_counts:
            # Determine grid layout
            if count == 1:
                grid_cols = 1
                suffix = "single"
            elif count == 4:
                grid_cols = 2
                suffix = "2x2"
            elif count == 9:
                grid_cols = 3
                suffix = "3x3"
            else:
                grid_cols = None
                suffix = f"{count}x"
            
            output_path = f"qc_testing/{base_name}_qc_{suffix}.3mf"
            
            success = converter.convert_with_copies(
                stl_path=stl_path,
                output_path=output_path,
                count=count,
                grid_cols=grid_cols,
                spacing_factor=1.2,
                center_grid=True
            )
            
            status = "✅" if success else "❌"
            print(f"   {status} {suffix}: {count} copies")

# Example usage
stl_files = ["prototype_v1.stl", "prototype_v2.stl"]
quality_control_batch(stl_files)
```

## Progress tracking

### Progress bar integration

```python
from tqdm import tqdm
import time

def batch_with_progress(stl_files, **kwargs):
    """Batch processing with progress bar"""
    
    converter = STLConverter(include_metadata=True)
    results = []
    
    # Create progress bar
    with tqdm(total=len(stl_files), desc="Converting STL files") as pbar:
        for stl_path in stl_files:
            # Update progress bar description
            filename = os.path.basename(stl_path)
            pbar.set_description(f"Converting {filename}")
            
            # Convert file
            output_path = stl_path.replace('.stl', '.3mf')
            success = converter.convert(stl_path, output_path, **kwargs)
            
            results.append({
                'input': stl_path,
                'output': output_path,
                'success': success
            })
            
            # Update progress
            pbar.update(1)
            time.sleep(0.1)  # Brief pause for visual feedback
    
    return results

# Example usage
stl_files = ["part1.stl", "part2.stl", "part3.stl"]
results = batch_with_progress(stl_files)
```

### Real-time statistics

```python
def batch_with_stats(stl_files, **kwargs):
    """Batch processing with real-time statistics"""
    
    converter = STLConverter(include_metadata=True, validate=True)
    
    start_time = time.time()
    total_triangles = 0
    total_objects = 0
    successful_conversions = 0
    
    print("🚀 Starting batch conversion...")
    print(f"Files to process: {len(stl_files)}")
    print("-" * 50)
    
    for i, stl_path in enumerate(stl_files, 1):
        file_start = time.time()
        filename = os.path.basename(stl_path)
        
        # Convert file
        output_path = stl_path.replace('.stl', '.3mf')
        success = converter.convert(stl_path, output_path, **kwargs)
        
        file_time = time.time() - file_start
        
        if success:
            successful_conversions += 1
            stats = converter.get_conversion_stats()
            total_triangles += stats.get('triangles', 0)
            total_objects += stats.get('copies', 1)
            
            print(f"✅ {i}/{len(stl_files)} {filename:<25} "
                  f"{stats.get('triangles', 0):>8,} tri "
                  f"{file_time:>6.1f}s")
        else:
            print(f"❌ {i}/{len(stl_files)} {filename:<25} "
                  f"{'FAILED':<8} "
                  f"{file_time:>6.1f}s")
        
        # Show running statistics
        elapsed = time.time() - start_time
        rate = total_triangles / elapsed if elapsed > 0 else 0
        
        if i % 5 == 0 or i == len(stl_files):  # Every 5 files or at end
            print(f"📊 Progress: {successful_conversions}/{i} successful, "
                  f"{total_triangles:,} triangles, "
                  f"{rate:,.0f} tri/s")
            print("-" * 50)
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n🎯 Batch Complete!")
    print(f"   Successful: {successful_conversions}/{len(stl_files)}")
    print(f"   Total Objects: {total_objects:,}")
    print(f"   Total Triangles: {total_triangles:,}")
    print(f"   Total Time: {total_time:.1f}s")
    print(f"   Average Rate: {total_triangles/total_time:,.0f} triangles/sec")

# Example usage
batch_with_stats(["model1.stl", "model2.stl", "model3.stl"])
```

## Error handling

### Robust batch processing

```python
import logging
from datetime import datetime

def robust_batch_processing(stl_files, **kwargs):
    """Batch processing with comprehensive error handling"""
    
    # Setup logging
    log_filename = f"batch_conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    converter = STLConverter(include_metadata=True, validate=True)
    results = {
        'successful': [],
        'failed': [],
        'errors': []
    }
    
    for i, stl_path in enumerate(stl_files, 1):
        try:
            filename = os.path.basename(stl_path)
            logging.info(f"Processing {i}/{len(stl_files)}: {filename}")
            
            # Check if input file exists
            if not os.path.exists(stl_path):
                raise FileNotFoundError(f"Input file not found: {stl_path}")
            
            # Generate output path
            output_path = stl_path.replace('.stl', '.3mf')
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert file
            success = converter.convert(stl_path, output_path, **kwargs)
            
            if success:
                results['successful'].append({
                    'input': stl_path,
                    'output': output_path,
                    'stats': converter.get_conversion_stats()
                })
                logging.info(f"✅ Successfully converted: {filename}")
            else:
                results['failed'].append(stl_path)
                logging.warning(f"❌ Conversion failed: {filename}")
                
        except Exception as e:
            error_msg = f"Error processing {stl_path}: {str(e)}"
            results['errors'].append({
                'file': stl_path,
                'error': str(e)
            })
            logging.error(error_msg)
            
            # Continue with next file
            continue
    
    # Summary
    logging.info(f"\n📊 Batch Processing Summary:")
    logging.info(f"   Successful: {len(results['successful'])}")
    logging.info(f"   Failed: {len(results['failed'])}")
    logging.info(f"   Errors: {len(results['errors'])}")
    logging.info(f"   Log file: {log_filename}")
    
    return results

# Example usage
stl_files = ["good_file.stl", "missing_file.stl", "corrupt_file.stl"]
results = robust_batch_processing(stl_files)
```

## Performance optimization

### Parallel processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def parallel_batch_processing(stl_files, max_workers=None, **kwargs):
    """High-performance parallel batch processing"""
    
    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), len(stl_files))
    
    print(f"🚀 Starting parallel processing with {max_workers} workers")
    
    def process_single_file(stl_path):
        """Process a single file"""
        converter = STLConverter(include_metadata=True, validate=True)
        
        try:
            output_path = stl_path.replace('.stl', '.3mf')
            success = converter.convert(stl_path, output_path, **kwargs)
            
            return {
                'input': stl_path,
                'output': output_path,
                'success': success,
                'stats': converter.get_conversion_stats() if success else None,
                'error': None
            }
        except Exception as e:
            return {
                'input': stl_path,
                'output': None,
                'success': False,
                'stats': None,
                'error': str(e)
            }
    
    # Process files in parallel
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_single_file, stl_path): stl_path 
            for stl_path in stl_files
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_file):
            stl_path = future_to_file[future]
            try:
                result = future.result()
                results.append(result)
                
                # Progress feedback
                status = "✅" if result['success'] else "❌"
                filename = os.path.basename(stl_path)
                print(f"{status} {len(results)}/{len(stl_files)} {filename}")
                
            except Exception as exc:
                print(f"❌ {stl_path} generated an exception: {exc}")
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n📊 Parallel Processing Complete:")
    print(f"   Successful: {successful}/{len(stl_files)}")
    print(f"   Workers used: {max_workers}")
    
    return results

# Example usage
stl_files = [f"part_{i}.stl" for i in range(10)]
results = parallel_batch_processing(stl_files, max_workers=4)
```

## Configuration management

### Batch configuration files

```python
import json
import yaml

def load_batch_config(config_path):
    """Load batch processing configuration from file"""
    
    with open(config_path, 'r') as f:
        if config_path.endswith('.json'):
            config = json.load(f)
        elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
            config = yaml.safe_load(f)
        else:
            raise ValueError("Config file must be JSON or YAML")
    
    return config

def process_from_config(config_path):
    """Process batch based on configuration file"""
    
    config = load_batch_config(config_path)
    
    # Extract settings
    input_dir = config['input_directory']
    output_dir = config['output_directory']
    conversion_settings = config.get('conversion_settings', {})
    grid_settings = config.get('grid_settings', {})
    processing_settings = config.get('processing_settings', {})
    
    # Find input files
    pattern = config.get('file_pattern', '*.stl')
    stl_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if fnmatch.fnmatch(file.lower(), pattern.lower()):
                stl_files.append(os.path.join(root, file))
    
    print(f"Found {len(stl_files)} files to process")
    
    # Process files
    if grid_settings.get('enabled', False):
        # Grid processing
        results = []
        for stl_path in stl_files:
            output_path = stl_path.replace(input_dir, output_dir).replace('.stl', '.3mf')
            
            success = stl_to_3mf_grid(
                stl_path=stl_path,
                output_path=output_path,
                count=grid_settings.get('count', 4),
                grid_cols=grid_settings.get('grid_cols'),
                spacing_factor=grid_settings.get('spacing_factor', 1.2),
                center_grid=grid_settings.get('center_grid', True)
            )
            
            results.append({'input': stl_path, 'output': output_path, 'success': success})
    else:
        # Standard conversion
        results = batch_convert_stl_to_3mf(
            input_dir=input_dir,
            output_dir=output_dir,
            max_workers=processing_settings.get('max_workers', 4),
            **conversion_settings
        )
    
    return results

# Example config file (batch_config.yaml):
"""
input_directory: "models/stl_files"
output_directory: "models/3mf_files"
file_pattern: "*.stl"

conversion_settings:
  include_metadata: true
  validate: true

grid_settings:
  enabled: true
  count: 4
  grid_cols: 2
  spacing_factor: 1.2
  center_grid: true

processing_settings:
  max_workers: 4
"""

# Usage
results = process_from_config("batch_config.yaml")
```

## Next steps

- **[Grid Layouts](grid-layouts.md)** - Create optimized grid arrangements
- **[3MF Analysis](3mf-analysis.md)** - Analyze your converted files
- **[API Reference](../reference/converters.md)** - Detailed API documentation
