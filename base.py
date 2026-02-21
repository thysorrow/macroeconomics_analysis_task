from abc import ABC, abstractmethod

class BaseReport(ABC):
    @abstractmethod
    def get_name(self):
        """Возвращает имя отчета для пользователя"""
        pass

    @abstractmethod
    def generate(self, data):
        """Основная логика генерации отчета"""
        pass