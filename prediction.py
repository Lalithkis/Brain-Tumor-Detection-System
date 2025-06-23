import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import ipywidgets as widgets
from IPython.display import display, clear_output
import io

def load_model(model_path):
    """
    Load the pre-trained model from the given path.
    Args:
        model_path (str): Path to the saved model file.
    Returns:
        tf.keras.Model: Loaded model.
    """
    return tf.keras.models.load_model(model_path)

def preprocess_image(image_path, target_size=(150, 150)):
    """
    Preprocess the image for prediction.
    Args:
        image_path (str): Path to the image file.
        target_size (tuple): Target size for resizing the image.
    Returns:
        numpy.ndarray: Preprocessed image array.
    """
    image = Image.open(image_path)
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def predict_image(model, image_array, labels):
    """
    Predict the class of the image using the model.
    Args:
        model (tf.keras.Model): Loaded model.
        image_array (numpy.ndarray): Preprocessed image array.
        labels (list): List of class labels.
    Returns:
        str: Predicted class label.
    """
    predictions = model.predict(image_array)
    predicted_index = np.argmax(predictions, axis=1)[0]
    return labels[predicted_index]

def img_pred(upload):
    """
    Predict the uploaded image using the model.
    Args:
        upload (widgets.FileUpload): Uploaded file widget.
    """
    for file_info in upload.value.values():
        img = Image.open(io.BytesIO(file_info['content']))
        opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img = cv2.resize(opencvImage, (150, 150))
        img = img.reshape(1, 150, 150, 3)
        p = model.predict(img)
        p = np.argmax(p, axis=1)[0]
        if p == 0:
            p = 'Glioma Tumor'
        elif p == 1:
            p = 'No Tumor'
        elif p == 2:
            p = 'Meningioma Tumor'
        else:
            p = 'Pituitary Tumor'

        print(f'The Model predicts that it is a {p}')

if __name__ == "__main__":
    # Define the labels
    labels = ['glioma_tumor', 'no_tumor', 'meningioma_tumor', 'pituitary_tumor']

    # Path to the saved model
    model_path = "effnet.h5"

    # Load the model
    model = load_model(model_path)

    # Load the model weights
    model.load_weights('effnet.h5')

    # Create uploader widget
    uploader = widgets.FileUpload()
    display(uploader)

    # Create predict button
    button = widgets.Button(description='Predict')
    out = widgets.Output()

    def on_button_clicked(_):
        with out:
            clear_output()
            try:
                img_pred(uploader)
            except Exception as e:
                print(f'Error: {e}')

    button.on_click(on_button_clicked)
    display(widgets.VBox([button, out]))