"""
Банковская система

Система управления банковскими операциями.
Включает управление счетами и операциями.
Анализ операций и визуализацию истории операций.
Поддерживает импорт данных из внешних файлов.

Основные модули:
- accounts: Счета (базовые, сберегательные, расчетные)
- visualization: Построение графиков и анализ транзакций
- services: История операций и импорт данных
- utils: Вспомогательные функции
"""

from .accounts import Account, CheckingAccount, SavingsAccount
from .visualization import AccountVisualizer, TransactionAnalyzer
from .utils import validate_holder_name, validate_account_number, parse_date

__all__ = [
    # Accounts
    "Account",
    "CheckingAccount",
    "SavingsAccount",
    # Visualization
    "AccountVisualizer",
    "TransactionAnalyzer",
    # Utils
    "validate_holder_name",
    "validate_account_number",
    "parse_date",
]
