import json

import pandas as pd
import requests
from pandas import json_normalize


def get_data(url: str) -> dict:
    response = requests.get(url)
    data = response.text
    json_data: dict = json.loads(data)
    return json_data


def data_to_df(json_data: dict):
    results: list[dict] = json_data["results"]

    df = json_normalize(results)
    df["name"] = df["name.first"] + " " + df["name.last"]

    final_df = df[["name", "email", "gender"]]

    return final_df


def df_to_csv(df: pd.DataFrame):
    df.to_csv("male_user_data.csv", index=False)


if __name__ == "__main__":
    url = "https://randomuser.me/api/?gender=male&results=100"
    data = get_data(url)
    df = data_to_df(data)
    df_to_csv(df)
