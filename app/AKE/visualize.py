import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载预训练的中文BERT模型和分词器
model_name = "./app/AKE/bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def generate_embeddings(phrases):
    embeddings = []
    for phrase in phrases:
        inputs = tokenizer(phrase, return_tensors="pt", padding=True, truncation=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        # 使用均值池化生成句子向量
        phrase_embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy().squeeze()
        embeddings.append(phrase_embedding)
    embeddings_matrix = np.array(embeddings)
    # L2标准化以优化余弦相似度计算
    return normalize(embeddings_matrix, norm='l2')

def visualize(phrases):
    matrix = []
    source = []
    for k, v in phrases.items():
        matrix += v
        source += [k] * len(v)
    
    embeddings_matrix = generate_embeddings(matrix)
    
    # 使用DBSCAN进行聚类
    dbscan = DBSCAN(eps=0.65, min_samples=3)
    cluster_labels = dbscan.fit_predict(embeddings_matrix).tolist()
    
    unique_labels = set(cluster_labels)
    if -1 in unique_labels:
        unique_labels.remove(-1)
    
    pca_3d = PCA(n_components=3)
    embeddings_3d = pca_3d.fit_transform(embeddings_matrix).tolist()
    
    by_type = {k: [] for k in phrases.keys()}
    
    by_cluster = {}
    for label in unique_labels:
        by_cluster[f'聚类{label}'] = []
    
    if -1 in set(cluster_labels):
        by_cluster['噪声点'] = []
    
    for i in range(len(matrix)):
        x, y, z = embeddings_3d[i]
        text = matrix[i]
        src = source[i]
        cluster_id = cluster_labels[i]
        
        by_type[src].append([x, y, z, text])
        
        if cluster_id == -1:
            by_cluster['噪声点'].append([x, y, z, text])
        else:
            by_cluster[f'聚类{cluster_id}'].append([x, y, z, text])
    
    return by_type, by_cluster