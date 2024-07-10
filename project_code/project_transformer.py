import pandas as pd


def create_verdict(df: pd.DataFrame, threshold=50):
    df["verdict"] = df["popularity"].apply(
        lambda x: "low" if x < threshold else "popular"
    )
    return df


def create_stoi(values) -> dict:
    stoi = {v: k for k, v in enumerate(values)}

    return stoi


def return_year_data(df: pd.DataFrame, year: int = None) -> pd.DataFrame:
    # return data for a specific year
    if year:
        return df[df["year"] == year]
    return df


def remove_score(df: pd.DataFrame, score=None) -> pd.DataFrame:
    if score is not None:
        return df[df["popularity"] != score]
    return df


def apply_genre_label(df: pd.DataFrame) -> pd.DataFrame:
    # convert data from string to int
    # i.e. metal to 1
    stoi = create_stoi(df["genre"])
    df["genre_label"] = df["genre"].apply(lambda x: stoi[x])
    return df
