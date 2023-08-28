import os
import sys
from loguru import logger
import pandas as pd
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(parent_dir)
from utils import Analyzer, Feature
from typing import List
from data_helper.geter import get_all_day_ml
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
# 加载数据并划分训练集和测试集
codes,market_df = get_all_day_ml(start_date="2019-01-01",use_cache=True)
# nan_columns = market_df.columns[market_df.isna().any()].tolist()
# 保存为csv文件(覆盖)
nan_counts = market_df.isna().sum()

# 确定要删除的列
columns_to_drop = nan_counts[nan_counts > 0.1 * len(market_df)].index.tolist()

# 删除包含NaN值数量大于总长度的0.1的列
market_df = market_df.drop(columns=columns_to_drop)
market_df = market_df.dropna()

# 划分训练集和测试集
split_date = '2022-01-01'

# 获取所有非字符串列名

features = market_df.columns.drop(['date', 'code', 'up_down']).tolist()

# 选择所有非字符串类型的字段
# features = market_df[features].select_dtypes(exclude=['object']).columns.tolist()
fenxi_features = features + ['up_down']
correlations = market_df[fenxi_features].corr()["up_down"]
# 获取相关性排名前10的因子
top_factors = correlations.abs().nlargest(10).index.tolist()
top_factors.remove('up_down')

print("Top factors:", top_factors)
features = top_factors
train_df = market_df[market_df['date'] < split_date]
test_df = market_df[market_df['date'] >= split_date]
target = 'up_down'  # 替换为您实际的目标列名称

# 划分特征和目标变量
X_train = train_df[features]
y_train = train_df[target]
X_test = test_df[features]
y_test = test_df[target]

# 创建分类器列表
classifiers = [
    # ('Logistic Regression', make_pipeline(StandardScaler(), LogisticRegression())),
    # ('Decision Tree', DecisionTreeClassifier()),
    # ('Random Forest', RandomForestClassifier()),
    # 
    # ('Gradient Boosting', GradientBoostingClassifier()),
    ('AdaBoost', AdaBoostClassifier()),
    ('XGBoost', XGBClassifier()),
    ('SVM', make_pipeline(StandardScaler(), SVC())),
]
# 
# 对每个分类器进行训练和验证
for name, classifier in classifiers:
    print(f"Training and validating {name}...")
    model = classifier.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")