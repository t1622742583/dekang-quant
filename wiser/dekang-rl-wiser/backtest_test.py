# 训练策略
import os
import sys

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
from utils import Analyzer, Feature, NormalPrice, NormalVolume
from feature_deals import *
from data_helper.server import save_stock_market_to_h5
from data_helper.geter import get_trade_days, get_day,  lack_data
from data_helper.downloader import download_stock_market_from_tushare
from stable_baselines3.common.vec_env import DummyVecEnv

from stable_baselines3 import PPO as Model
# from stable_baselines3.common.policies import MlpPolicy
# from stable_baselines3.common.policies import ActorCriticPolicy

from loguru import logger
import gym
from data_helper.saver import save_etf_day
import pandas as pd
from typing import List
import argparse
import gym
import numpy as np
import torch
import torch.nn as nn
import torch.distributions as distributions
from stable_baselines3 import PPO

class LSTMExtractor(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMExtractor, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        
    def forward(self, x,use_sde=False):
        # x: (batch_size, sequence_length, input_size)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))  # out: (batch_size, sequence_length, hidden_size)
        
        return out[:, -1, :]  # Return the last hidden state of the LSTM

class CustomPolicy(nn.Module):
    def __init__(self, observation_space, action_space):
        super(CustomPolicy, self).__init__()
        self.observation_space = observation_space
        self.action_space = action_space
        self.observation_size = np.prod(observation_space.shape)
        
        self.lstm_extractor = LSTMExtractor(self.observation_size, hidden_size=128, num_layers=2)
        self.mean = nn.Linear(128, np.prod(action_space.shape))
        self.std = nn.Linear(128, np.prod(action_space.shape))

    def forward(self, obs, use_sde=False):
        obs_flat = obs.view(obs.size(0), -1)

        features = self.lstm_extractor(obs_flat)
        mean = self.mean(features)
        std = torch.exp(self.std(features))
        distribution = distributions.Normal(mean, std)
        action = distribution.sample()
        log_prob = distribution.log_prob(action)
        action = torch.clamp(action, self.action_space.low, self.action_space.high)

        return action, log_prob




def get_results_df(cache_dates, cache_portfolio_mv):
    """ 用于回测结果的可视化
    :param cache_dates: 日期序列
    :param cache_portfolio_mv: 组合市值序列"""
    df = pd.DataFrame(
        {'date': cache_dates, 'portfolio': cache_portfolio_mv})  # 日期和总市值
    df['rate'] = df['portfolio'].pct_change()  # 计算收益率
    df['equity'] = (df['rate'] + 1).cumprod()  # 计算累计收益率
    df.set_index('date', inplace=True)  # 以日期为索引
    df.dropna(inplace=True)  # 删除空值
    return df


class Account:
    def __init__(self,
                 init_cash: float = 10000,  # 初始资金
                 commission: float = 0.0003,  # 手续费
                 stamp_duty: float = 0.001  # 印花税
                 ):
        self.init_cash = init_cash  # 初始资金
        self.curr_cash = self.init_cash  # 当前现金
        self.max_net_worth = self.init_cash  # 最大净值
        self.now_net_worth = self.init_cash  # 当前净值
        self.cost_basis = 0.0  # 每股成本
        self.shares_held = 0  # 持有股票数量
        self.commission = commission  # 手续费
        self.stamp_duty = stamp_duty  # 印花税
        self.cache_portfolio_mv = []  # 每日市值序列

    @property
    def profit(self):
        """收益"""
        return self.now_net_worth - self.init_cash

    def buy(self, now_price: float, buy_ratio: float = 1.0):
        """买入"""
        # 可以购买的股票数量
        max_buy_num = int(self.curr_cash / (now_price *
                          (1 + self.commission + self.stamp_duty)))
        # 使其为100的整数倍
        max_buy_num = max_buy_num // 100 * 100
        # 买入数量
        buy_num = int(max_buy_num * buy_ratio)
        # 买入金额
        buy_amount = buy_num * now_price * (1 + self.commission)
        # 买入后剩余现金
        self.curr_cash -= buy_amount
        # 买入后持仓数量
        self.shares_held += buy_num
        # 买入后成本
        self.cost_basis = self.cost_basis * \
            (1 - buy_ratio) + now_price * buy_ratio
        # 更新当前净值
        self.now_net_worth = self.curr_cash + self.shares_held * now_price
        # 更新最大净值
        self.max_net_worth = max(self.now_net_worth, self.max_net_worth)
        self.cache_portfolio_mv.append(self.now_net_worth)

    def sell(self, now_price: float, sell_ratio: float = 1.0):
        """卖出"""
        # 卖出数量
        sell_num = int(self.shares_held * sell_ratio)
        # 卖出金额
        sell_amount = sell_num * now_price * \
            (1 + self.commission + self.stamp_duty)
        # 卖出后剩余现金
        self.curr_cash += sell_amount
        # 卖出后持仓数量
        self.shares_held -= sell_num
        # 更新当前净值
        self.now_net_worth = self.curr_cash + self.shares_held * now_price
        # 更新最大净值
        self.max_net_worth = max(self.now_net_worth, self.max_net_worth)
        self.cache_portfolio_mv.append(self.now_net_worth)

    def keep(self, now_price: float):
        """暗兵不动"""
        # 更新当前净值
        self.now_net_worth = self.curr_cash + self.shares_held * now_price
        # 更新最大净值
        self.max_net_worth = max(self.now_net_worth, self.max_net_worth)
        self.cache_portfolio_mv.append(self.now_net_worth)
    # weights之和需要<=1，空仓就是cash:1，只调整curr_holding/cash两个变量


class TradingEnv(gym.Env):
    """交易环境"""
    metadata = {'render.modes': ['human']}  # 人类可读的模式

    def __init__(self,
                 market_df: pd.DataFrame,  # 行情数据
                 features: List,  # 特征列表
                 initial_balance: float = 10000,  # 初始账户余额
                 commission: float = 0.0003,
                 stamp_duty: float = 0.001,  # 印花税 千1
                 trade_field: str = 'close'  # 交易字段
                 ):
        super(TradingEnv, self).__init__()  # 父类初始化
        self.account = Account(init_cash=initial_balance,
                               commission=commission, stamp_duty=stamp_duty)  # 账户
        self.market_df = market_df  # 行情数据
        self.initial_balance = initial_balance  # 初始账户余额
        self.commission = commission  # 手续费
        self.stamp_duty = stamp_duty  # 印花税
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)  # 奖励范围
        self.features = features  # 特征列表
        # 定义动作空间
        # 0: 买入 1: 卖出 2: 无操作

        self.action_space = gym.spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        # 定义观察空间 shape=(19,)意思是一维数组，长度为19
        # self.observation_space = gym.spaces.Box(
        #     low=0, high=1, shape=(7,len(features)), dtype=np.float16)
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(len(features),), dtype=np.float16)
        self.trade_prices = self.market_df[trade_field].values  # 交易价格
        cache_market_df = self.market_df.copy()
        for feature in self.features:
            df = feature(self.market_df)
            cache_market_df[feature.name] = df
        self.market_df = cache_market_df
        del cache_market_df
    def _next_observation(self):
        """获取下一个观察值"""
        obs = self.market_df.iloc[self.current_step, :].values
        # 获取前7条记录不足7条则补0
        # obs = self.market_df.iloc[max(self.current_step - 6,0):self.current_step+1, :].values
        # obs = np.pad(obs, ((7 - obs.shape[0], 0), (0, 0)), 'constant')

        # north  = self.account.now_net_worth/(self.initial_balance*10)
        # obs = np.append(obs, north)
        return obs

    def _take_action(self, action):
        """ 执行动作 """
        current_price = self.trade_prices[self.current_step]  # 当前价格
        action_type = action[0]  # 动作类型
        ratio = action[1]  # 购买比例

        if action_type < 1:  # 0-1之间
            # 购买 amount % 的可用余额的股票
            self.account.buy(current_price, ratio)
        elif action_type < 2:  # 1-2之间
            # 卖出 amount % 的持有股票
            self.account.sell(current_price, ratio)
        elif action_type < 3:  # 2-3之间
            # 无操作
            self.account.keep(current_price)
        # 当前净值
    def step(self, action):
        """下一步"""
        self._take_action(action)  # 执行动作
        done = False  # 是否结束
        self.current_step += 1  # 当前步数
        if self.current_step > len(self.market_df.loc[:, 'open'].values) - 1:
            self.current_step = 0  # 重置当前步数(可能是重新训练)
            # done = True
        # 奖励
        reward = self.account.now_net_worth - self.initial_balance  # 奖励
        # reward = 1 if reward > 0 else -2  # 奖励值
        if self.account.now_net_worth < 0:
            done = True
        obs = self._next_observation()
        return obs, reward, done, {}

    def reset(self, new_df: pd.DataFrame = None):
        """重置"""
        self.account = Account(self.initial_balance,
                               self.commission, self.stamp_duty)
        if new_df:
            self.market_df = new_df
        self.current_step = 0
        return self._next_observation()

    def render(self, mode='human', close=False):
        """每日结束"""
        return self.account.now_net_worth



def main1(opt):
    # if opt.breed == 'etf':
    if not opt.use_mutal:
        market_df = get_day(opt.code, opt.breed, opt.start_date, opt.end_date)

        trade_days = get_trade_days(opt.start_date, opt.end_date)
        # 获取当前股票该时期所有交易日的行情数据
        # 如果大于进行去重
        if len(market_df) > len(trade_days):
            market_df = market_df.drop_duplicates(subset=['date'])
        if market_df.empty or len(market_df) != len(trade_days):
            # 下载数据
            lack_data(breed=opt.breed, code=opt.code,
                      start_date=opt.start_date, end_date=opt.end_date)
            # 保存到.h5
            market_df = get_day(opt.code, opt.breed,
                                opt.start_date, opt.end_date)
        # date作为索引
        market_df.set_index('date', inplace=True)
        logger.info(market_df)
        # 按中间时间段划分训练集和测试集
        train_market_df = market_df[:int(len(market_df) * 0.8)]
        test_market_df = market_df[int(len(market_df) * 0.8):]
        # 特征
        features = [
            Feature("open", normalization=NormalPrice()),
            Feature("high", normalization=NormalPrice()),
            Feature("low", normalization=NormalPrice()),
            Feature("close", normalization=NormalPrice()),
            Feature("volume", normalization=NormalVolume()),
        ]
        # 创建环境
        env = DummyVecEnv(
            [lambda: TradingEnv(train_market_df, features)])  # 创建环境
        # 创建模型
        # policy = CustomPolicy(env.envs[0].observation_space, env.envs[0].action_space)
        model = Model("MlpPolicy", env, verbose=0, tensorboard_log='./log')
        model.learn(total_timesteps=int(1e5),progress_bar=True)
        # 测试环境 因为要对TradingEnv传参，所以要用lambda
        env = DummyVecEnv([lambda: TradingEnv(test_market_df, features)])
        obs = env.reset()
        cache_portfolio_mv = [env.envs[0].render()]  # 缓存组合市值
        for i in range(len(test_market_df) - 1):
            action, _states = model.predict(obs)
            obs, rewards, done, info = env.step(action)
            # 惩罚模型
            mv = env.envs[0].render()  # 每日净值
            cache_portfolio_mv.append(mv)
            if done:
                break
        df_results = get_results_df(test_market_df.index, cache_portfolio_mv)
        analyzer = Analyzer(df_results, opt.benckmarks)
        analyzer.plot()
        analyzer.show_results()
        # 询问是否保存模型
        if input('是否保存模型？(y/n)').lower() == 'y':
            model.save('./model/{}.pkl'.format(opt.code))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--codes', type=List, default=[
                        'sh510300', 'sh510050', 'sz159915', 'sh510500', 'sh588000'], help='代码')
    parser.add_argument('--code', type=str, default='sh510050', help='代码')
    parser.add_argument('--breed', type=str, default='etf', help='品种')
    parser.add_argument('--start_date', type=str, default='2015-01-01', help='开始时间')
    parser.add_argument('--mid_date', type=str, default='2020-01-01', help='中间时间')
    parser.add_argument('--end_date', type=str, default='2023-01-01', help='结束时间')
    # 使用已有模型/重新
    parser.add_argument('--benckmarks', type=List, default=['sh510300'], help='对比'
                        '基准')
    parser.add_argument(
        '--use_mutal', action='store_true', help='多代码交易'
    )
    # TODO: 动作空间：买入、卖出、无操作/保持比例
    opt = parser.parse_args()
    main1(opt)
# 优化策略
# - nlp转为lstm
# - 基于数字货币