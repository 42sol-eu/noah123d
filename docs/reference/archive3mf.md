## Archive3mf class

You use it in  a with block:

```python
from noah123d import Archive3mf

with Archive3mf('example.3mf') as archive:
    with Directory('models') as directory:
        # Perform operations on the directory
        print(f"Directory contents: {directory.list_contents()}")
        model = archive.read()  
    # Perform operations on the model
    # TODO: improve code   
```


::: noah123d.archive3mf.Archive3mf
    options:
      show_source: true
      show_signature_annotations: true

