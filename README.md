# SPA-StockPriceAgent
# Industry-Sentiment-Classifier

This repository contains the implementation of sentiment and industry classification models using PhoBERT and XLM transformers.

## Sentiment

### PhoBERT
#### PhoBERT thường
- data 5k title: 0.6
- data 5k summary v1: 0.73
- data 12k v2: 0.76
- data 12k fix v4: 0.8

#### PhoBERT tuning
- data: 12k v3: 
- data: 12k fix v5: 

### XLM
- data 5k summary v1: 0.76
- data 12k v2: 0.75
- data 12k fix v3: 0.81

## Industry

### PhoBERT
#### PhoBERT thường
- data 5k title: 0.78
- data 5k summary v1: 0.85
- data 12k v2: 0.83
- data 12k fix v4: 0.9

#### PhoBERT tuning
- data: 12k v3: 0.83
- data: 12k fix v5:

### XLM
- data 5k summary v1: 0.8
- data 12k v2: 0.78
- data 12k fix v3: 0.84

## Training Outputs
The output files from training each version (v1, v2, v3, v4, v5, etc.) are available at:  
[https://drive.google.com/drive/folders/1bt9ES-e-YQiNZPGd8odRfEhv0ove0aCl](https://drive.google.com/drive/folders/1bt9ES-e-YQiNZPGd8odRfEhv0ove0aCl)