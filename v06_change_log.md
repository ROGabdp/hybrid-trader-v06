# v06 重點

1. 移除 LSTM 特徵 (由35個特徵，降至31 個特徵)
2. 強制 CPU 訓練 (在train_v5_models.py中)
3. 調整sell agent的學習目標
4. 調整訓練和驗證的超參數設定，讓評估更穩定，且最終選出的模型會更有代表性。

# 針對v5模型，搭配了牛熊MA120濾網，更新了回測腳本和每日運營腳本:

    * 盤後
    python backtest_v5_dca_hybrid_dynamic_filter_fixed_lstm.py --start 2025-12-09
    python daily_ops_v5_dynamic_filter_fixed_lstm.py   
    * 盤中
    python daily_ops_v5_intraday_dynamic_filter_fixed_lstm.py -i

# 移除LSTM之後，sell agent的賣出判斷變差，因此我們對sell agent的學習目標進行調整。

完成 ptrl_hybrid_system.py 中 SellEnvHybrid 的修改：

變更摘要：

1. 隨機化 Episode 長度：reset() 時隨機選擇 60~250 天作為本回合結束點。
2. 解耦獎勵視窗 (Lookahead)：無論在哪一天結算，系統都會往後看固定 60 天來計算「錯過高點」及「躲過大跌」的獎勵/懲罰。即使被隨機踢出局，也無法免於被評價後續走勢。
3. 資料切片擴大：每個 Episode 的資料從 120 天增加到 310 天，以容納最長 250 天的 Episode 加上 60 天的 Lookahead。
4. 核心獎勵公式（基礎報酬、錯失高點懲罰、躲過大跌獎勵）維持不變，只修改了計算所用的時間視窗。

# evl 時不知道為什麼，一開始分數都會飆高，導致雖然跑了 1M steps，但最後存下來的model 卻是前面沒跑幾步的模型。 

調整 train_v5_models.py 的參數，讓評估更穩定，且最終選出的模型會更有代表性。

1. 增加評估回數 (n_eval_episodes)：
從 30 改為 100。
更多的樣本數能消除運氣成分，只有「真的強」的模型才能在 100 次測試中拿下高分。
2. 增加熵係數 (ent_coef)：
Fine-tune 目前是 0.005，建議改回 0.01（與 Pre-train 相同）。
TensorBoard 顯示 entropy 下降很快（Agent 太快變自信）。提高這個係數可以強迫 Agent 保持「好奇心」，不要太早鎖死在「死抱不賣」這個局部最佳解。
3. 降低學習率 (learning_rate)：
目前是 1e-5，可以降為 5e-6。讓 Fine-tune 的步伐更慢、更穩，避免破壞 Pre-train 學到的知識，也能減少訓練過程的震盪。