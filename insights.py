import pandas as pd

def generate_insights():
    df = pd.read_csv("data/sales_data.csv")

    avg_revenue = df["Revenue"].mean()
    best_day = df.loc[df["Revenue"].idxmax()]
    worst_day = df.loc[df["Revenue"].idxmin()]

    return {
        "avg_revenue": round(avg_revenue, 2),
        "best_day": best_day["Date"],
        "worst_day": worst_day["Date"]
    }
