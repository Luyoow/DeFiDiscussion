import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# 下载nltk停用词和分词数据
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# 数据预处理函数
def preprocess_text(text):
    # 转小写
    text = text.lower()
    # 去除标点符号
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    # 分词
    words = word_tokenize(text)
    # 去除停用词
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # 词干提取
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words]
    return " ".join(words)

# 读取对话文件
with open('./matching/dialog.txt', 'r', encoding='utf-8') as file:
    dialogues = file.read().replace('\n', '')

# 读取简介文件
data = pd.read_csv('./matching/all-attack.csv')
summaries = data['Description'].tolist()

print('----------------------------------------------------------------------')
print('Discussion is:')
print(dialogues)
print('----------------------------------------------------------------------')


# 预处理对话和简介


    
preprocessed_dialogues = [preprocess_text(dialogues)]
preprocessed_summaries = [preprocess_text(summary) for summary in summaries]

# 使用TF-IDF生成特征向量
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(preprocessed_dialogues + preprocessed_summaries)

# 计算相似度
dialogue_vectors = vectors[:len(preprocessed_dialogues)]
summary_vectors = vectors[len(preprocessed_dialogues):]

similarities = cosine_similarity(dialogue_vectors, summary_vectors)

# 获取每个对话对应的前10个简介
top_n = 10
top_summaries_indices = [np.argsort(similarity)[-top_n:][::-1] for similarity in similarities]

# 输出结果
results = {}
for i, indices in enumerate(top_summaries_indices):
    results[f"Dialogue {i+1}"] = data['Hacked target'].iloc[indices].tolist()


# 打印结果
for dialogue, targets in results.items():
    print(f"Best matched related DeFi Discussions are: {targets}")
