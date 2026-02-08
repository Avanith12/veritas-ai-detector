import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image

# Global Model Variable
_model = None
_class_names = ['FAKE', 'REAL'] # Standard alphabetized classes from directory structure

def get_model():
    """Returns the loaded model, loading it if necessary."""
    global _model
    if _model is None:
        load_model_safe()
    return _model

def load_model_safe():
    """Loads the model from the local directory with error handling."""
    global _model
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'ai_detector_model.h5')
        
        if os.path.exists(model_path):
            # compile=False is crucial for avoiding version mismatch errors
            _model = load_model(model_path, compile=False)
            print(f"SUCCESS: Model loaded from {model_path}")
        else:
            print(f"CRITICAL ERROR: Model file not found at {model_path}")
            _model = None
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to load model. Reason: {e}")
        _model = None

def prepare_image(image_path):
    """
    Preprocesses the image for the model.
    - Converts to RGB (removes Alpha channel).
    - Resizes to 32x32 using Bilinear interpolation.
    - Adds batch dimension.
    """
    img = Image.open(image_path).convert('RGB')
    img = img.resize((32, 32), Image.BILINEAR) # Match Keras training resizing
    img_array = np.array(img)
    # Note: No division by 255.0 here because the model has a Rescaling layer
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
    return img_array

def predict_image(image_path):
    """
    Runs inference on the image at the given path.
    Returns a dictionary with 'label', 'confidence', etc.
    """
    model = get_model()
    if model is None:
        return {'error': "Model not loaded. Check server logs."}
    
    try:
        processed_img = prepare_image(image_path)
        
        # Run Prediction
        prediction = model.predict(processed_img)
        score = tf.nn.softmax(prediction[0])
        
        confidence = 100 * np.max(score)
        label = _class_names[np.argmax(score)]
        
        # Save Debug Image (Neural View)
        # We need to save this so the frontend can display it
        # Assuming the caller handles the file save location, we just return the array if needed?
        # Actually, let's just save it here if we know the directory, but let's keep it simple.
        # We'll return the processed array (squeezed) so the app can save the debug image.
        
        return {
            'label': label,
            'confidence': confidence,
            'processed_array': processed_img[0] # For debug visualization
        }
    except Exception as e:
        return {'error': str(e)}
