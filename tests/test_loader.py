import sys
sys.path.insert(0, '.')

from main import ReportLoader
from base import BaseReport

def test_discover_finds_report(reports_dir):
    """Проверка, что загрузчик находит файл отчета"""
    report_file = reports_dir / "test_report.py"
    report_file.write_text("""
from base import BaseReport
class TestReport(BaseReport):
    def get_name(self): return "test"
    def generate(self, data): return []
""")
    
    loader = ReportLoader(reports_dir=str(reports_dir))
    loader.discover()
    
    assert "test" in loader.registry
    assert isinstance(loader.registry["test"], BaseReport)

def test_discover_ignores_invalid(capsys, reports_dir):
    """Проверка, что битые файлы не ломают систему"""
    bad_file = reports_dir / "bad.py"
    bad_file.write_text("class Bad: pass")
    
    loader = ReportLoader(reports_dir=str(reports_dir))
    loader.discover()
    
    assert "bad" not in loader.registry