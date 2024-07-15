from project_code.project_dataloader import load_data

data_filepath = (
    "https://raw.githubusercontent.com/Dakini/MLops_project/local/data/diabetes.csv"
)


def test_dataloader():
    df = load_data(data_filepath)

    assert len(df) == 768
