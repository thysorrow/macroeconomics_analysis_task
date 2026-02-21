import pytest

@pytest.fixture
def sample_csv_data():
    """Тестовые данные"""
    return [
        {'country': 'USA', 'year': '2023', 'gdp': '1000', 'gdp_growth': '2.0'},
        {'country': 'USA', 'year': '2022', 'gdp': '800', 'gdp_growth': '1.5'},
        {'country': 'China', 'year': '2023', 'gdp': '500', 'gdp_growth': '5.0'},
    ]

@pytest.fixture
def reports_dir(tmp_path):
    """Создает временную папку reports для тестов"""
    folder = tmp_path / "reports"
    folder.mkdir()
    (folder / "__init__.py").write_text("")
    return folder

@pytest.fixture
def csv_file(tmp_path):
    """Создает временный CSV файл"""
    file = tmp_path / "test.csv"
    file.write_text("country,year,gdp\nUSA,2023,1000\nUSA,2022,800\n")
    return str(file)