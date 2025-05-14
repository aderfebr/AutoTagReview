import torch
import json
import numpy as np
from transformers import BertTokenizer, BertModel

class ClassifyNet(torch.nn.Module):
    def __init__(self, label_number, feature_layers, bert_hidden_size):
        super(ClassifyNet, self).__init__()

        self.feature_layers = feature_layers
        self.dropout = torch.nn.Dropout(0.5)
        self.linear = torch.nn.Linear(feature_layers * bert_hidden_size, label_number)

    def forward(self, x):
        out = x['hidden_states']
        out = torch.cat([out[-i][:, 0] for i in range(1, self.feature_layers + 1)], dim=-1)
        out = self.dropout(out)
        out = self.linear(out)

        return out

def get_label_num(label_map_path):
    with open(label_map_path, 'r', encoding='utf-8') as file:
        label_map = json.load(file)
        return len(label_map)

def load_model(model_path, label_map_path, device):
    # Load tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    
    # Load BERT model
    bert = BertModel.from_pretrained(model_path).to(device)
    
    # Load ClassifyNet
    classify_net = ClassifyNet(
        label_number=get_label_num(label_map_path),
        feature_layers=10,
        bert_hidden_size=bert.config.hidden_size
    ).to(device)
    classify_net.load_state_dict(torch.load(f"{model_path}/student_model_file.bin",map_location=device))
    
    return bert, classify_net, tokenizer

def prepare_input(text, tokenizer, device, max_length=128):
    inputs = tokenizer(
        text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    return {k: v.to(device) for k, v in inputs.items()}

def predict_bert(model_path, label_map_path, text):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model
    bert, classify_net, tokenizer = load_model(model_path, label_map_path, device)
    bert.eval()
    classify_net.eval()
    
    # Prepare input
    inputs = prepare_input(text, tokenizer, device)
    
    # Run inference
    with torch.no_grad():
        # Get BERT embeddings
        bert_out = bert(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            output_hidden_states=True
        )
        
        # Get predictions
        logits = classify_net(bert_out)
        probs = torch.sigmoid(logits).cpu().numpy().tolist()[0]
    
    return probs