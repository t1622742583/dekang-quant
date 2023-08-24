# 基本字段 |
|  ## ETF |
|  - open: 开盘价 |
|  - high: 最高价 |
|  - low: 最低价 |
|  - close: 收盘价 |
|  - volume: 成交量 |
|  ## 可转债 |
|  - open: 开盘价 |
|  - high: 最高价 |
|  - low: 最低价 |
|  - close: 收盘价 |
|  - volume: 成交量 |
## 股票

|  名称 | 类型 | 描述 |
|:---:|:---:|:---:|
|  trade_date | str | 交易日期 |
|  open | float | 开盘价 |
|  high | float | 最高价 |
|  low | float | 最低价 |
|  close | float | 收盘价 |
|  pre_close | float | 昨收价(前复权) |
|  change | float | 涨跌额 |
|  pct_chg | float | 涨跌幅 （未复权，如果是复权请用 通用行情接口 ） |
|  vol | float | 成交量 （手） |
|  amount | float | 成交额 （千元） |
|  turnover_rate | float | 换手率（%） |
|  turnover_rate_f | float | 换手率（自由流通股） |
|  volume_ratio | float | 量比 |
|  pe | float | 市盈率（总市值/净利润， 亏损的PE为空） |
|  pe_ttm | float | 市盈率（TTM，亏损的PE为空） |
|  pb | float | 市净率（总市值/净资产） |
|  ps | float | 市销率 |
|  ps_ttm | float | 市销率（TTM） |
|  dv_ratio | float | 股息率 （%） |
|  dv_ttm | float | 股息率（TTM）（%） |
|  total_share | float | 总股本 （万股） |
|  float_share | float | 流通股本 （万股） |
|  free_share | float | 自由流通股本 （万） |
|  total_mv | float | 总市值 （万元） |
|  circ_mv | float | 流通市值（万元） |
|  f_ann_date | str | 实际公告日期 |
|  end_date | str | 报告期 |
|  report_type | str | 报告类型 见底部表 |
|  comp_type | str | 公司类型(1一般工商业2银行3保险4证券) |
|  end_type | str | 报告期类型 |
|  basic_eps | float | 基本每股收益 |
|  diluted_eps | float | 稀释每股收益 |
|  total_revenue | float | 营业总收入 |
|  revenue | float | 营业收入 |
|  int_income | float | 利息收入 |
|  prem_earned | float | 已赚保费 |
|  comm_income | float | 手续费及佣金收入 |
|  n_commis_income | float | 手续费及佣金净收入 |
|  n_oth_income | float | 其他经营净收益 |
|  n_oth_b_income | float | 加:其他业务净收益 |
|  prem_income | float | 保险业务收入 |
|  out_prem | float | 减:分出保费 |
|  une_prem_reser | float | 提取未到期责任准备金 |
|  reins_income | float | 其中:分保费收入 |
|  n_sec_tb_income | float | 代理买卖证券业务净收入 |
|  n_sec_uw_income | float | 证券承销业务净收入 |
|  n_asset_mg_income | float | 受托客户资产管理业务净收入 |
|  oth_b_income | float | 其他业务收入 |
|  fv_value_chg_gain | float | 加:公允价值变动净收益 |
|  invest_income | float | 加:投资净收益 |
|  ass_invest_income | float | 其中:对联营企业和合营企业的投资收益 |
|  forex_gain | float | 加:汇兑净收益 |
|  total_cogs | float | 营业总成本 |
|  oper_cost | float | 减:营业成本 |
|  int_exp | float | 减:利息支出 |
|  comm_exp | float | 减:手续费及佣金支出 |
|  biz_tax_surchg | float | 减:营业税金及附加 |
|  sell_exp | float | 减:销售费用 |
|  admin_exp | float | 减:管理费用 |
|  fin_exp | float | 减:财务费用 |
|  assets_impair_loss | float | 减:资产减值损失 |
|  prem_refund | float | 退保金 |
|  compens_payout | float | 赔付总支出 |
|  reser_insur_liab | float | 提取保险责任准备金 |
|  div_payt | float | 保户红利支出 |
|  reins_exp | float | 分保费用 |
|  oper_exp | float | 营业支出 |
|  compens_payout_refu | float | 减:摊回赔付支出 |
|  insur_reser_refu | float | 减:摊回保险责任准备金 |
|  reins_cost_refund | float | 减:摊回分保费用 |
|  other_bus_cost | float | 其他业务成本 |
|  operate_profit | float | 营业利润 |
|  non_oper_income | float | 加:营业外收入 |
|  non_oper_exp | float | 减:营业外支出 |
|  nca_disploss | float | 其中:减:非流动资产处置净损失 |
|  total_profit | float | 利润总额 |
|  income_tax | float | 所得税费用 |
|  n_income | float | 净利润(含少数股东损益) |
|  n_income_attr_p | float | 净利润(不含少数股东损益) |
|  minority_gain | float | 少数股东损益 |
|  oth_compr_income | float | 其他综合收益 |
|  t_compr_income | float | 综合收益总额 |
|  compr_inc_attr_p | float | 归属于母公司(或股东)的综合收益总额 |
|  compr_inc_attr_m_s | float | 归属于少数股东的综合收益总额 |
|  ebit | float | 息税前利润 |
|  ebitda | float | 息税折旧摊销前利润 |
|  insurance_exp | float | 保险业务支出 |
|  undist_profit | float | 年初未分配利润 |
|  distable_profit | float | 可分配利润 |
|  rd_exp | float | 研发费用 |
|  fin_exp_int_exp | float | 财务费用:利息费用 |
|  fin_exp_int_inc | float | 财务费用:利息收入 |
|  transfer_surplus_rese | float | 盈余公积转入 |
|  transfer_housing_imprest | float | 住房周转金转入 |
|  transfer_oth | float | 其他转入 |
|  adj_lossgain | float | 调整以前年度损益 |
|  withdra_legal_surplus | float | 提取法定盈余公积 |
|  withdra_legal_pubfund | float | 提取法定公益金 |
|  withdra_biz_devfund | float | 提取企业发展基金 |
|  withdra_rese_fund | float | 提取储备基金 |
|  withdra_oth_ersu | float | 提取任意盈余公积金 |
|  workers_welfare | float | 职工奖金福利 |
|  distr_profit_shrhder | float | 可供股东分配的利润 |
|  prfshare_payable_dvd | float | 应付优先股股利 |
|  comshare_payable_dvd | float | 应付普通股股利 |
|  capit_comstock_div | float | 转作股本的普通股股利 |
|  net_after_nr_lp_correct | float  | 扣除非经常性损益后的净利润（更正前） |
|  credit_impa_loss | float  | 信用减值损失 |
|  net_expo_hedging_benefits | float  | 净敞口套期收益 |
|  oth_impair_loss_assets | float  | 其他资产减值损失 |
|  total_opcost | float  | 营业总成本（二） |
|  amodcost_fin_assets | float  | 以摊余成本计量的金融资产终止确认收益 |
|  oth_income | float  | 其他收益 |
|  asset_disp_income | float  | 资产处置收益 |
|  continued_net_profit | float  | 持续经营净利润 |
|  end_net_profit | float  | 终止经营净利润 |
|  update_flag | str | 更新标识 |
|  end_date | str | 报告期 |
|  eps | float | 基本每股收益 |
|  dt_eps | float | 稀释每股收益 |
|  total_revenue_ps | float | 每股营业总收入 |
|  revenue_ps | float | 每股营业收入 |
|  capital_rese_ps | float | 每股资本公积 |
|  surplus_rese_ps | float | 每股盈余公积 |
|  undist_profit_ps | float | 每股未分配利润 |
|  extra_item | float | 非经常性损益 |
|  profit_dedt | float | 扣除非经常性损益后的净利润（扣非净利润） |
|  gross_margin | float | 毛利 |
|  current_ratio | float | 流动比率 |
|  quick_ratio | float | 速动比率 |
|  cash_ratio | float | 保守速动比率 |
|  invturn_days | float  | 存货周转天数 |
|  arturn_days | float  | 应收账款周转天数 |
|  inv_turn | float  | 存货周转率 |
|  ar_turn | float | 应收账款周转率 |
|  ca_turn | float | 流动资产周转率 |
|  fa_turn | float | 固定资产周转率 |
|  assets_turn | float | 总资产周转率 |
|  op_income | float | 经营活动净收益 |
|  valuechange_income | float  | 价值变动净收益 |
|  interst_income | float  | 利息费用 |
|  daa | float  | 折旧与摊销 |
|  ebit | float | 息税前利润 |
|  ebitda | float | 息税折旧摊销前利润 |
|  fcff | float | 企业自由现金流量 |
|  fcfe | float | 股权自由现金流量 |
|  current_exint | float | 无息流动负债 |
|  noncurrent_exint | float | 无息非流动负债 |
|  interestdebt | float | 带息债务 |
|  netdebt | float | 净债务 |
|  tangible_asset | float | 有形资产 |
|  working_capital | float | 营运资金 |
|  networking_capital | float | 营运流动资本 |
|  invest_capital | float | 全部投入资本 |
|  retained_earnings | float | 留存收益 |
|  diluted2_eps | float | 期末摊薄每股收益 |
|  bps | float | 每股净资产 |
|  ocfps | float | 每股经营活动产生的现金流量净额 |
|  retainedps | float | 每股留存收益 |
|  cfps | float | 每股现金流量净额 |
|  ebit_ps | float | 每股息税前利润 |
|  fcff_ps | float | 每股企业自由现金流量 |
|  fcfe_ps | float | 每股股东自由现金流量 |
|  netprofit_margin | float | 销售净利率 |
|  grossprofit_margin | float | 销售毛利率 |
|  cogs_of_sales | float | 销售成本率 |
|  expense_of_sales | float | 销售期间费用率 |
|  profit_to_gr | float | 净利润/营业总收入 |
|  saleexp_to_gr | float | 销售费用/营业总收入 |
|  adminexp_of_gr | float | 管理费用/营业总收入 |
|  finaexp_of_gr | float | 财务费用/营业总收入 |
|  impai_ttm | float | 资产减值损失/营业总收入 |
|  gc_of_gr | float | 营业总成本/营业总收入 |
|  op_of_gr | float | 营业利润/营业总收入 |
|  ebit_of_gr | float | 息税前利润/营业总收入 |
|  roe | float | 净资产收益率 |
|  roe_waa | float | 加权平均净资产收益率 |
|  roe_dt | float | 净资产收益率(扣除非经常损益) |
|  roa | float | 总资产报酬率 |
|  npta | float | 总资产净利润 |
|  roic | float | 投入资本回报率 |
|  roe_yearly | float | 年化净资产收益率 |
|  roa2_yearly | float | 年化总资产报酬率 |
|  roe_avg | float  | 平均净资产收益率(增发条件) |
|  opincome_of_ebt | float  | 经营活动净收益/利润总额 |
|  investincome_of_ebt | float  | 价值变动净收益/利润总额 |
|  n_op_profit_of_ebt | float  | 营业外收支净额/利润总额 |
|  tax_to_ebt | float  | 所得税/利润总额 |
|  dtprofit_to_profit | float  | 扣除非经常损益后的净利润/净利润 |
|  salescash_to_or | float  | 销售商品提供劳务收到的现金/营业收入 |
|  ocf_to_or | float  | 经营活动产生的现金流量净额/营业收入 |
|  ocf_to_opincome | float  | 经营活动产生的现金流量净额/经营活动净收益 |
|  capitalized_to_da | float  | 资本支出/折旧和摊销 |
|  debt_to_assets | float | 资产负债率 |
|  assets_to_eqt | float | 权益乘数 |
|  dp_assets_to_eqt | float | 权益乘数(杜邦分析) |
|  ca_to_assets | float | 流动资产/总资产 |
|  nca_to_assets | float | 非流动资产/总资产 |
|  tbassets_to_totalassets | float | 有形资产/总资产 |
|  int_to_talcap | float | 带息债务/全部投入资本 |
|  eqt_to_talcapital | float | 归属于母公司的股东权益/全部投入资本 |
|  currentdebt_to_debt | float | 流动负债/负债合计 |
|  longdeb_to_debt | float | 非流动负债/负债合计 |
|  ocf_to_shortdebt | float | 经营活动产生的现金流量净额/流动负债 |
|  debt_to_eqt | float | 产权比率 |
|  eqt_to_debt | float | 归属于母公司的股东权益/负债合计 |
|  eqt_to_interestdebt | float | 归属于母公司的股东权益/带息债务 |
|  tangibleasset_to_debt | float | 有形资产/负债合计 |
|  tangasset_to_intdebt | float | 有形资产/带息债务 |
|  tangibleasset_to_netdebt | float | 有形资产/净债务 |
|  ocf_to_debt | float | 经营活动产生的现金流量净额/负债合计 |
|  ocf_to_interestdebt | float  | 经营活动产生的现金流量净额/带息债务 |
|  ocf_to_netdebt | float  | 经营活动产生的现金流量净额/净债务 |
|  ebit_to_interest | float  | 已获利息倍数(EBIT/利息费用) |
|  longdebt_to_workingcapital | float  | 长期债务与营运资金比率 |
|  ebitda_to_debt | float  | 息税折旧摊销前利润/负债合计 |
|  turn_days | float | 营业周期 |
|  roa_yearly | float | 年化总资产净利率 |
|  roa_dp | float | 总资产净利率(杜邦分析) |
|  fixed_assets | float | 固定资产合计 |
|  profit_prefin_exp | float  | 扣除财务费用前营业利润 |
|  non_op_profit | float  | 非营业利润 |
|  op_to_ebt | float  | 营业利润／利润总额 |
|  nop_to_ebt | float  | 非营业利润／利润总额 |
|  ocf_to_profit | float  | 经营活动产生的现金流量净额／营业利润 |
|  cash_to_liqdebt | float  | 货币资金／流动负债 |
|  cash_to_liqdebt_withinterest | float  | 货币资金／带息流动负债 |
|  op_to_liqdebt | float  | 营业利润／流动负债 |
|  op_to_debt | float  | 营业利润／负债合计 |
|  roic_yearly | float  | 年化投入资本回报率 |
|  total_fa_trun | float  | 固定资产合计周转率 |
|  profit_to_op | float | 利润总额／营业收入 |
|  q_opincome | float  | 经营活动单季度净收益 |
|  q_investincome | float  | 价值变动单季度净收益 |
|  q_dtprofit | float  | 扣除非经常损益后的单季度净利润 |
|  q_eps | float  | 每股收益(单季度) |
|  q_netprofit_margin | float  | 销售净利率(单季度) |
|  q_gsprofit_margin | float  | 销售毛利率(单季度) |
|  q_exp_to_sales | float  | 销售期间费用率(单季度) |
|  q_profit_to_gr | float  | 净利润／营业总收入(单季度) |
|  q_saleexp_to_gr | float | 销售费用／营业总收入 (单季度) |
|  q_adminexp_to_gr | float  | 管理费用／营业总收入 (单季度) |
|  q_finaexp_to_gr | float  | 财务费用／营业总收入 (单季度) |
|  q_impair_to_gr_ttm | float  | 资产减值损失／营业总收入(单季度) |
|  q_gc_to_gr | float | 营业总成本／营业总收入 (单季度) |
|  q_op_to_gr | float  | 营业利润／营业总收入(单季度) |
|  q_roe | float | 净资产收益率(单季度) |
|  q_dt_roe | float | 净资产单季度收益率(扣除非经常损益) |
|  q_npta | float | 总资产净利润(单季度) |
|  q_opincome_to_ebt | float  | 经营活动净收益／利润总额(单季度) |
|  q_investincome_to_ebt | float  | 价值变动净收益／利润总额(单季度) |
|  q_dtprofit_to_profit | float  | 扣除非经常损益后的净利润／净利润(单季度) |
|  q_salescash_to_or | float  | 销售商品提供劳务收到的现金／营业收入(单季度) |
|  q_ocf_to_sales | float | 经营活动产生的现金流量净额／营业收入(单季度) |
|  q_ocf_to_or | float  | 经营活动产生的现金流量净额／经营活动净收益(单季度) |
|  basic_eps_yoy | float | 基本每股收益同比增长率(%) |
|  dt_eps_yoy | float | 稀释每股收益同比增长率(%) |
|  cfps_yoy | float | 每股经营活动产生的现金流量净额同比增长率(%) |
|  op_yoy | float | 营业利润同比增长率(%) |
|  ebt_yoy | float | 利润总额同比增长率(%) |
|  netprofit_yoy | float | 归属母公司股东的净利润同比增长率(%) |
|  dt_netprofit_yoy | float | 归属母公司股东的净利润-扣除非经常损益同比增长率(%) |
|  ocf_yoy | float | 经营活动产生的现金流量净额同比增长率(%) |
|  roe_yoy | float | 净资产收益率(摊薄)同比增长率(%) |
|  bps_yoy | float | 每股净资产相对年初增长率(%) |
|  assets_yoy | float | 资产总计相对年初增长率(%) |
|  eqt_yoy | float | 归属母公司的股东权益相对年初增长率(%) |
|  tr_yoy | float | 营业总收入同比增长率(%) |
|  or_yoy | float | 营业收入同比增长率(%) |
|  q_gr_yoy | float  | 营业总收入同比增长率(%)(单季度) |
|  q_gr_qoq | float  | 营业总收入环比增长率(%)(单季度) |
|  q_sales_yoy | float | 营业收入同比增长率(%)(单季度) |
|  q_sales_qoq | float  | 营业收入环比增长率(%)(单季度) |
|  q_op_yoy | float  | 营业利润同比增长率(%)(单季度) |
|  q_op_qoq | float | 营业利润环比增长率(%)(单季度) |
|  q_profit_yoy | float  | 净利润同比增长率(%)(单季度) |
|  q_profit_qoq | float  | 净利润环比增长率(%)(单季度) |
|  q_netprofit_yoy | float  | 归属母公司股东的净利润同比增长率(%)(单季度) |
|  q_netprofit_qoq | float  | 归属母公司股东的净利润环比增长率(%)(单季度) |
|  equity_yoy | float | 净资产同比增长率 |
|  rd_exp | float  | 研发费用 |
|  update_flag | str  | 更新标识 |
|  # 因子讲解 |
|  - peTTM 市盈率TTM |
|  `市盈率TTM（Trailing Twelve Months）是指公司过去12个月的净收益（EPS）与当前股价的比率。简单来说，它是表示投资者每投资一元获得的收益。 |
|  例如，一个公司的市盈率TTM为10倍，意味着投资者需要支付10元才能获取1元的净收益，因此市盈率越高，需要支付的成本就越高。 |
|  市盈率TTM的计算可以帮助投资者评估股票的估值，如果一个公司的市盈率与同行业相比明显偏高，投资者可能会认为该股票已经过度估值，不值得投资；相反，如果市盈率较低，可能意味着该公司具有更好的投资价值。 |
|  总的来说，市盈率TTM是投资者评估公司价值、决定是否投资的重要指标之一。` |
|  - peLYR 市盈率LYR |
|  `市盈率LYR（Last Year Ratio）是指公司上一财年的净收益（EPS）与当前股价的比率。简单来说，它是表示投资者每投资一元获得的收益。` |
|  - pbMRQ 市净率MRQ |
|  `市净率MRQ（Most Recent Quarter）是指公司最近一个季度的每股净资产与当前股价的比率。简单来说，它是表示投资者每投资一元获得的净资产。` |
|  - psTTM 市销率TTM |
|  `市销率TTM（Trailing Twelve Months）是指公司过去12个月的营业收入与当前股价的比率。简单来说，它是表示投资者每投资一元获得的营业收入。` |
|  - pcfNCF 市现率NCF |
|  `市现率NCF（Net Cash Flow）是指公司过去12个月的现金流量净额与当前股价的比率。简单来说，它是表示投资者每投资一元获得的现金流量净额。` |
|  -转股溢价 |
|  `转股溢价（Convertible Premium）是指可转换债券或优先股转换为普通股时的转换价格高于当前市场上同一发行企业的股票价格。也就是说，在转换股票时，投资者需要以溢价的价格购买普通股票，而不是以市场价格购买。 |
|  例如，某公司发行了一种可转换优先股票，转换比率为10股优先股票可以转换为1股普通股票，转换价格为50美元，而当前股票市场上的同一公司的股票价格为40美元。在这种情况下，如果投资者选择转换他们所持有的10股优先股票，他们需要以高于市场价格的50美元购买一股普通股（而不是40美元），因此他们需要支付每股10美元的转股溢价。 |
|  转股溢价通常发生在市场价格下跌的情况下，因为那些持有可转换债券和优先股的投资者通常会将股票持有到转换时间（或转换后）再出售，这样会影响到普通股的供应量和需求量，进而推高转换价格。另一方面，当市场价格上涨时，转股溢价就会下降或消失。` |
|  -pb_pct |
|  `市价（Market Price）是指可交易金融资产（如股票、债券、基金等）在股票、债券或基金市场上实时的买卖价格。与股票的行情价格不同，市价是指股票在某一时刻可以正常成交的最新价格。当投资者下达买入或卖出订单时，交易执行的价格通常就是市价。市价不会被提前确定，而是在交易时实时根据买方和卖方的供需情况而产生。 |
|  账面价值（Book Value）是指一家公司根据其会计准则编制的财务报表中所披露的净资产的价值，也可以理解为公司拥有的所有净资产在会计上计算的价值总和。它是根据公司的账面价值资产和负债计算得出的，反映了公司的实际财务状况。 |
|  Price-to-Book Ratio = Market Price / Book Value |
|  PB越高，意味着股票相对于每股净资产的市场定价越高，可能意味着公司市场价值超过了其资产价值，也可能意味着市场存在一些高估情况。 |
|  PB_pct在股票的多因素分析中表示某只股票在所有股票中的PB值的排名百分比，即该股票的PB值在所有股票中处于百分之几的位置。常用于分析股票相对于市场的估值水平，以及对股票估值的实时监测。 |
|  ` |
|  - dt_netprofit_yoy |
|  ` |
|  DT_NetProfit_YOY是一个财务指标，全称为上市公司最近一季度(或最近12个月，根据具体情况而定)净利润同比增长率，是描述公司盈利情况的重要指标之一。 |
|  具体地，这个指标是指上市公司最近一个季度或最近12个月的净利润同比增长的百分比。这个指标的计算公式是： |
|  DT_NetProfit_YOY = (本期净利润- 上期净利润) / |上期净利润| * 100% |
|  其中，本期净利润和上期净利润是相邻两个季度或12个月的净利润数值，|上期净利润|是上期净利润的绝对值。 |
|  DT_NetProfit_YOY的变化可以反映公司营收增长情况、成本控制、经营效率、市场竞争等多方面的情况，是评估公司盈利能力和发展潜力的重要指标。` |
|  -价格动量