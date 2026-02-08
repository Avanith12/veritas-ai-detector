import os
import sys
import numpy as np

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

try:
    from model_handler import load_model_safe, predict_image
except ImportError:
    print("Could not import model_handler. Ensure you are in the web_app directory.")
    sys.exit(1)

# Load the model once
print("Loading Model...")
load_model_safe()

examples_dir = os.path.join(os.getcwd(), 'test_examples')
if not os.path.exists(examples_dir):
    print("Test examples directory not found.")
    sys.exit(1)

files = os.listdir(examples_dir)
print(f"Testing {len(files)} files...")

for f in files:
    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(examples_dir, f)
        result = predict_image(path)
        
        if 'error' in result:
            print(f"{f}: ERROR - {result['error']}")
        else:
            # Print raw confidence to see if they are identical
            print(f"{f}: {result['label']} - {result['confidence']:.6f}%")
