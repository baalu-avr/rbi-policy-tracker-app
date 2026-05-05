from src.fetcher import load_rbi_data
from src.visualizer import plot_repo_rate, plot_rate_comparison

def main():
    print("=" * 50)
    print("   RBI Monetary Policy Tracker")
    print("=" * 50)

    # Load data
    print("\n📥 Loading RBI data...")
    df = load_rbi_data()
    print(f"✅ Loaded {len(df)} records")
    print(f"📅 Date range: {df['date'].min().date()} → {df['date'].max().date()}")

    # Latest rate
    latest = df.dropna(subset=["repo_rate"]).iloc[-1]
    print(f"\n🏦 Current Repo Rate: {latest['repo_rate']}%")
    print(f"📆 Last changed: {latest['date'].date()}")

    # Generate charts
    print("\n📊 Generating charts...")
    plot_repo_rate(df)
    plot_rate_comparison(df)
    print("\n✅ Done! Charts saved to output/charts/")

if __name__ == "__main__":
    main()