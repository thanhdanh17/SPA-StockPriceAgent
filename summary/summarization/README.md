# News Summarization Pipeline

This system automatically summarizes news articles stored in Supabase using a fine-tuned ViT5 model.

## Features

- Optimized for both CPU and GPU environments
- Batch processing capability
- Continuous operation mode
- Performance monitoring

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your Supabase credentials
4. Place your trained model in the specified folder

## Usage

For one-time processing:
```bash
python main.py