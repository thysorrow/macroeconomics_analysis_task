import sys
sys.path.insert(0, '.')

from main import read_files, ReportLoader
from reports.average_gdp import AverageGDP

def test_read_files(csv_file):
    """Проверка чтения CSV"""
    data = read_files([csv_file])
    assert len(data) == 2
    assert data[0]['country'] == 'USA'

def test_read_files_not_found():
    """Проверка обработки несуществующего файла"""
    try:
        read_files(["nonexistent.csv"])
        assert False, "Должно было возникнуть исключение"
    except FileNotFoundError:
        pass

def test_run_report_output(capsys):
    """Проверка вывода в консоль"""
    loader = ReportLoader()
    loader.registry["average-gdp"] = AverageGDP()
    
    data = [{'country': 'USA', 'gdp': '1000'}]
    loader.run_report("average-gdp", data)
    
    captured = capsys.readouterr()
    assert "USA" in captured.out
    assert "1000" in captured.out

def test_run_report_not_found(capsys):
    """Проверка сообщения об отсутствии отчета"""
    loader = ReportLoader()
    loader.run_report("nonexistent", [])
    
    captured = capsys.readouterr()
    assert "не найден" in captured.out