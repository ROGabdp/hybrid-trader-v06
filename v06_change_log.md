# v06 重點

1. 移除 LSTM 特徵 (由35個特徵，降至31 個特徵)
2. 強制 CPU 訓練 (在train_v5_models.py中)

# 針對v5模型，搭配了牛熊MA120濾網，更新了回測腳本和每日運營腳本:

    * 盤後
    python backtest_v5_dca_hybrid_dynamic_filter_fixed_lstm.py --start 2025-12-09
    python daily_ops_v5_dynamic_filter_fixed_lstm.py   
    * 盤中
    python daily_ops_v5_intraday_dynamic_filter_fixed_lstm.py -i

