from flask import Flask, request, jsonify
import torch
import numpy as np
from flask_cors import CORS
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax

app = Flask(__name__)
CORS(app)
# 检查是否有可用的GPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# 模型和参数设置
model_name = 'bert-base-chinese'  # 使用的预训练模型名称
model_path = 'workspace/wb/1.pt'  # 模型权重路径
num_labels = 7  # 分类标签数量

# 加载模型与分词器
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
print(f'Loading checkpoint: {model_path} ...')
state_dict = torch.load(model_path, map_location='cpu')
model.load_state_dict(state_dict, strict=True)
model.to(device)
model.eval()

# 定义标签映射
label = {0: '开心', 1: '生气', 2: '伤心', 3: '害怕', 4: '惊吓', 5: '中性', 6:'爱'}

tokenizer = AutoTokenizer.from_pretrained(model_name)


def predict_emotion(input_text):
    # 对输入文本进行编码
    token = tokenizer(input_text, padding='max_length', truncation=True, max_length=140, return_tensors='pt')

    # 将数据移动到设备上（CPU或GPU）
    input_ids = token['input_ids'].to(device)

    with torch.no_grad():
        output = model(input_ids)
    logits = output.logits.detach().cpu().numpy()

    # 计算softmax概率并转换为百分比
    probabilities = softmax(logits, axis=1)[0] * 100

    # 找出概率最高的情绪
    predicted_emotion_index = np.argmax(probabilities)
    predicted_emotion = label[predicted_emotion_index]

    # 返回所有预测结果和最终答案
    all_probabilities = {label[i]: f'{prob:.2f}%' for i, prob in enumerate(probabilities)}

    return {
        'predicted_emotion': predicted_emotion,
        'all_probabilities': all_probabilities,
        'final_answer': f'预测情绪: {predicted_emotion} 的概率为: {all_probabilities[predicted_emotion]}'
    }


@app.route('/myApp/analysis/', methods=['POST'])
def analysis():
    # 获取前端发送的文本
    input_text = request.form.get('example-nf-email')

    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    # 进行情感预测
    result = predict_emotion(input_text)

    # 返回预测结果
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)