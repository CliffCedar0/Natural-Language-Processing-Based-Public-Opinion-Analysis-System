import os
import django

# 初始化 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '微博舆情分析.settings')
django.setup()

# 导入 Django 模块
from myApp.models import TiebaInfo

# 编写你的逻辑
print("开始运行爬虫脚本...")
