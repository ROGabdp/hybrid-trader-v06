import pandas as pd
import sys

def analyze_backtest(file_path):
    # Redirect output to file
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f
        
        print(f"Reading {file_path}")
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # Filter for rows where status is 'holding' or we have sell_conf (sell agent only runs when holding)
        sell_df = df[df['sell_conf'].notna()].copy()
        
        if sell_df.empty:
            print("No rows with sell_conf found.")
            return

        print(f"\nTotal rows with Sell Confidence: {len(sell_df)}")
        
        print("\n--- Sell Confidence Statistics ---")
        print(sell_df['sell_conf'].describe())
        
        print("\n--- Sell Action Counts ---")
        if 'sell_action' in sell_df.columns:
            print(sell_df['sell_action'].value_counts())
        else:
            print("sell_action column missing")

        # Check thresholds
        thresholds = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
        print("\n--- Potential Threshold Analysis ---")
        for t in thresholds:
            count = len(sell_df[sell_df['sell_conf'] >= t])
            pct = (count / len(sell_df)) * 100
            print(f"Sell Confidence >= {t}: {count} rows ({pct:.2f}%)")

        # High confidence examples
        print("\n--- Top 10 Highest Confidence Rows ---")
        top_10 = sell_df.nlargest(10, 'sell_conf')
        print(top_10[['date', 'price', 'sell_conf', 'sell_action', 'current_return']])

        # Check low confidence examples just in case
        print("\n--- Top 5 Lowest Confidence Rows ---")
        bottom_5 = sell_df.nsmallest(5, 'sell_conf')
        print(bottom_5[['date', 'price', 'sell_conf', 'sell_action', 'current_return']])

if __name__ == "__main__":
    file_path = "results_backtest_v5_no_filter/daily_confidence_v5_20230103_20260102.csv"
    analyze_backtest(file_path)
