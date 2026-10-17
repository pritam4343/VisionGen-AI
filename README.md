# VisionGen AI — Text-to-Image Studio

VisionGen AI is a text-to-image generation application built using Python, Streamlit, Hugging Face Diffusers, and Stable Diffusion 1.5. It transforms text prompts into visual content through an interactive interface with customizable generation settings, prompt enhancement, and image management features.

## Features

- **AI Text-to-Image Generation:** Generate images from natural-language descriptions using Stable Diffusion 1.5.
- **Prompt Enhancement:** Refine prompts using configurable visual styles, lighting, and composition.
- **Negative Prompts:** Specify unwanted visual elements to guide image generation.
- **Flexible Image Resolution:** Choose from square, landscape, and portrait formats.
- **Generation Controls:** Adjust inference steps and prompt guidance to customize results.
- **Seed Reproducibility:** Use fixed seeds to reproduce generation results or random seeds to explore variations.
- **Image Gallery:** Browse recently generated images through the integrated generation history.
- **PNG Downloads:** Save generated images for further use.
- **Organized Output Management:** Automatically save generated images in the project’s `outputs/` directory.
- **Interactive Interface:** Access generation controls, prompt previews, image results, and generation details through Streamlit.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and image-generation workflow |
| Streamlit | Interactive web interface |
| Hugging Face Diffusers | Diffusion pipeline and image-generation operations |
| Stable Diffusion 1.5 | Text-to-image generation model |
| PyTorch | Model execution and tensor operations |
| Pillow (PIL) | Image processing and PNG export |

## Prerequisites

- Python 3.10 or 3.11 (64-bit recommended)
- Git
- Internet connection for downloading model weights and dependencies
- Sufficient storage and system resources for the model and generated images

## Installation and Setup

### Windows

1. Clone the repository:

```bash
git clone https://github.com/pritam4343/VisionGen-AI.git
cd VisionGen-AI
```

2. Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Launch the application:

```bash
streamlit run app.py
```

### Linux and macOS

1. Clone the repository:

```bash
git clone https://github.com/pritam4343/VisionGen-AI.git
cd VisionGen-AI
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies and start the application:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

On the first launch, the application downloads the required model files from Hugging Face. Download time depends on the internet connection and model availability.

## How to Use

1. Launch VisionGen AI in your browser.
2. Enter a descriptive prompt specifying the subject, environment, visual style, and mood.
3. Optionally provide a negative prompt to describe unwanted elements.
4. Configure visual style, lighting, composition, resolution, inference steps, and prompt guidance.
5. Select a random or fixed seed.
6. Click **Generate Image**.
7. Preview the generated result and review the generation details.
8. Download the image as a PNG or revisit previous generations in the gallery.

## Project Structure

```text
VisionGen-AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/
    └── Generated PNG images
```

The `outputs/` directory is created automatically when the application starts.

## Potential Future Enhancements

- Optional LLM-based prompt rewriting
- Image-to-image generation
- Image inpainting and editing
- User accounts and personalized generation history
- Batch generation and image variations
- Automated testing for prompt processing and image-saving utilities
- Docker-based deployment
- Cloud deployment and API integration
- Image-quality evaluation and prompt-adherence testing

## Model and Licensing

VisionGen AI uses the `stable-diffusion-v1-5/stable-diffusion-v1-5` model through Hugging Face Diffusers.

Review the model card and applicable license before commercial use, redistribution, or deployment. Model usage and distribution are subject to the relevant license terms.

## Disclaimer

VisionGen AI is a portfolio project demonstrating text-to-image generation and interactive AI application development. Generated outputs may vary depending on prompts, model behavior, generation settings, and random seeds.
