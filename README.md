```markdown
# Script for Creating SDXL LoRAs on Modal
A sample script for creating LoRAs for SDXL using [Modal](https://modal.com/).

## What is Modal?
[Modal](https://modal.com/) is a cloud environment for executing arbitrary Python code. It is particularly well-suited for AI/ML workloads, offering affordable access to GPU resources.  
The free tier provides $30 in monthly credits.

Pricing is based on CPU, memory, and GPU usage time. Running an A10G instance for an hour costs just over $1 USD, making LoRA generation relatively accessible.

## Preparation
Requires Python 3.10 or later.

```bash
git clone sdxl-lora-gen-with-modal
cd sdxl-lora-gen-with-modal
python -m venv venv
venv/Script/activate
pip install -r requirements.txt
```

1. Register on Modal's website.
2. Run `python -m modal setup` for initial configuration.

## Usage
Example: Creating a Tohoku Kiritan LoRA

1. **Download training data**  
Download the "kiritan" dataset from [AI Image Model Training Data](https://zunko.jp/con_illust.html) under "02_LoRA学習用データ_B氏提供版_背景透過".

2. **Process images**  
Resize images to 1024x1024 for SDXL training:  
`python resizer.py kiritan`

3. **Upload base model**  
Upload your base model to Modal:  
```bash
modal volume create models
modal volume put models <model_filename> /
```

4. **Configure files**  
Copy and edit `config.toml` and `dataset.toml` to your dataset folder (kiritan).  
Set `pretrained_model_name_or_path = '/model/<model_filename>'` and adjust other parameters.  
Reference: [Configuration Guide (Japanese)](https://hoshikat.hatenablog.com/entry/2023/05/26/223229)

5. **Start training**  
```bash
modal run generate_lora.py --name kiritan
```
- Training takes ~30 minutes on A10G
- Monitor progress via console or Modal's web interface
- Stop jobs using "Stop Now" in Modal's logs if needed
- Final output: `kiritan.safetensors`

## Cleanup
After successful training:  
```bash
modal volume delete inputs
modal volume delete outputs
modal volume delete models
```

## Tips
- Match `--name` parameter with your dataset directory name
- Change GPU type by modifying `GPU = "A10G"` in `generate_lora.py`
- For configuration details, see [sd-script documentation](https://github.com/kohya-ss/sd-scripts)
```
