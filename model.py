import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_revenue():
    df = pd.read_csv("data/sales_data.csv")

    # Convert date to numeric index
    df["DayIndex"] = np.arange(len(df))

    X = df[["DayIndex"]]
    y = df["Revenue"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 7 days
    future_days = np.arange(len(df), len(df) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)

    forecast_df = pd.DataFrame({
        "DayIndex": future_days.flatten(),
        "Revenue": predictions,
        "Type": "Forecast"
    })

    df["Type"] = "Actual"

    combined = pd.concat([df[["DayIndex", "Revenue", "Type"]], forecast_df])

    return combined
