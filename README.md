# 🎬 Subtitle Generator (WhisperX)
A fast, GPU-accelerated subtitle generator using **WhisperX** for highly accurate, word-level timestamps and clean `.srt` output.

## ✨ Features
* ⚡ Fast transcription with GPU support (CUDA)
* 🧠 Word-level alignment using WhisperX
* 🧼 Automatic cleanup of bad timestamps
* ⏱️ Improved subtitle readability timing
* 📄 Outputs standard `.srt` subtitle files

## 🧰 Requirements
* Python **3.11.9**
* NVIDIA GPU (recommended for best performance)
* CUDA-compatible environment

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/subtitle-generator.git
cd subtitle-generator
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install PyTorch (CUDA)
⚠️ This step is important for GPU acceleration.

Example for CUDA 12.8:

```bash
pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
```

If you're unsure about your CUDA version, check: https://pytorch.org/get-started/locally/

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage
Run the script with an audio file:

```bash
py main.py audio.wav
```

## 📂 Output
* Generates a `.srt` file in the same directory as your input audio
* Example:

```
audio.wav → audio.srt
```

## ⚙️ How It Works
1. Loads WhisperX model
2. Transcribes audio
3. Aligns words with precise timestamps
4. Cleans invalid segments
5. Adjusts timing for readability
6. Writes subtitles to `.srt`

## 🧠 Notes
* First run may take longer due to model downloads
* GPU (`cuda`) is automatically used if available
* Falls back to CPU if CUDA is not available (slower)

## 🛠️ Troubleshooting

### CUDA not detected
Run:

```python
import torch
print(torch.cuda.is_available())
```

If `False`, reinstall PyTorch with the correct CUDA version.