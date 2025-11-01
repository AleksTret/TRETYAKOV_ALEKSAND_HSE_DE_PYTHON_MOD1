"""
Вспомогательные утилиты

Набор функций для валидации данных и работы с датами.
Используется во всех модулях банковской системы
для проверки корректности данных.
"""

import re
from datetime import datetime
from typing import Optional


def validate_holder_name(name: str) -> None:
    """Валидация имени владельца счета"""
    pattern = r"^[A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+$"
    if not re.match(pattern, name):
        raise ValueError(
            "Имя владельца должно быть в формате "
            + "'Имя Фамилия' с заглавных букв, "
            + "кириллицей или латиницей"
        )


def validate_account_number(account_number: str) -> None:
    """Валидация кастомного номера счета"""
    # Проверяем формат
    if not account_number.startswith("ACC-"):
        raise ValueError("Номер счета должен начинаться с 'ACC-'")

    # Проверяем числовую часть
    try:
        int(account_number[4:])
    except ValueError as exc:
        raise ValueError("Некорректный формат номера счета") from exc


def parse_date(date_str: str) -> Optional[datetime]:
    """Парсинг даты из разных форматов"""
    try:
        date_str = str(date_str).strip()

        formats = [
            "%Y-%m-%d %H:%M:%S",  # 2025-09-27 22:17:26
            "%d/%m/%Y %H:%M",  # 28/09/2025 22:17
            "%Y-%m-%d %H:%M",  # 2025-09-27 22:17
            "%d.%m.%Y %H:%M:%S",  # 28.09.2025 22:17:26
            "%d-%m-%Y %H:%M:%S",  # 28-09-2025 22:17:26
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None
    except (ValueError, TypeError, AttributeError):
        return None
