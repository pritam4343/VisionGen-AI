# VisionGen AI — Low-Memory Text-to-Image Studio

A portfolio-ready text-to-image app built with Python, Streamlit, Hugging Face Diffusers and Stable Diffusion 1.5. It includes prompt styling controls, negative prompts, resolution choices, seed reproducibility, saved image history and PNG downloads.

## Hardware note (important)

Designed to attempt CPU inference on an 8 GB RAM laptop using 512px images, one image per run, attention slicing and VAE slicing. CPU image generation may be very slow and can still run out of memory depending on the operating system and background applications. A dedicated GPU is not assumed. If generation is unstable, use a hosted GPU notebook (for example, a free/paid notebook service) rather than expecting fast local inference.

The app intentionally does not load a separate LLM locally because keeping an LLM and a diffusion model in memory together is not a good fit for 8 GB RAM. Prompt enhancement is lightweight and rule-based. This can be extended later with an optional remote open-source LLM endpoint.

## Features

- Text-to-image generation using an open model
- Prompt enhancement controls for style, lighting and composition
- Negative prompts
- 512x512, 512x384 and 384x512 output sizes
- Adjustable inference steps and guidance
- Fixed or random seed
- Saved generation history and PNG download
- CPU memory-saving settings

## Setup (Windows PowerShell)

1. Install Python 3.10 or 3.11 (64-bit).
2. Extract this project folder.
3. Open PowerShell inside the folder.
4. Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Run the application:

```powershell
streamlit run app.py
```

The first run downloads the model weights from Hugging Face. A stable internet connection and free disk space are required. Later runs use the local model cache.

## Setup (Linux/macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Recommended settings for an 8 GB RAM laptop

- Resolution: 512 × 512
- Inference steps: start at 5–8; increase to 12–20 only if stable
- Generate one image at a time
- Close browsers and other memory-heavy apps
- Keep 10–15 GB free disk space for model cache and outputs
- If possible, use a machine with a compatible GPU for much faster inference

## Troubleshooting

- **Out of memory:** close applications, reboot, use the smallest resolution and 5 steps, and check that the OS has a page file/swap enabled.
- **Slow generation:** CPU diffusion is compute-intensive; this is expected without a GPU.
- **Model download issue:** retry with a stable internet connection. Some model repositories may require accepting their model terms.
- **PyTorch installation issue:** install the correct PyTorch build for your operating system from the official PyTorch installation selector, then install the remaining packages.

## Project structure

```text
VisionGen-AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/          # generated PNGs (created automatically)
```

## Portfolio extensions

For a stronger AI Engineer portfolio, consider adding:
- Optional prompt rewriting using a small open LLM through a remote endpoint
- Image-to-image generation or inpainting
- A small evaluation set comparing prompts/seeds and human-rated prompt adherence
- Automated tests for prompt handling, settings and image-saving utilities
- Docker support and a deployment guide

## Model and license

The application uses `stable-diffusion-v1-5/stable-diffusion-v1-5` from Hugging Face Diffusers. Review the model card and license before commercial use or redistribution. Open weights do not automatically mean unrestricted commercial use.

## Disclaimer

This is a starter portfolio implementation. Image quality is probabilistic and not guaranteed to be perfect; hands, text, fine geometry and complex compositions can be imperfect.
