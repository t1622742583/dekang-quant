import os
import sys
from loguru import logger
import pandas as pd
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
# 训练机器学习模型
sys.path.append(parent_dir)
from data_helper.geter import get_all_day


df = get_all_day(breed="stock",cache=True,ud=True)
# 2023年之前作为训练集
pass