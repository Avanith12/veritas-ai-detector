---
title: VERITAS AI Image Detector
emoji: 🕵️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.11.0
app_file: app.py
pinned: false
---

# VERITAS - AI Image Forensics

Detect if an image is **REAL** (photographed) or **FAKE** (AI-generated) using a Convolutional Neural Network.

## Model Details

- **Architecture:** CNN with 3 convolutional layers
- **Training Data:** 60,000 images from CIFAKE dataset (30K real, 30K AI-generated)
- **Input Resolution:** 32x32 RGB
- **Validation Accuracy:** ~93%

## How It Works

1. Upload an image or select an example
2. The model preprocesses the image (resize to 32x32, normalize)
3. CNN analyzes patterns to detect AI artifacts
4. Returns verdict: REAL or FAKE with confidence score

## Limitations

⚠️ **Important:** This model is trained on low-resolution (32x32) images. High-quality AI art from modern generators (Midjourney v6, DALL-E 3) may be misclassified due to resolution downscaling.

Best results on images similar to the training distribution.

## Try It

Use the example images below or upload your own!

---

**Built by Avanith Kanamarlapudi**
