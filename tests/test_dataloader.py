from project_code.project_dataloader import load_data

data_filepath = "data/spotify_data.csv"


def test_dataloader():
    df = load_data(data_filepath)

    assert len(df) == 1159764
