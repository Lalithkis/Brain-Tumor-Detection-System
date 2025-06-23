from PIL import Image
import numpy as np

def preprocess_image(image):
    """
    Preprocesses the image for the AI model.
    Args:
        image (PIL.Image): The input image.
    Returns:
        numpy.ndarray: The preprocessed image array.
    """
    # Placeholder: Resize image and convert to numpy array
    img = image.resize((128, 128)) #adjust the size based on your AI model
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension

    return img_array