from pathlib import Path
from noah123d.core import ModelParameters, BaseModel

class BoxModel(BaseModel):
    def build(self) -> None:
        logging.debug("Building BoxModel with parameters: %s", self.params)
        # Placeholder for build123d code
        self.model = f"Box({self.params.width} x {self.params.height} x {self.params.depth})"

params = ModelParameters(name="MyBox", width=10, height=5, depth=3, material="PLA")
box = BoxModel(params)
box.build()
box.export(Path("box_model.stl"))
