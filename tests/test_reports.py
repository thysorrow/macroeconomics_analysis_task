import sys
sys.path.insert(0, '.')

from reports.average_gdp import AverageGDP
from base import BaseReport

def test_average_gdp_inherits_base():
    """Проверка, что отчет наследуется от BaseReport"""
    report = AverageGDP()
    assert isinstance(report, BaseReport)

def test_average_gdp_name():
    """Проверка имени отчета"""
    report = AverageGDP()
    assert report.get_name() == "average-gdp"

def test_average_gdp_calculation(sample_csv_data):
    """Проверка логики расчета среднего GDP"""
    report = AverageGDP()
    result = report.generate(sample_csv_data)
    
    assert isinstance(result, list)
    assert len(result) == 2
    
    usa_data = next(item for item in result if item['country'] == 'USA')
    assert usa_data['gdp'] == 900.0
    
    assert result[0]['country'] == 'USA'

def test_average_gdp_empty_data():
    """Проверка работы с пустыми данными"""
    report = AverageGDP()
    result = report.generate([])
    assert result == []