import argparse
import csv
import importlib
import importlib.util
import inspect
from pathlib import Path
import sys
from tabulate import tabulate

from base import BaseReport

class ReportLoader:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = Path(reports_dir)
        self.registry = {}

    def discover(self):
        for file_path in self.reports_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
            
            module_name = file_path.stem
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                
                root_dir = str(Path(__file__).parent)
                sys.path.insert(0, root_dir)
                
                spec.loader.exec_module(module)
                
                sys.path.pop(0)
                
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseReport) and obj is not BaseReport:
                        instance = obj()
                        self.registry[instance.get_name()] = instance
                        
            except Exception as e:
                print(f"[ERROR] Не удалось загрузить {file_path.name}: {e}")

    def run_report(self, name, data):
        if name in self.registry:
            report_data = self.registry[name].generate(data)
            if report_data:
                print(tabulate(
                    report_data, 
                    tablefmt="psql", 
                    floatfmt=".2f", 
                    headers="keys"
                ))
            else:
                print("Нет данных для отображения.")
        else:
            print(f"Отчет '{name}' не найден.")

def read_files(files):
    for file in files:
        file_path = Path(file)
        if not file_path.is_file():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    file_content = []

    for file in files:
        with open(file, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            file_content += list(csv_reader)
            
    return file_content

if __name__ == "__main__":
    loader = ReportLoader()
    loader.discover()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str, nargs="+", help='Files for which reports will be created')
    parser.add_argument('--report', type=str, help='Name for the report')
    args = parser.parse_args()
    
    file_content = read_files(args.files)
    
    loader.run_report(args.report, file_content)