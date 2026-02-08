import os
import shutil
import random
import kagglehub
import pathlib
from PIL import Image

def get_examples():
    print("Finding dataset...")
    # This should return the cached path instantly
    path = kagglehub.dataset_download("birdy654/cifake-real-and-ai-generated-synthetic-images")
    data_dir = pathlib.Path(path) / 'test' # Use test set for unseen examples
    
    output_dir = os.path.join(os.getcwd(), 'test_examples')
    os.makedirs(output_dir, exist_ok=True)
    
    # Get 5 Real images
    real_dir = data_dir / 'REAL'
    real_files = list(real_dir.glob('*.jpg'))
    selected_real = random.sample(real_files, 5)
    
    print(f"Copying {len(selected_real)} REAL images...")
    for i, file in enumerate(selected_real):
        dest = os.path.join(output_dir, f'real_sample_{i+1}.jpg')
        shutil.copy(file, dest)
        
    # Get 5 Fake images
    fake_dir = data_dir / 'FAKE'
    fake_files = list(fake_dir.glob('*.jpg'))
    selected_fake = random.sample(fake_files, 5)
    
    print(f"Copying {len(selected_fake)} FAKE images...")
    for i, file in enumerate(selected_fake):
        dest = os.path.join(output_dir, f'fake_sample_{i+1}.jpg')
        shutil.copy(file, dest)
        
    print(f"Done! Check the folder: {output_dir}")

if __name__ == "__main__":
    get_examples()
