from project_code.project_dataloader import load_data
from project_code.project_transformer import (
    return_year_data,
    remove_score,
    create_verdict,
    apply_genre_label,
)


data_filepath = "data/spotify_data.csv"


def get_data():
    return load_data(data_filepath)


def test_genre_label():
    df = load_data(data_filepath)
    df = apply_genre_label(df)
    assert df["genre_label"].nunique() == 82


def test_remove_score_and_get_year():
    df = load_data(data_filepath)
    year = 2018
    df = remove_score(df, 0)
    df = return_year_data(df, year)
    assert len(df) == 52529


def test_create_verdict():
    df = load_data(data_filepath)
    df = create_verdict(df)
    assert df["verdict"].nunique() == 2


def test_remove_score():
    df = load_data(data_filepath)
    df = remove_score(df, 0)

    assert len(df) == 1001373


def test_return_year_data():
    # test the remove the year data
    # check for year 2018
    df = load_data(data_filepath)
    year = 2018
    df = return_year_data(df, year)

    assert len(df) == 56572
