import kagglehub
import pathlib
import os

print("Checking dataset...")
try:
    path = kagglehub.dataset_download("cashbowman/ai-generated-images-vs-real-images")
    data_dir = pathlib.Path(path)
    print(f"Dataset Path: {data_dir}")

    if not data_dir.exists():
        print("Error: Directory does not exist.")
    else:
        print("Contents of root:")
        for item in data_dir.iterdir():
            print(f" - {item.name} ({'DIR' if item.is_dir() else 'FILE'})")
            if item.is_dir():
                count = len(list(item.glob('*')))
                print(f"   -> Contains {count} files")

except Exception as e:
    print(f"Error: {e}")
