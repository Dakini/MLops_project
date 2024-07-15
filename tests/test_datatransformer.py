from project_code.project_dataloader import load_data
from project_code.project_transformer import return_cols


data_filepath = (
    "https://raw.githubusercontent.com/Dakini/MLops_project/local/data/diabetes.csv"
)


def test_return_cols():
    df = load_data(data_filepath)
    cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness"]
    df = return_cols(df, cols)
    assert len(df.columns) == len(cols)
