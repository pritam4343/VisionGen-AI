import os
import time
from pathlib import Path

import streamlit as st
import torch
from PIL import Image
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

APP_DIR = Path(__file__).parent
OUTPUT_DIR = APP_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="VisionGen AI",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.4rem;
    max-width: 1400px;
}
.hero {
    padding: 1.2rem 1.5rem;
    border-radius: 16px;
    background: linear-gradient(120deg, #101827, #28205a);
    color: white;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_pipeline():
    """Load Stable Diffusion with optional memory optimizations."""

    model_id = os.getenv(
        "VISIONGEN_MODEL_ID",
        "stable-diffusion-v1-5/stable-diffusion-v1-5"
    )

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        dtype=torch.float32,
        use_safetensors=True,
        low_cpu_mem_usage=True,
    )

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config
    )

    # Enable optimizations only when supported.
    if hasattr(pipe, "enable_attention_slicing"):
        pipe.enable_attention_slicing("max")

    if hasattr(pipe, "enable_vae_slicing"):
        pipe.enable_vae_slicing()

    if hasattr(pipe, "enable_vae_tiling"):
        pipe.enable_vae_tiling()

    # The app is configured for CPU inference.
    pipe = pipe.to("cpu")

    return pipe


def enhance_prompt(prompt, style, lighting, composition):
    """Enhance prompts without loading an additional LLM."""

    additions = []

    if style != "None":
        additions.append(style)

    if lighting != "Default":
        additions.append(f"{lighting} lighting")

    if composition != "Default":
        additions.append(f"{composition} composition")

    additions.extend([
        "coherent details",
        "well-composed image"
    ])

    if additions:
        return f"{prompt.strip()}, " + ", ".join(additions)

    return prompt.strip()


def save_image(image):
    """Save a generated image using a unique filename."""

    stamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"visiongen-{stamp}-{time.time_ns() % 1000000}.png"
    path = OUTPUT_DIR / filename

    image.save(path, format="PNG")
    return path


st.markdown("""
<div class="hero">
    <h1>🎨 VisionGen AI</h1>
</div>
""", unsafe_allow_html=True)


# Sidebar settings
with st.sidebar:
    st.header("Generation Settings")

    st.caption("")

    style = st.selectbox(
        "Visual Style",
        [
            "None",
            "photorealistic",
            "cinematic concept art",
            "digital illustration",
            "watercolour painting",
            "3D render",
            "editorial photography"
        ]
    )

    lighting = st.selectbox(
        "Lighting",
        [
            "Default",
            "soft natural",
            "golden hour",
            "dramatic studio",
            "neon",
            "diffused"
        ]
    )

    composition = st.selectbox(
        "Composition",
        [
            "Default",
            "wide-angle",
            "close-up",
            "rule-of-thirds",
            "symmetrical"
        ]
    )

    size = st.selectbox(
        "Image Resolution",
        [
            "512 × 512 (recommended)",
            "512 × 384 (landscape)",
            "384 × 512 (portrait)"
        ]
    )

    steps = st.slider(
        "Inference Steps",
        min_value=5,
        max_value=20,
        value=8,
        help="Fewer steps reduce generation time."
    )

    guidance = st.slider(
        "Prompt Guidance",
        min_value=4.0,
        max_value=9.0,
        value=7.0,
        step=0.5
    )

    seed_mode = st.radio(
        "Seed",
        ["Random", "Fixed"],
        horizontal=True
    )

    seed = st.number_input(
        "Fixed Seed",
        min_value=0,
        max_value=2_147_483_647,
        value=42,
        disabled=(seed_mode == "Random")
    )

    generate = st.button(
        "✨ Generate Image",
        type="primary",
        width="stretch"
    )


left, right = st.columns([1, 1.4], gap="large")


# Prompt input
with left:
    st.subheader("Describe Your Image")

    prompt = st.text_area(
        "Prompt",
        value=(
            "A cosy modern cabin beside a mountain lake at dusk, "
            "warm lights glowing through the windows, "
            "detailed natural environment"
        ),
        height=160,
        max_chars=700,
        placeholder="Describe the subject, setting, lighting and mood..."
    )

    negative_prompt = st.text_area(
        "Negative Prompt (Optional)",
        value=(
            "blurry, low quality, distorted, extra limbs, "
            "malformed hands, text, watermark, logo"
        ),
        height=90,
        max_chars=400
    )

    st.info(
        "Tip: describe the subject, environment, visual style, "
        "lighting and composition for more controllable results."
    )

    if prompt.strip():
        with st.expander("Preview Enhanced Prompt"):
            st.write(
                enhance_prompt(
                    prompt,
                    style,
                    lighting,
                    composition
                )
            )


# Image generation
with right:
    st.subheader("Generated Image")

    if generate:
        if not prompt.strip():
            st.error("Please enter a prompt before generating.")

        else:
            width, height = {
                "512 × 512 (recommended)": (512, 512),
                "512 × 384 (landscape)": (512, 384),
                "384 × 512 (portrait)": (384, 512),
            }[size]

            final_prompt = enhance_prompt(
                prompt,
                style,
                lighting,
                composition
            )

            if seed_mode == "Fixed":
                chosen_seed = int(seed)
            else:
                chosen_seed = int(
                    torch.randint(
                        0,
                        2_147_483_647,
                        (1,)
                    ).item()
                )

            try:
                if not torch.cuda.is_available():
                    st.warning(
                        ""
                        ""
                    )

                with st.spinner(
                    "Loading model and generating image. "
                    "The first run downloads the model..."
                ):
                    pipe = load_pipeline()

                    generator = torch.Generator(
                        device="cpu"
                    ).manual_seed(chosen_seed)

                    start = time.perf_counter()

                    result = pipe(
                        prompt=final_prompt,
                        negative_prompt=(
                            negative_prompt.strip() or None
                        ),
                        width=width,
                        height=height,
                        num_inference_steps=int(steps),
                        guidance_scale=float(guidance),
                        generator=generator,
                    )

                    image = result.images[0]
                    elapsed = time.perf_counter() - start
                    path = save_image(image)

                    st.session_state["last_image"] = image
                    st.session_state["last_path"] = str(path)
                    st.session_state["last_prompt"] = final_prompt
                    st.session_state["last_seed"] = chosen_seed
                    st.session_state["last_elapsed"] = elapsed

            except Exception as exc:
                st.error(f"Image generation failed: {exc}")

                st.info(
                    "Try 512 × 512 resolution and 5 inference steps. "
                    "Check your internet connection, model download, "
                    "installed packages and available RAM."
                )

    # Display the latest generated image
    if "last_image" in st.session_state:
        st.image(
            st.session_state["last_image"],
            width="stretch"
        )

        st.caption(
            f"Seed: {st.session_state['last_seed']} | "
            f"Generation time: "
            f"{st.session_state['last_elapsed']:.1f} seconds"
        )

        image_path = st.session_state["last_path"]

        with open(image_path, "rb") as file:
            st.download_button(
                "⬇️ Download PNG",
                data=file.read(),
                file_name=Path(image_path).name,
                mime="image/png",
                width="stretch"
            )

        with st.expander("Generation Details"):
            st.write(
                "**Prompt used:**",
                st.session_state["last_prompt"]
            )
            st.write("**Saved to:**", image_path)

    else:
        st.markdown("""
        <div style="
            border: 1px dashed #777;
            border-radius: 14px;
            padding: 4rem 1rem;
            text-align: center;
        ">
            <h3>Your image will appear here</h3>
            <p>Enter a prompt and click Generate Image.</p>
        </div>
        """, unsafe_allow_html=True)


# Recent generations
st.divider()
st.subheader("Recent Generations")

images = sorted(
    OUTPUT_DIR.glob("*.png"),
    key=lambda path: path.stat().st_mtime,
    reverse=True
)[:8]

if images:
    cols = st.columns(4)

    for idx, image_path in enumerate(images):
        with cols[idx % 4]:
            st.image(
                Image.open(image_path),
                width="stretch"
            )
            st.caption(image_path.name)

else:
    st.caption(
        "Your saved images will appear here after the first generation."
    )


st.caption(
    "Model: Stable Diffusion 1.5 | Hugging Face Diffusers | "
    "Image quality depends on the prompt, seed and model limitations."
)