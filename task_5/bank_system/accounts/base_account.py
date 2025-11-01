"""
Базовый класс счета

Абстрактный класс для всех типов банковских счетов.
Определяет общие методы и свойства для работы со счетами.
"""

from datetime import datetime
from typing import Optional, List

from bank_system.services import OperationHistory
from bank_system.utils import validate_holder_name, validate_account_number
import pandas as pd


class Account:
    """Базовый класс банковского счета.

    Атрибуты:
        account_holder (str): Владелец счета
        balance (Decimal): Текущий баланс
        account_number (str): Номер счета
        status (str): Статус счета
        transaction_history (list): История операций
    """

    __slots__ = (
        "_holder",
        "_balance",
        "_account_number",
        "_operation_history"
    )

    _account_counter = 999
    _used_account_numbers = set()

    def __init__(
        self,
        account_holder: str,
        balance: float = 0,
        account_number: Optional[str] = None,
    ):
        """
        Создание счета

        Args:
            account_holder: Владелец счета
            balance: Начальный баланс
            account_number: Опциональный номер счета (формат ACC-xxxx)
                          Если не указан - генерируется автоматически
        """

        # Инициализируем атрибуты перед использованием сеттеров
        self._holder = None
        self._balance = None
        self._account_number = None
        self._operation_history = None

        if account_number:
            # Если передана строка, например "ACC-10001". Проверка в setter
            self.account_number = account_number
        else:
            self.account_number = (
                Account.get_account_counter()
            )  # Генерируем, если не передано. Проверка в setter

        self.holder = account_holder  # Проверка в setter
        self.balance = balance  # Проверка в setter
        self.operation_history = OperationHistory()  # Проверка в setter

    @classmethod
    def get_account_counter(cls) -> int:
        """Генерирует уникальный номер счета.

        Returns:
            str: Сгенерированный номер счета
        """
        cls._account_counter += 1
        return cls._account_counter

    @property
    def holder(self) -> str:
        """Возвращает владельца счета.

        Returns:
            str: Имя владельца счета
        """
        return self._holder

    @holder.setter
    def holder(self, value: str) -> None:
        """Устанавливает владельца счета.

        Args:
            value (str): Имя владельца

        Raises:
            AttributeError: При попытке изменить существующего владельца
            ValueError: При невалидном имени владельца
        """
        if hasattr(self, "_holder") and self._holder is not None:
            raise AttributeError("Изменение владельца счета невозможно")
        validate_holder_name(value)
        self._holder = value

    @property
    def account_number(self) -> str:
        """Возвращает номер счета.

        Returns:
            str: Номер счета
        """
        return self._account_number

    @account_number.setter
    def account_number(self, value) -> None:
        """Устанавливает номер счета.

        Args:
            value: Номер счета (str или int)

        Raises:
            AttributeError: При попытке изменить существующий номер
            ValueError: При невалидном номере или дубликате
        """
        if (hasattr(self, "_account_number")
                and self._account_number is not None):
            raise AttributeError("Изменение номера счета невозможно")

        new_account_number = ""

        if isinstance(value, int):
            # Для сгенерированных номеров
            new_account_number = f"ACC-{value}"
        elif isinstance(value, str):
            # Для кастомных номеров
            validate_account_number(value)
            new_account_number = value
        else:
            raise ValueError("Некорректный тип номера счета")

        # Проверяем, что номер не занят
        if new_account_number in Account._used_account_numbers:
            raise ValueError(
                f"Номер счета {new_account_number} уже используется"
            )

        # Добавляем номер в использованные
        Account._used_account_numbers.add(new_account_number)

        # Устанавливаем номер для экземпляра класса
        self._account_number = new_account_number

    @property
    def balance(self) -> float:
        """Возвращает текущий баланс.

        Returns:
            float: Текущий баланс счета
        """
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        """Устанавливает баланс счета.

        Args:
            value (float): Новое значение баланса

        Raises:
            ValueError: При отрицательном балансе
        """
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = value

    def get_balance(self) -> float:
        """Возвращает текущий баланс счета.
            Метод излишен, при наличии @property balance, но нужен по заданию
        Returns:
            float: Текущий баланс
        """

        return self.balance

    @property
    def operation_history(self) -> "OperationHistory":
        """Возвращает историю операций.

        Returns:
            OperationHistory: Объект истории операций
        """
        return self._operation_history

    @operation_history.setter
    def operation_history(self, value: "OperationHistory") -> None:
        """Устанавливает историю операций.

        Args:
            value (OperationHistory): Объект истории операций
        """
        self._operation_history = value

    def get_history(self) -> pd.DataFrame:
        """Возвращает историю операций по счету.

        Returns:
            pd.DataFrame: DataFrame с историей операций
        """
        return self.operation_history.get_all_operations()

    def deposit(self, amount: float, op_type: str = "deposit") -> None:
        """Пополняет счет на указанную сумму.

        Args:
            amount (float): Сумма для пополнения
            op_type (str): Тип операции, по умолчанию 'deposit'

        Raises:
            ValueError: Если сумма отрицательная
        """

        def deposit_operation(amt):
            self.balance = self.balance + amt

        self._execute_operation(op_type, amount, deposit_operation)

    def withdraw(self, amount: float, op_type: str = "withdraw") -> None:
        """Снимает средства со счета.

        Args:
            amount (float): Сумма для снятия
            op_type (str): Тип операции, по умолчанию 'withdraw'

        Raises:
            ValueError: Если сумма отрицательная или недостаточно средств
        """

        def withdraw_operation(amt):
            self.balance = self.balance - amt

        self._execute_operation(op_type, amount, withdraw_operation)

    def _execute_operation(
        self,
        op_type: str,
        amount: float,
        operation_func
    ) -> None:
        """Общий метод для выполнения операций со счетом.

        Args:
            op_type (str): Тип операции
            amount (float): Сумма операции
            operation_func: Функция выполнения операции

        Raises:
            ValueError: При ошибках выполнения операции
        """
        try:
            if amount <= 0:
                raise ValueError(f"Сумма {op_type} должна быть положительной")

            # Выполняем операцию (пополнение или снятие)
            operation_func(amount)

            # Фиксируем успешную операцию в истории
            status = "success"

        except (ValueError, AttributeError) as e:
            # Ловим исключение от проверки суммы или от сеттера баланса
            status = "fail"

            # Уточняем сообщение об ошибке для снятия средств
            if op_type == "withdraw" and "баланс" in str(e).lower():
                raise ValueError("Недостаточно средств на счете") from e

            raise e

        finally:
            # Всегда добавляем операцию в историю (и при успехе, и при ошибке)
            self.operation_history.add_operation(
                op_type=op_type,
                amount=amount,
                timestamp=datetime.now(),
                balance_after=self.balance,
                status=status,
            )

    def _load_operations(
        self,
        file_path: str,
        valid_operations: List[str]
    ) -> None:
        """Загружает историю операций из файла.

        Args:
            file_path (str): Путь к файлу с операциями
            valid_operations (List[str]): Список допустимых операций
        """
        final_balance = self.operation_history.import_operations(
            file_path, self.account_number, valid_operations
        )

        # Обновляем баланс
        self.balance = final_balance
