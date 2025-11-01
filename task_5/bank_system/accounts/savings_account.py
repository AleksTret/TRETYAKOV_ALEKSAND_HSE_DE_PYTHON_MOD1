"""
Сберегательный счет

Класс для сберегательных счетов с начислением процентов.
Включает ограничения на снятие средств и расчет процентов.
"""

from bank_system.accounts.base_account import Account


class SavingsAccount(Account):
    """Сберегательный счет с процентным начислением и ограничениями на снятие.

    Атрибуты:
        account_type (str): Тип счета ('savings')
    """

    account_type = "savings"

    def apply_interest(self, rate: float) -> None:
        """Начисляет проценты на остаток счета.

        Args:
            rate (float): Процентная ставка

        Raises:
            ValueError: Если процентная ставка не положительная
        """
        if rate <= 0:
            raise ValueError("Процентная ставка должна быть положительной")

        interest = self.balance * (rate / 100)

        if interest > 0:
            # Используем deposit с типом операции 'interest'
            self.deposit(interest, "interest")

    def withdraw(self, amount: float, op_type: str = "withdraw") -> None:
        """Снимает средства со сберегательного счета с ограничением.

        Не позволяет снять больше 50% от текущего баланса.

        Args:
            amount (float): Сумма для снятия
            op_type (str): Тип операции, по умолчанию 'withdraw'

        Raises:
            ValueError: Если сумма отрицательная или превышает лимит
        """
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        # Проверка лимита снятия (не более 50% от баланса)
        max_withdrawal = self.balance * 0.5
        if amount > max_withdrawal:
            raise ValueError(
                f"Нельзя снять более 50% от баланса. "
                f"Максимально доступно: {max_withdrawal:.2f}"
            )

        # Вызываем родительский метод снятия
        super().withdraw(amount, op_type)

    def load_operations(self, file_path: str) -> None:
        """Загружает историю операций из файла для сберегательного счета.

        Args:
            file_path (str): Путь к файлу с операциями

        Raises:
            ValueError: При ошибках загрузки или невалидных операциях
        """
        valid_operations = ["deposit", "withdraw", "interest"]
        self._load_operations(file_path, valid_operations)
