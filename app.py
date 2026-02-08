import gradio as gr
import os
import sys

# Add web_app to path so we can import model_handler
sys.path.append(os.path.join(os.path.dirname(__file__), 'web_app'))

from model_handler import load_model_safe, predict_image

# Load model on startup
print("Loading AI detection model...")
load_model_safe()
print("Model loaded successfully!")

def classify_image(image_path):
    """
    Gradio callback for image classification
    
    Args:
        image_path: Path to uploaded image file
        
    Returns:
        Formatted prediction string
    """
    if image_path is None:
        return "Please upload an image first."
    
    # Run prediction using existing model_handler
    result = predict_image(image_path)
    
    if 'error' in result:
        return f"❌ ERROR: {result['error']}"
    
    label = result['label']
    confidence = result['confidence']
    
    # Format output with verdict and confidence
    if label == 'REAL':
        verdict = f"✅ REAL ({confidence:.1f}% confidence)"
        explanation = "This image appears to be a genuine photograph."
    else:
        verdict = f"🚫 FAKE ({confidence:.1f}% confidence)"
        explanation = "This image appears to be AI-generated."
    
    return f"{verdict}\n\n{explanation}"

# Create Gradio interface
demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="filepath", label="Upload Image to Analyze"),
    outputs=gr.Textbox(label="Verdict", lines=3),
    title="🕵️ VERITAS - AI Image Forensics",
    description="""
    Detect if an image is **REAL** (photographed) or **FAKE** (AI-generated) using deep learning.
    
    **Model:** CNN trained on 60,000 images from the CIFAKE dataset  
    **Accuracy:** ~93% on validation set  
    **Note:** Best results on 32x32 resolution images similar to training data.
    """,
    examples=[
        [os.path.join("web_app", "test_examples", "real_sample_1.jpg")],
        [os.path.join("web_app", "test_examples", "fake_sample_1.jpg")],
        [os.path.join("web_app", "test_examples", "real_sample_3.jpg")],
        [os.path.join("web_app", "test_examples", "fake_sample_3.jpg")],
    ],
    theme=gr.themes.Monochrome(),
    css="""
    .gradio-container {
        background: linear-gradient(to bottom, #0a0a0a, #1a1a1a);
        color: #00ff00;
    }
    """
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
