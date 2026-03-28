from fastapi import FastAPI
import pandas as pd

app = FastAPI()

cluster_df = pd.read_csv("cluster_assignments.csv", index_col=0)
#print(cluster_df.columns)

cluster_map = {}

cluster_encoding = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

for entity_id_raw, row in cluster_df.iterrows():
    key = str(entity_id_raw).strip().upper()
    cluster_map[key] = cluster_encoding[row["cluster"].strip()]

cluster_names = {0: "Low", 1: "Medium", 2: "High"}

def load_forecast(cluster):
    if cluster == 0:
        file = "sarimax_output/Low_forecast_results.csv"
    elif cluster == 1:
        file = "sarimax_output/Medium_forecast_results.csv"
    else:
        file = "sarimax_output/High_forecast_results.csv"

    df = pd.read_csv(file, index_col=0)
    df.index = pd.to_datetime(df.index)

    return df

@app.post("/forecast")
def get_forecast(data: dict):
    entity_id = str(data.get("entity_id")).strip().upper()

    cluster = cluster_map.get(entity_id)  

    if cluster is None:
        return {"error": f"Unknown entity_id: {entity_id}"}

    df = load_forecast(cluster)

    return {
        "entity_id": entity_id,
        "cluster": cluster,
        "cluster_name": cluster_names[cluster],
        "forecast": df["forecast"].tolist()[:5],
        "lower_95": df["lower_95"].tolist()[:5],
        "upper_95": df["upper_95"].tolist()[:5],
        "datetime": df.index.astype(str).tolist()[:5]
    }