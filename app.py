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
        Formatted prediction string with analysis
    """
    if image_path is None:
        return "ERROR: No image provided", ""
    
    # Run prediction using existing model_handler
    result = predict_image(image_path)
    
    if 'error' in result:
        return f"ERROR: {result['error']}", ""
    
    label = result['label']
    confidence = result['confidence']
    
    # Format verdict
    verdict = f"CLASSIFICATION: {label}"
    
    # Format detailed analysis
    analysis = f"""CONFIDENCE SCORE: {confidence:.1f}%

ASSESSMENT:
{f'Image appears to be a genuine photograph.' if label == 'REAL' else 'Image appears to be AI-generated.'}

MODEL: CNN trained on CIFAKE dataset
RESOLUTION: 32x32 (optimal for this model)
TRAINING DATA: 60,000 images (50% real, 50% AI-generated)"""
    
    return verdict, analysis

# Custom CSS for cyberpunk terminal aesthetic
custom_css = """
/* Global dark theme */
.gradio-container {
    background: #0a0a0a !important;
    font-family: 'Courier New', monospace !important;
}

/* Title styling */
.gradio-container h1 {
    color: #00ff00 !important;
    text-align: center;
    font-weight: bold;
    letter-spacing: 0.15em;
    text-shadow: 0 0 10px #00ff00;
    margin-bottom: 10px;
}

/* Description text */
.gradio-container .prose {
    color: #00ff00 !important;
    font-family: 'Courier New', monospace !important;
}

/* Input/Output boxes */
.gradio-container .block {
    background: #1a1a1a !important;
    border: 1px solid #00ff00 !important;
    border-radius: 0 !important;
}

/* Labels */
.gradio-container label {
    color: #00ff00 !important;
    font-weight: bold !important;
    text-transform: uppercase;
}

/* Textboxes */
.gradio-container textarea, .gradio-container input {
    background: #0a0a0a !important;
    color: #00ff00 !important;
    border: 1px solid #00ff00 !important;
    font-family: 'Courier New', monospace !important;
}

/* Buttons */
.gradio-container button {
    background: #1a1a1a !important;
    color: #00ff00 !important;
    border: 1px solid #00ff00 !important;
    border-radius: 0 !important;
    font-family: 'Courier New', monospace !important;
    text-transform: uppercase;
}

.gradio-container button:hover {
    background: #00ff00 !important;
    color: #0a0a0a !important;
}

/* Examples section */
.gradio-container .example {
    border: 1px solid #00ff00 !important;
}
"""

# Create Gradio interface with blocks for more control
with gr.Blocks(css=custom_css, theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# VERITAS - AI IMAGE FORENSICS")
    gr.Markdown("""
    **SYSTEM STATUS:** ONLINE | **MODEL:** CNN | **DATASET:** CIFAKE | **ACCURACY:** 93%
    
    MISSION: Detect if an image is REAL (photographed) or FAKE (AI-generated) using deep learning.
    
    **LIMITATIONS:** Model trained on 32x32 resolution. Best results on images similar to training distribution.
    """)
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath", label="UPLOAD TARGET IMAGE")
            submit_btn = gr.Button("ANALYZE", variant="primary")
            
        with gr.Column():
            verdict_output = gr.Textbox(label="VERDICT", lines=1, interactive=False)
            analysis_output = gr.Textbox(label="DETAILED ANALYSIS", lines=8, interactive=False)
    
    gr.Markdown("### EVIDENCE LOCKER - TEST SAMPLES")
    
    # Updated Examples for Gradio 5.x compatibility
    examples = gr.Examples(
        examples=[
            [os.path.join("web_app", "test_examples", "real_sample_1.jpg")],
            [os.path.join("web_app", "test_examples", "fake_sample_1.jpg")],
            [os.path.join("web_app", "test_examples", "real_sample_3.jpg")],
            [os.path.join("web_app", "test_examples", "fake_sample_3.jpg")],
        ],
        inputs=image_input,
        outputs=[verdict_output, analysis_output],
        fn=classify_image,
        cache_examples=False,
    )
    
    gr.Markdown("""
    ---
    **AUTHOR:** Avanith Kanamarlapudi | **FRAMEWORK:** Gradio | **DEPLOYMENT:** Hugging Face Spaces
    """)
    
    # Event handlers
    submit_btn.click(
        fn=classify_image,
        inputs=image_input,
        outputs=[verdict_output, analysis_output]
    )
    
    image_input.change(
        fn=classify_image,
        inputs=image_input,
        outputs=[verdict_output, analysis_output]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )

