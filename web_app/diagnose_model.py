import os
import sys
import traceback

# Redirect stderr to a file so we capture everything
sys.stderr = open('error_log.txt', 'w')
sys.stdout = open('output_log.txt', 'w')

try:
    print("Starting diagnostics...")
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'ai_detector_model.h5')
    
    print(f"Diagnostics Script Running in: {os.getcwd()}")
    print(f"Base Directory: {BASE_DIR}")
    print(f"Target Model Path: {MODEL_PATH}")
    
    if os.path.exists(MODEL_PATH):
        print(f"File exists! Size: {os.path.getsize(MODEL_PATH)} bytes")
        try:
            # TRYING FIX: compile=False to define inference-only model
            print("Attempting with compile=False...")
            model = load_model(MODEL_PATH, compile=False)
            print("SUCCESS: Model loaded correctly (Inference Mode)!")
        except Exception as e:
            print(f"FAILURE: Model file exists but failed to load.")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            traceback.print_exc()
    else:
        print(f"FAILURE: File NOT found at {MODEL_PATH}")
        print(f"Contents of {BASE_DIR}:")
        for f in os.listdir(BASE_DIR):
            print(f" - {f}")

except Exception as e:
    print(f"CRITICAL SCRIPT FAILURE: {str(e)}")
    traceback.print_exc()
finally:
    sys.stderr.close()
    sys.stdout.close()
