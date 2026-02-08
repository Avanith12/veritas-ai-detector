# VERITAS - AI Image Forensics Terminal

**A cyberpunk-themed deep learning application for detecting AI-generated images.**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## What is VERITAS?

VERITAS (Latin for "Truth") is a forensic command-center style web application that uses a Convolutional Neural Network (CNN) to analyze images and determine if they are **REAL** (photographed) or **FAKE** (AI-generated).

### Key Features

- **Neural Network Detection**: Trained on 60,000+ images from the CIFAKE dataset
- **Forensic UI**: Cyberpunk "terminal" aesthetic with scan animations and sound effects
- **Evidence Locker**: Built-in test samples to verify system accuracy
- **Neural View Debugger**: See exactly what the AI sees (32x32 preprocessed input)
- **Mission Briefing**: Clear explanation of system capabilities and limitations
- **Clean Architecture**: Separated "Brain" (AI logic) and "Face" (Web UI) for easy upgrades

---

## Important Limitations

> **WARNING - DATASET CONSTRAINT**: This model is trained on **32x32 pixel images** from the CIFAKE dataset. High-resolution AI art (e.g., Midjourney v6, DALL-E 3) may yield false positives due to downscaling loss. For best results, test with the provided samples in the **Evidence Locker**.

---

## Project Structure

```
AI_Real_vs_Fake_Detector/
├── training/
│   ├── train_model.ipynb       # Jupyter notebook for model training
│   ├── ai_detector_model.h5    # Trained model (generated after training)
│   └── requirements.txt        # Training dependencies
├── web_app/
│   ├── app.py                  # Flask web server ("The Face")
│   ├── model_handler.py        # AI logic module ("The Brain")
│   ├── static/
│   │   ├── style.css           # Cyberpunk terminal styling
│   │   ├── script.js           # Frontend interactions
│   │   └── uploads/            # User-uploaded images (auto-created)
│   ├── templates/
│   │   └── index.html          # Main UI
│   └── test_examples/          # 10 verified test images (5 Real, 5 Fake)
├── Procfile                    # Render.com deployment config
├── requirements.txt            # Production dependencies
├── .gitignore                  # Git exclusions
└── README.md                   # This file
```

---

## Local Setup

### Prerequisites

- Python 3.8+
- pip
- (Optional) Conda for environment management

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/veritas-ai-detector.git
cd veritas-ai-detector
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
cd web_app
python app.py
```

Open your browser to: **http://127.0.0.1:5000**

---

## Testing the System

1. **Navigate to the Evidence Locker** (left sidebar)
2. **Drag a sample image** onto the "Initiate Scan" area
3. **Verify the result** matches the label (REAL or FAKE)

**Expected behavior:**
- `real_sample_1.jpg` → **REAL** (~100%)
- `fake_sample_1.jpg` → **FAKE** (~100%)

---

## Training Your Own Model (Optional)

If you want to retrain the model:

1. Navigate to `training/`
2. Install training dependencies:
   ```bash
   pip install -r training/requirements.txt
   ```
3. Open `train_model.ipynb` in Jupyter Notebook or VS Code
4. Run all cells (the dataset will auto-download via `kagglehub`)
5. Copy the generated `ai_detector_model.h5` to `web_app/`

---

## Deploying to Render.com

### Why Render?

- **Free Tier Available** (750 hours/month)
- **Automatic HTTPS** (Secure by default)
- **GitHub Integration** (Auto-deploy on push)
- **No Credit Card Required** (for free tier)

### Deployment Steps

#### 1. Prepare Your Repository

```bash
# Ensure you have these files in the root:
# - Procfile
# - requirements.txt
# - .gitignore

# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

#### 3. Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository (`veritas-ai-detector`)
3. Configure:
   - **Name**: `veritas-ai-detector` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT web_app.app:app --chdir web_app`
   - **Plan**: `Free`

4. Click **"Create Web Service"**

#### 4. Wait for Deployment

- Initial build takes ~5-10 minutes
- Watch the logs for "Model loaded successfully!"
- Once live, you'll get a URL like: `https://veritas-ai-detector.onrender.com`

#### 5. Test Your Live Site

Visit your Render URL and verify the Evidence Locker samples work correctly.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask (Python) |
| **AI Framework** | TensorFlow / Keras |
| **Frontend** | Vanilla JavaScript, CSS3 |
| **Dataset** | [CIFAKE](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images) (via Kaggle Hub) |
| **Deployment** | Render.com (Gunicorn WSGI) |

---

## How It Works

1. **User uploads an image** via drag-and-drop
2. **Image is preprocessed**:
   - Converted to RGB (removes alpha channel)
   - Resized to 32x32 pixels (bilinear interpolation)
3. **Model runs inference**:
   - Passes through 3 convolutional layers
   - Outputs probability distribution: `[P(FAKE), P(REAL)]`
4. **Result displayed**:
   - Label: Highest probability class
   - Confidence: Percentage value
   - Neural View: 32x32 preprocessed image

---

## Model Performance

| Metric | Value |
|--------|-------|
| **Training Accuracy** | ~95% |
| **Validation Accuracy** | ~93% |
| **Dataset Size** | 60,000 images (30K Real, 30K Fake) |
| **Input Size** | 32x32 RGB |
| **Model Size** | ~1.9 MB |

---

## Known Issues

- **High-res AI art may be misclassified**: The 32x32 downscaling loses fine details that newer AI generators produce
- **Flask `before_first_request` deprecated**: Updated to direct call in code
- **Model confidence often 99%+**: Expected behavior on training-distribution samples

---

## License

MIT License - Feel free to use, modify, and distribute.

---

## Contributing

Contributions welcome! To improve the model:

1. Train on higher resolution (e.g., 256x256)
2. Use transfer learning (ResNet, EfficientNet)
3. Add data augmentation
4. Test on newer generators (DALL-E 3, Midjourney v6)

---

## Links

- **Live Demo**: [Coming Soon]
- **Dataset**: [CIFAKE on Kaggle](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images)
- **Report Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/veritas-ai-detector/issues)

---

**Built by Avanith Kanamarlapudi**
