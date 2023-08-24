import pandas as pd


class TopFactor:
    def __init__(self, factors):
        self.factors = factors  # factors: [{"name": "factor_name", "big2small":True}}]


    def __call__(self, env):
        current_observation_df = env.current_observation_df
        current_observation_df['order_by'] = 0.0
        for factor in self.factors:
            current_observation_df['order_by'] = current_observation_df['order_by'] + current_observation_df[factor["name"]].rank(pct=True, ascending= not factor["big2smail"])
        env.selected_df = current_observation_df.sort_values(by='order_by', ascending=False)
class ConditionedWarehouse:
    """调仓"""
    def __init__(self,k=10):
        """
        :param k: 持仓数
        """
        self.k = k
    def __call__(self, env):
        selected_df = env.selected_df
        # 制作成 [(代码，收盘价，持仓比例)]
        selected_df = selected_df.iloc[:self.k]
        selected_df = selected_df[['close']]
        selected_df['ratio'] = 1.0 / self.k
        selected_df.reset_index(inplace=True)
        selected_df.rename(columns={"code":"code","close":"price","ratio":"ratio"},inplace=True)
        env.selected_codes = selected_df.to_dict(orient="records")