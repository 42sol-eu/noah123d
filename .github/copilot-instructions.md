For Python code, a library import should look like this : `from {module} import (\n    {elements} )\n#!md| [docs]({url_to_the_docs})`.
For Python code, dataclasses should align their field name, type and value in a column style.
For Python code, a files doc string must be present and must look like this: 
```python
# -*- coding: utf-8 -*-
"""
Simple constants for build123d projects.
----
file:
    name:       {file name}.py  
    uuid:       {file specific UUIDs}
description:    Simple constants for build123d projects
authors:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""
```
In Python, a class must be implemented in its own file 
In Python, the following headings should be present if the file has the section:
- `# %% [Main]` if a `if __name__ == "__main__":` block is present
- `# %% [External imports]` if the file has external import statements
- `# %% [Local imports]` if the file has local import statements
- `# %% [Constants]` if the file contains any constants
- `# %% [Functions]` if the file contains any functions
- `# %% [Classes]` if the file contains any classes
