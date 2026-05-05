import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os

def plot_repo_rate(df, save=True):
    """
    Plots RBI Repo Rate history over time.
    """

    # Filter only rows where repo_rate exists
    df_repo = df.dropna(subset=["repo_rate"]).copy()

    # Focus on post-2000 data — more relevant for modern analysis
    df_repo = df_repo[df_repo["date"] >= "2000-01-01"]

    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot the repo rate as a step chart (rates don't change continuously)
    ax.step(df_repo["date"], df_repo["repo_rate"],
            where="post", color="#E63946", linewidth=2, label="Repo Rate")

    # Fill under the line for visual impact
    ax.fill_between(df_repo["date"], df_repo["repo_rate"],
                    step="post", alpha=0.15, color="#E63946")

    # Annotate the latest rate
    latest = df_repo.iloc[-1]
    ax.annotate(
        f'Current: {latest["repo_rate"]}%',
        xy=(latest["date"], latest["repo_rate"]),
        xytext=(10, 10), textcoords="offset points",
        fontsize=11, fontweight="bold", color="#E63946"
    )

    # Formatting
    ax.set_title("RBI Monetary Policy — Repo Rate History (2000–2025)",
                 fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Repo Rate (%)", fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    plt.xticks(rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(fontsize=11)

    # Add source credit
    fig.text(0.99, 0.01, "Source: Reserve Bank of India (RBI)",
             ha="right", fontsize=9, color="gray")

    plt.tight_layout()

    # Save to output folder
    if save:
        os.makedirs("output/charts", exist_ok=True)
        filepath = "output/charts/repo_rate_history.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {filepath}")

    plt.show()


def plot_rate_comparison(df, save=True):
    """
    Plots Repo Rate vs Bank Rate comparison.
    """

    df_plot = df[df["date"] >= "2000-01-01"].copy()

    fig, ax = plt.subplots(figsize=(14, 6))

    for col, color, label in [
        ("repo_rate", "#E63946", "Repo Rate"),
        ("bank_rate", "#457B9D", "Bank Rate"),
    ]:
        data = df_plot.dropna(subset=[col])
        ax.step(data["date"], data[col], where="post",
                color=color, linewidth=2, label=label)

    ax.set_title("RBI Key Policy Rates Comparison (2000–2025)",
                 fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Rate (%)", fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    plt.xticks(rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(fontsize=11)

    fig.text(0.99, 0.01, "Source: Reserve Bank of India (RBI)",
             ha="right", fontsize=9, color="gray")

    plt.tight_layout()

    if save:
        os.makedirs("output/charts", exist_ok=True)
        filepath = "output/charts/rate_comparison.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {filepath}")

    plt.show()


if __name__ == "__main__":
    from fetcher import load_rbi_data

    df = load_rbi_data()
    print("Generating charts...")
    plot_repo_rate(df)
    plot_rate_comparison(df)
    print("Done! Check output/charts/ folder.")