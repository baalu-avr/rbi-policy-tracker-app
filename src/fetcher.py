import pandas as pd

def load_rbi_data(filepath="data/rates.xlsx"):
    """
    Loads and cleans RBI monetary policy rates from the official RBI Excel file.
    Returns a clean DataFrame with Date and Repo Rate columns.
    """

    # Read raw Excel, skipping the messy header rows
    df = pd.read_excel(filepath, header=None, skiprows=8)

    # Assign column names based on RBI file structure
    df.columns = [
        "drop", "date", "bank_rate", "repo_rate",
        "reverse_repo", "sdf_rate", "msf_rate", "crr", "slr"
    ]

    # Drop the useless first column
    df = df.drop(columns=["drop"])

    # Drop rows where date is missing or not a real date
    df = df[pd.to_datetime(df["date"], errors="coerce").notna()]

    # Convert date column properly
    df["date"] = pd.to_datetime(df["date"])

    # Replace "-" strings with NaN
    df = df.replace("-", pd.NA)

    # Convert rate columns to numeric
    rate_cols = ["bank_rate", "repo_rate", "reverse_repo", "sdf_rate", "msf_rate"]
    for col in rate_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort by date ascending
    df = df.sort_values("date").reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = load_rbi_data()
    print(f"Loaded {len(df)} records")
    print(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print("\nLatest 5 policy changes:")
    print(df[["date", "repo_rate", "reverse_repo", "bank_rate"]].dropna(subset=["repo_rate"]).tail())