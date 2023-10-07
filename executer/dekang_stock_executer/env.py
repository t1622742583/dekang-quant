import os
import sys
from loguru import logger
import pandas as pd
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取三级父目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(parent_dir)

from typing import List

from data_helper.geter import get_custom_day
breed_unit = {
    "cb": 10,
    "stock": 100,
}
class Account:
    def __init__(self, init_cash: float = 100000, commission: float = 0.0003, stamp_duty: float = 0.001, breed: str = "cb",position=dict()):
        self.breed = breed
        self.init_cash = init_cash
        self.curr_cash = self.init_cash
        self.now_net_worth = self.init_cash
        self.commission = commission
        self.stamp_duty = stamp_duty
        self.cache_net_worth = []
        self.cache_position = []
        self.position = position
        self.unit = breed_unit[self.breed]

    @property
    def profit(self):
        return self.now_net_worth - self.init_cash

    def update_net_worth(self):
        self.now_net_worth = self.curr_cash + sum([self.position[code]["shares"] * self.unit * self.position[code]["price"] for code in self.position.keys()])
        # 保留2位小数
        self.now_net_worth = round(self.now_net_worth,2)

    def change_position(self, selected_codes: List[dict]):
        # Create a copy of the current position dictionary
        prev_position = self.position.copy()
        trade_signs = []
        # Sell positions not in the selected codes list
        for code in prev_position.keys():
            if code not in [code_info["code"] for code_info in selected_codes]:
                self.sell_position(code)
                trade_signs.append((-1,code,-1))
        # 
        # Update the position for each selected code
        for code_info in selected_codes:
            code = code_info["code"]
            price = code_info["price"]
            conversion_ratio = code_info["ratio"]

            if code in prev_position:
                prev_shares = prev_position[code]["shares"]
                shares_diff = prev_shares - int(self.now_net_worth * conversion_ratio / (price * self.unit))
                shares_diff = int(shares_diff)
                if shares_diff > 0:
                    # Sell a portion of the position
                    shares_to_sell = shares_diff
                    self.sell_position(code, shares_to_sell)
                    trade_signs.append((-1,code,shares_to_sell))
                    
                elif shares_diff < 0:
                    # buy a portion of the position
                    self.buy_position(code, price, -shares_diff)
                    trade_signs.append((1,code,-shares_to_sell))
            else:
                # Buy the position
                shares = self.now_net_worth * conversion_ratio / (price * self.unit)
                shares = int(shares)
                if shares != 0:
                    self.buy_position(code, price, shares)
                    trade_signs.append((1,code,shares))

        # Update the net worth
        self.update_net_worth()
        self.cache_net_worth.append(self.now_net_worth)
        return trade_signs

    def sell_position(self, code: str, shares: int = None):
        if code in self.position:
            if shares is None:
                shares = self.position[code]["shares"]

            price = self.position[code]["price"]

            # Calculate the sale amount
            sale_amount = shares * self.unit * price

            # Calculate the transaction costs
            commission = sale_amount * self.commission
            # 保留2位小数
            commission = round(commission,2)
            stamp_duty = sale_amount * self.stamp_duty
            stamp_duty = round(stamp_duty,2)

            # Update the current cash and net worth
            self.curr_cash += sale_amount - commission - stamp_duty
            self.update_net_worth()

            # Remove the position from the dictionary if all shares are sold
            if shares == self.position[code]["shares"]:
                del self.position[code]
            else:
                # Update the shares in the position dictionary
                self.position[code]["shares"] -= shares

    def buy_position(self, code: str, price: float, shares: int):
        # Calculate the purchase amount
        purchase_amount = shares * self.unit * price

        # Calculate the transaction costs
        commission = purchase_amount * self.commission
        commission = round(commission,2)
        # Check if the current cash is sufficient for the purchase
        if purchase_amount + commission > self.curr_cash:
            print("Insufficient funds to buy the position.")
            return

        # Update the current cash and net worth
        self.curr_cash -= purchase_amount + commission 

        self.update_net_worth()
        # Add the position to the dictionary
        if code not in self.position:
            self.position[code] = {"price": price, "shares": shares}
        else:
            self.position[code]["shares"] += shares

class TradingEnv:
    """交易环境"""
    def __init__(self,
                 features: List,  # 特征列表
                 initial_balance: float = 100000,  # 当前资金
                 commission: float = 0.0003,
                 stamp_duty: float = 0.001,  # 印花税 千1
                 strategy_pipelines: List = None,  # 策略流水线
                 breed: str = "cb"  # 品种 
                 ,data_path:str = None # 数据路径
                 ,position=dict() # 当前持仓
                 ):
        super(TradingEnv, self).__init__()  # 父类初始化
        # 
        self.account = Account(init_cash=initial_balance, commission=commission, stamp_duty=stamp_duty,breed=breed,position=position)  # 账户
        self.features = features  # 特征列表
        self.strategy_pipelines = strategy_pipelines  # 策略管道
        self.selected_codes = []  # 选中的股票/可转债代码
        self.data_path = data_path
        # 获取交易时间内所有行情
    def get_current_observation(self):
        self.current_observation_df = pd.read_parquet(self.data_path)
        self.current_observation_df.set_index("code",inplace=True)
        feature_dict = {}
        for feature in self.features:
            feature_dict[feature.name] = feature(self.current_observation_df)
        self.current_observation_df = pd.DataFrame(feature_dict)
    def __call__(self):
        # 获取当前观察值
        self.get_current_observation()
        # 执行策略流水线 
        for strategy_pipeline in self.strategy_pipelines:
            strategy_pipeline(self)
        return self.account.change_position(self.selected_codes)

