from abc import ABC, abstractmethod

class ImageModelBase(ABC):
    """
    Abstract base class for all image generation models.
    Implementations must define `generate_image()` method.
    """

    @abstractmethod
    def generate_image(self, prompt: str, output_path: str) -> None:
        """
        Generate an image from a text prompt and save it to output_path.

        Args:
            prompt (str): The text description for the image.
            output_path (str): Where to save the generated image.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        pass
