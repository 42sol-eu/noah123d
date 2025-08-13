""" Example: Demonstrating the Model class methods for STL conversion. """

from noah123d import Archive, Directory, Model


with Archive('output.3mf', 'w') as archive:
    with Directory('3D') as models_dir:
        model = Model.create_simple_cube(size=42.0)
        model.analyze_model_content()
        model.add_conversion_metadata('model.stl')