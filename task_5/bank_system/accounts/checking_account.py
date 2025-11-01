"""
Расчетный счет

Класс для повседневных банковских операций.
"""

from bank_system.accounts.base_account import Account


class CheckingAccount(Account):
    """Расчетный счет для ежедневных банковских операций.

    Наследует все методы базового счета и добавляет
    специфичную валидацию для операций расчетного счета.

    Атрибуты:
        account_type (str): Тип счета ('checking')
    """

    account_type = "checking"

    def load_operations(self, file_path: str) -> None:
        """Загружает историю операций из файла для расчетного счета.

        Args:
            file_path (str): Путь к файлу с операциями

        Raises:
            ValueError: При ошибках загрузки или невалидных операциях
        """
        valid_operations = ["deposit", "withdraw"]
        self._load_operations(file_path, valid_operations)

    def get_account_info(self) -> dict:
        """Возвращает информацию о расчетном счете.

        Returns:
            dict: Словарь с информацией о счете
        """
        return {
            "account_type": self.account_type,
            "holder": self.holder,
            "account_number": self.account_number,
            "balance": self.balance,
        }
