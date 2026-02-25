import setuptools # Must be first to support Python 3.12+ distutils
import gradio as gr
import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image

# Setup paths
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(base_dir, 'web_app'))

# Load Models Global Variables
model_v1 = None
model_v2 = None
model_v2_status = "Not Initialized"

# Keras 2/3 Compatibility Hack
class FixedSCC(tf.keras.losses.SparseCategoricalCrossentropy):
    def __init__(self, *args, **kwargs):
        kwargs.pop('fn', None)
        super().__init__(*args, **kwargs)

def load_models():
    global model_v1, model_v2, model_v2_status
    custom_objs = {'SparseCategoricalCrossentropy': FixedSCC}
    try:
        print("Loading V1 Model...")
        model_v1 = tf.keras.models.load_model(
            os.path.join(base_dir, 'web_app', 'ai_detector_model.h5'), 
            compile=False, 
            custom_objects=custom_objs
        )
        print("V1 Loaded.")
        
        v2_path = os.path.join(base_dir, 'web_app', 'ai_detector_v2.h5')
        if os.path.exists(v2_path):
            print("Loading V2 Model...")
            try:
                model_v2 = tf.keras.models.load_model(
                    v2_path, 
                    compile=False, 
                    custom_objects=custom_objs
                )
                model_v2_status = "Loaded Successfully"
                print("V2 Loaded.")
            except Exception as e_load:
                model_v2_status = f"Load Failed: {str(e_load)}"
                print(f"V2 Load Error: {e_load}")
        else:
            model_v2_status = f"File Not Found at {v2_path}"
            print(f"V2 Model not found at {v2_path}")
    except Exception as e:
        model_v2_status = f"System Error: {str(e)}"
        print(f"Error loading models: {e}")

# Load on startup
load_models()

def predict(image, model_choice):
    if image is None:
        return "ERROR: No image provided", ""
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
            
        if "V1" in model_choice:
            # V1 Logic (32x32, Simple CNN)
            target_size = (32, 32)
            img = image.resize(target_size)
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0) # Create batch axis
            
            # Predict
            predictions = model_v1.predict(img_array, verbose=0)
            score = tf.nn.softmax(predictions[0])
            confidence = 100 * np.max(score)
            
            # Label logic: 0=AI, 1=REAL
            class_idx = np.argmax(score)
            if class_idx == 0:
                label = "AI-GENERATED"
            else:
                label = "REAL"
                
            details = f"""MODEL: V1 (Custom CNN)
RESOLUTION: 32x32 pixels
CONFIDENCE: {confidence:.2f}%
trained on CIFAKE (60k images)"""

        else:
            # V2 Logic (224x224, EfficientNet)
            if model_v2 is None:
                return "ERROR", f"V2 STATUS: {model_v2_status}"
                
            target_size = (224, 224)
            img = image.resize(target_size)
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            
            logits = model_v2.predict(img_array, verbose=0)
            probability = tf.nn.sigmoid(logits[0][0])
            
            # Binary classification: 0=AI, 1=Real
            if probability < 0.5:
                label = "AI-GENERATED"
                confidence = 100 * (1 - probability)
            else:
                label = "REAL" 
                confidence = 100 * probability
                
            details = f"""MODEL: V2 (EfficientNetB0)
RESOLUTION: 224x224 pixels
CONFIDENCE: {confidence:.2f}%
trained on High-Res Dataset"""

        return label, details

    except Exception as e:
        return "ERROR", str(e)


# Custom CSS
custom_css = """
.gradio-container { background: #0a0a0a !important; font-family: 'Courier New', monospace !important; }
h1 { color: #00ff00 !important; text-align: center; text-shadow: 0 0 10px #00ff00; }
.prose { color: #00ff00 !important; }
.block { background: #1a1a1a !important; border: 1px solid #00ff00 !important; }
label { color: #00ff00 !important; font-weight: bold !important; }
textarea, input { background: #0a0a0a !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
button { background: #1a1a1a !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
button:hover { background: #00ff00 !important; color: #0a0a0a !important; }
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# VERITAS - AI IMAGE FORENSICS")
    gr.Markdown("""
    **SYSTEM ONLINE** | DETECT REAL vs AI IMAGES
    Select a model version below to load specific examples.
    """)
    
    with gr.Row():
        with gr.Column():
            model_selector = gr.Radio(
                ["V1 (Fast/Low-Res)", "V2 (Accurate/High-Res)"], 
                label="SELECT MODEL VERSION", 
                value="V2 (Accurate/High-Res)"
            )
            image_input = gr.Image(type="numpy", label="UPLOAD TARGET IMAGE")
            submit_btn = gr.Button("ANALYZE", variant="primary")
            
        with gr.Column():
            verdict_output = gr.Textbox(label="VERDICT", lines=1)
            analysis_output = gr.Textbox(label="DETAILED ANALYSIS", lines=6)
            
    gr.Markdown("### EVIDENCE LOCKER - EXAMPLES")
    
    # V1 Examples (Visible only when V1 selected)
    with gr.Group(visible=False) as v1_examples_group:
        gr.Markdown("**V1 Test Samples (32x32 Optimized) - click to load**")
        gr.Examples(
            examples=[
                [os.path.join("web_app", "test_examples", "real_sample_1.jpg")],
                [os.path.join("web_app", "test_examples", "fake_sample_1.jpg")],
                [os.path.join("web_app", "test_examples", "real_sample_2.jpg")],
                [os.path.join("web_app", "test_examples", "fake_sample_2.jpg")],
                [os.path.join("web_app", "test_examples", "fake_sample_3.jpg")],
            ],
            inputs=image_input,  # Only update image input, NOT model_selector to avoid table clutter
            outputs=[verdict_output, analysis_output],
            fn=lambda x: predict(x, "V1 (Fast/Low-Res)"), # Force V1 context for V1 examples
            cache_examples=False,
        )

    # V2 Examples (Visible only when V2 selected - Default)
    with gr.Group(visible=True) as v2_examples_group:
        gr.Markdown("**V2 Test Samples (High-Res Optimized) - click to load**")
        gr.Examples(
            examples=[
                # Use actual available files from directory
                [os.path.join("web_app", "test_examples_v2", "100960167.jpg")], 
                [os.path.join("web_app", "test_examples_v2", "1032249.jpg")],
                [os.path.join("web_app", "test_examples_v2", "120522_Lensa_AI.width-696.jpg")],
                [os.path.join("web_app", "test_examples_v2", "190430171751-mona-lisa.jpg")],
                [os.path.join("web_app", "test_examples_v2", "AI-Tracking-Cat.jpg")],
            ],
            inputs=image_input, # Only update image input
            outputs=[verdict_output, analysis_output],
            fn=lambda x: predict(x, "V2 (Accurate/High-Res)"), # Force V2 context for V2 examples
            cache_examples=False,
        )

    # Dynamic Visibility Logic
    def toggle_examples(choice):
        if "V1" in choice:
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)

    model_selector.change(
        fn=toggle_examples,
        inputs=model_selector,
        outputs=[v1_examples_group, v2_examples_group]
    )

    submit_btn.click(predict, inputs=[image_input, model_selector], outputs=[verdict_output, analysis_output])
    image_input.change(predict, inputs=[image_input, model_selector], outputs=[verdict_output, analysis_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
