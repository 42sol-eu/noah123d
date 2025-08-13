
"""Base model class for noah123d models."""

from abc import ABC, abstractmethod # https://docs.python.org/3/library/abc.html
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html

from .constants import *
from .logging import *
from .parameters import ModelParameters


class BaseModel(ABC):
    """Abstract base class for all noah123d models."""

    def __init__(self, params: ModelParameters) -> None:
        logging.debug("Initializing BaseModel with params: %s", params)
        self.params = params
        self.model = None

    @abstractmethod
    def build(self) -> None:
        """
        Build the model using build123d or noah123d operations.
        Must set self.model to the built object.
        """
        logging.debug(f"Building model '{self.params.name}' with {self.params}")
        # Implement model building logic here
        self.model = None
        return self

    def export(self, file_path: Path) -> None:
        """
        Export the model to the given file path.
        This is a placeholder — in practice, hook into build123d exporters.
        """
        logging.debug("Exporting model '%s' to %s", self.params.name, file_path)
        if self.model is None:
            raise ValueError("Model not built. Call build() first.")
        # Example: Replace with actual build123d export code
        file_path.write_text(f"Exported model: {self.params.name}")
        logging.info("Model '%s' exported to %s", self.params.name, file_path)
        return self
