"""
Пакет сервисов банковской системы

Содержит сервисные классы для работы с данными:
- OperationHistory: управление историей операций счетов
"""

from .operation_history import OperationHistory

__all__ = ["OperationHistory"]
