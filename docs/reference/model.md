## Model class

The `Model` class represents a 3D model structure within the 3MF file format. It encapsulates the various components and metadata associated with the model, including parts, assemblies, and their relationships.

### Attributes

TODO: review model attributes
- `id`: A unique identifier for the model.
- `name`: The name of the model.
- `parts`: A list of parts that make up the model.
- `assemblies`: A list of assemblies that define the structure of the model.

### Methods

TODO: review model methods
- `add_part(part)`: Adds a new part to the model.
- `remove_part(part)`: Removes a part from the model.
- `get_part(part_id)`: Retrieves a part by its ID.
- `add_assembly(assembly)`: Adds a new assembly to the model.
- `remove_assembly(assembly)`: Removes an assembly from the model.
- `get_assembly(assembly_id)`: Retrieves an assembly by its ID.
