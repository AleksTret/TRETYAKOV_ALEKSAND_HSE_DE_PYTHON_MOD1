"""
История операций

Класс для управления историей банковских операций.
Обеспечивает запись, загрузку и очистку финансовых транзакций.
Поддерживает импорт из CSV и JSON файлов.
"""

import json
from datetime import datetime
from typing import List

from bank_system.utils import parse_date
import pandas as pd


class OperationHistory:
    """Управление историей операций банковского счета."""

    def __init__(self):
        # Создаем пустой DataFrame с явно указанными типами
        self._df = pd.DataFrame(
            {
                "op_type": pd.Series(dtype="object"),
                "amount": pd.Series(dtype="float64"),
                "timestamp": pd.Series(dtype="datetime64[ns]"),
                "balance_after": pd.Series(dtype="float64"),
                "status": pd.Series(dtype="object"),
            }
        )

    # def add_operation(
    #     self,
    #     op_type: str,
    #     amount: float,
    #     timestamp: Optional[datetime],
    #     balance_after: float,
    #     status: str,
    # )-> None:
    #     """Добавляет операцию в историю.

    #     Args:
    #         op_type: Тип операции (deposit/withdraw/interest)
    #         amount: Сумма операции
    #         timestamp: Время операции, по умолчанию текущее время
    #         balance_after: Баланс после операции
    #         status: Статус операции, по умолчанию 'success'
    #     """
    #     timestamp = timestamp or datetime.now()

    #     # Добавляем строку через loc
    #     new_index = len(self._df)
    #     self._df.loc[new_index] = [
    #         op_type,
    #         amount,
    #         timestamp,
    #         balance_after,
    #         status
    #     ]

    def add_operation(self, **kwargs) -> None:
        """Добавляет операцию в историю.

        Args:
            **kwargs: Параметры операции:
                - op_type: Тип операции (deposit/withdraw/interest)
                - amount: Сумма операции
                - timestamp: Время операции, по умолчанию текущее время
                - balance_after: Баланс после операции, по умолчанию 0
                - status: Статус операции, по умолчанию 'success'
        """
        op_type = kwargs.get("op_type")
        amount = kwargs.get("amount", 0)
        timestamp = kwargs.get("timestamp") or datetime.now()
        balance_after = kwargs.get("balance_after", 0)
        status = kwargs.get("status", "success")

        # Добавляем строку через loc
        new_index = len(self._df)
        self._df.loc[new_index] = [
            op_type,
            amount,
            timestamp,
            balance_after,
            status
        ]

    def get_all_operations(self) -> pd.DataFrame:
        """Возвращает все операции отсортированные по времени.

        Returns:
            pd.DataFrame: DataFrame с историей операций
        """
        return self._df.copy().sort_values("timestamp")

    def load_history_from_file(
        self, file_path: str, account_number: str, valid_operations: List[str]
    ) -> pd.DataFrame:
        """Загрузка истории операций из файла с фильтрацией и очисткой

        Returns:
            pd.DataFrame: DataFrame с историей операций
        """
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".json"):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                raise ValueError("Поддерживаются только CSV и JSON файлы")

            # Фильтруем операции только для этого счета
            account_ops = df[df["account_number"] == account_number].copy()

            # Очищаем данные
            cleaned_ops = self.clean_history(account_ops, valid_operations)

            return cleaned_ops

        except Exception as e:
            raise ValueError(f"Ошибка загрузки файла: {e}") from e

    def clean_history(
        self, operations_df: pd.DataFrame, valid_operations: List[str]
    ) -> pd.DataFrame:
        """Очистка истории операций от ошибок

        Returns:
            pd.DataFrame: DataFrame с историей операций
        """
        if operations_df.empty:
            return operations_df

        df = operations_df.copy()

        # Конвертируем типы данных
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["balance_after"] = pd.to_numeric(
            df["balance_after"],
            errors="coerce"
        )

        # Удаляем строки с пропущенными значениями
        df = df.dropna(
            subset=["operation", "amount", "balance_after", "status"]
        )

        # Нормализуем названия операций
        operation_mapping = {
            "deposit": "deposit",
            "diposit": "deposit",
            "withdraw": "withdraw",
            "withtraw": "withdraw",
            "interest": "interest",
        }

        # нормализация названий операций
        def safe_normalize(op_name):
            if not isinstance(op_name, str):
                return op_name
            return operation_mapping.get(op_name.lower(), op_name)

        df["operation"] = df["operation"].apply(safe_normalize)

        # Проверяем корректность операций
        df = df[df["operation"].isin(valid_operations)]

        # Проверяем, что amount положительный
        df = df[df["amount"] > 0]

        # Проверяем корректность статуса
        def safe_status_check(status):
            if not isinstance(status, str):
                return False
            return "success" in status.lower()

        df = df[df["status"].apply(safe_status_check)]

        # Проверяем корректность дат
        valid_ops = []
        for _, op in df.iterrows():
            parsed_date = parse_date(op["date"])
            if parsed_date:
                valid_op = op.copy()
                valid_op["date"] = parsed_date
                valid_ops.append(valid_op)

        return pd.DataFrame(valid_ops)

    def import_operations(
        self, file_path: str, account_number: str, valid_operations: List[str]
    ) -> float:
        """Импортирует операции из файла.

        Returns:
            float: Итоговый баланс после импорта операций
        """
        # Загружаем и очищаем данные
        cleaned_ops = self.load_history_from_file(
            file_path, account_number, valid_operations
        )

        if cleaned_ops.empty:
            return 0.0

        # Проверяем конечный баланс перед добавлением операций
        if "date" in cleaned_ops.columns:
            cleaned_ops = cleaned_ops.sort_values("date")
        last_op = cleaned_ops.iloc[-1]

        # Парсим баланс - единственное место где нужна защита
        try:
            final_balance = float(last_op["balance_after"])
        except (ValueError, TypeError) as exc:
            raise ValueError("Некорректное значение баланса в файле") from exc

        if final_balance < 0:
            raise ValueError(
                "Значение баланса при загрузке операций стало отрицательным"
            )

        # Добавляем очищенные операции в историю - данные уже отчищены
        for _, op in cleaned_ops.iterrows():
            self.add_operation(
                op_type=op["operation"],
                amount=float(op["amount"]),
                timestamp=op["date"],  # Уже распарсенная дата
                balance_after=float(op["balance_after"]),
                status=op["status"],
            )

        return final_balance
