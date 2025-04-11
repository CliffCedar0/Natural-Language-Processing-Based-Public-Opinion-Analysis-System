# 基于自然语言处理的舆情分析系统 / Natural Language Processing Based Public Opinion Analysis System

## 项目简介 / Project Introduction
这是一个基于自然语言处理技术的舆情分析系统，集成了多种先进的文本分析技术，包括BERTopic、LDA主题建模、RAG（检索增强生成）和词云可视化等功能。系统能够对社交媒体平台（如微博、贴吧）的评论内容进行深度分析，帮助用户理解公众舆论趋势和热点话题。

This is a public opinion analysis system based on natural language processing technology, integrating multiple advanced text analysis techniques including BERTopic, LDA topic modeling, RAG (Retrieval-Augmented Generation), and word cloud visualization. The system can perform in-depth analysis of social media platform (such as Weibo and Tieba) comments, helping users understand public opinion trends and hot topics.

## 主要功能 / Main Features
1. **主题建模 / Topic Modeling**
   - BERTopic：利用预训练语言模型进行主题建模 / Using pre-trained language models for topic modeling
   - LDA：传统主题建模方法 / Traditional topic modeling method
   - 主题可视化：提供直观的主题分布图表 / Topic visualization: Provides intuitive topic distribution charts
   - 支持DBSCAN聚类分析 / Supports DBSCAN clustering analysis
   - 主题分布统计和可视化 / Topic distribution statistics and visualization

2. **情感分析 / Sentiment Analysis**
   - 基于BERT的中文情感分类 / BERT-based Chinese sentiment classification
   - 七类情感分析（开心、生气、伤心、害怕、惊吓、中性、爱） / Seven-category sentiment analysis (happy, angry, sad, afraid, scared, neutral, love)
   - 情感概率分布分析 / Sentiment probability distribution analysis
   - 情感趋势可视化 / Sentiment trend visualization
   - 细粒度情感分析（支持多类别情感） / Fine-grained sentiment analysis (supports multiple sentiment categories)
   - 情感强度分析 / Sentiment intensity analysis
   - 情感时间序列分析 / Sentiment time series analysis
   - 情感分布统计 / Sentiment distribution statistics

3. **检索增强生成 (RAG) / Retrieval-Augmented Generation**
   - 基于向量数据库的语义检索 / Semantic search based on vector database
   - 结合大语言模型的智能问答 / Intelligent Q&A with large language models
   - 支持多轮对话和上下文理解 / Supports multi-turn conversations and context understanding
   - 实时舆情分析和趋势预测 / Real-time public opinion analysis and trend prediction

4. **词云生成 / Word Cloud Generation**
   - 支持自定义词云形状 / Supports custom word cloud shapes
   - 智能过滤停用词 / Intelligent stop word filtering
   - 支持中英文混合文本处理 / Supports mixed Chinese-English text processing
   - 支持微博、贴吧、评论数据生成词云 / Supports word cloud generation for Weibo, Tieba, and comment data

5. **数据采集 / Data Collection**
   - 支持微博数据爬取 / Supports Weibo data crawling
   - 支持贴吧数据爬取 / Supports Tieba data crawling
   - 数据清洗和预处理 / Data cleaning and preprocessing
   - 支持CSV格式数据导入导出 / Supports CSV format data import and export

## 技术栈 / Technology Stack
- Python 3.10
- 自然语言处理库 / NLP Libraries：
  - jieba（中文分词） / Chinese text segmentation
  - BERTopic
  - Gensim（LDA实现） / LDA implementation
  - Transformers（情感分析） / Transformers (for sentiment analysis)
  - PyTorch（深度学习框架） / PyTorch (deep learning framework)
- 检索增强生成 / RAG：
  - LangChain
  - Vector Database
  - Large Language Models
- 数据可视化 / Data Visualization：
  - Matplotlib
  - WordCloud
  - Plotly（情感趋势可视化） / Plotly (for sentiment trend visualization)
- 数据库 / Database：
  - MySQL
- Web框架 / Web Framework：
  - Django（后端） / Django (backend)
  - Flask（情感分析服务） / Flask (sentiment analysis service)
- 其他工具 / Other Tools：
  - Jupyter Notebook（数据分析） / Jupyter Notebook (data analysis)
  - scikit-learn（机器学习） / scikit-learn (machine learning)
  - pandas（数据处理） / pandas (data processing)

## 安装说明 / Installation Guide
1. 克隆项目到本地 / Clone the project locally：
```bash
git clone [项目地址 / project URL]
```

2. 创建并激活虚拟环境 / Create and activate virtual environment：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 / or
.venv\Scripts\activate  # Windows
```

3. 安装依赖包 / Install dependencies：
```bash
pip install -r requirements.txt
```

4. 初始化数据库 / Initialize database：
```bash
python manage.py migrate
```

## 使用说明 / Usage Guide
1. **数据采集 / Data Collection**
   - 运行爬虫脚本收集微博和贴吧数据 / Run crawler scripts to collect Weibo and Tieba data
   - 数据会自动存储到MySQL数据库中 / Data will be automatically stored in MySQL database

2. **主题分析 / Topic Analysis**
   - 运行BERTopic或LDA分析脚本 / Run BERTopic or LDA analysis scripts
   - 查看生成的主题可视化结果 / View generated topic visualization results

3. **词云生成 / Word Cloud Generation**
   - 准备背景图片 / Prepare background image
   - 运行wordCloud.py脚本 / Run wordCloud.py script
   - 查看生成的词云图片 / View generated word cloud image

4. **Web界面 / Web Interface**
   - 启动Django服务器 / Start Django server：
```bash
python manage.py runserver
```
   - 访问 http://localhost:8000 查看分析结果 / Visit http://localhost:8000 to view analysis results

## 项目结构 / Project Structure
```
├── deateset/          # 数据集目录 / Dataset directory
├── sentiment_analysis/ # 情感分析模块 / Sentiment analysis module
├── topic_model/       # 主题建模相关代码 / Topic modeling related code
├── spiders/           # 爬虫模块 / Crawler module
├── utils/             # 工具函数 / Utility functions
├── static/            # 静态资源 / Static resources
├── templates/         # 网页模板 / Web templates
├── wordCloud.py       # 词云生成脚本 / Word cloud generation script
└── manage.py          # Django管理脚本 / Django management script
```

## 注意事项 / Notes
1. 使用前请确保已安装所有必要的依赖包 / Make sure all necessary dependencies are installed before use
2. 词云生成需要中文字体文件（STHUPO.TTF） / Word cloud generation requires Chinese font file (STHUPO.TTF)
3. 爬虫使用时请遵守相关网站的使用条款 / Please comply with the terms of use of relevant websites when using crawlers
4. 建议使用GPU加速BERTopic模型训练 / It is recommended to use GPU to accelerate BERTopic model training

## 贡献指南 / Contribution Guide
欢迎提交Issue和Pull Request来帮助改进项目。在提交代码前，请确保：
Welcome to submit Issues and Pull Requests to help improve the project. Before submitting code, please ensure:
1. 代码符合PEP 8规范 / Code complies with PEP 8 standards
2. 添加必要的注释 / Add necessary comments
3. 更新相关文档 / Update relevant documentation

## 许可证 / License
[请在此处添加许可证信息 / Please add license information here]

## 作者信息 / Author Information
- 作者 / Author: Junjie Chen
- 邮箱 / Email: cliffcedar0@gmail.com 