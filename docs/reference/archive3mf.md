## Archive class

A 3mf (3D Manufacturing Format) file is a ZIP archive, the structure is discussed in this section.


You use it in  a nested with blocks:

```python
from noah123d import *

with Archive('example.3mf') as archive:
    with Directory('3D') as directory:
        # Perform operations on the directory
        print(f"Directory contents: {directory.list_contents()}")
        model = archive.read()  
    # Perform operations on the model
```

## 3MF Archive Structure

A 3MF archive is essentially a ZIP file with a specific directory structure. Here's what a typical 3MF archive looks like:

```
{name}.3mf                          # The main archive 
├── [Content_Types].xml             # Required: MIME type definitions
├── _rels/
│   └── .rels                       # Required: Package relationships
|
├── 3D/                             # 3D models directory
│   ├── 3dmodel.model               # Required: Main 3D model file (XML)
│   └── thumbnail.png               # Optional: Preview thumbnail
|
├── Metadata/                       # Optional: Additional metadata
│   ├── conversion_info.txt         # Custom conversion information
│   └── properties.xml              # Optional: Additional properties
|
└── Textures/                       # Optional: Texture files
    ├── texture1.jpg
    └── texture2.png
```

**Key Components:**

- **`[Content_Types].xml`** - Defines MIME types for all files in the archive
- **`_rels/.rels`** - Defines relationships between files in the package
- **`3D/3dmodel.model`** - The main 3D model data in XML format containing vertices, triangles, and objects
- **`3D/` directory** - Contains all 3D model files and related resources
- **`Metadata/` directory** - Optional directory for custom metadata and properties
- **`Textures/` directory** - Optional directory for texture images and materials (via extensions)

> **Note:** The 3MF specification does not define an "attachments" directory. Custom files should be placed in the `Metadata/` directory or other appropriately named custom directories with proper content types and relationships.


::: noah123d.archive.archive
    options:
      show_source: true
      show_signature_annotations: true

