"""
Анализ транзакций

Класс для анализа истории банковских операций.
Предоставляет методы для фильтрации и сортировки транзакций
по различным критериям (сумма, дата).
"""

from bank_system.accounts import Account
import pandas as pd


class TransactionAnalyzer:
    """Класс для анализа истории операций счетов"""

    @staticmethod
    def analyze_transactions(
        account: Account, n: int = 5, sort_by: str = "amount"
    ) -> pd.DataFrame:
        """
        Анализ истории транзакций по размеру и дате

        Args:
            account: Счет для анализа
            n: Количество операций для возврата
            sort_by: Критерий сортировки
            ('amount' - по сумме, 'date' - по дате)

        Returns:
            DataFrame с проанализированными операциями
        """
        history_df = account.get_history()

        if history_df.empty:
            return pd.DataFrame()

        # Фильтруем успешные операции
        successful_ops = history_df[history_df["status"] == "success"].copy()

        if successful_ops.empty:
            return pd.DataFrame()

        # Сортируем в зависимости от критерия
        if sort_by == "amount":
            # По сумме (крупные сначала) и по дате (свежие сначала)
            analyzed_df = successful_ops.sort_values(
                by=["amount", "timestamp"], ascending=[False, False]
            ).head(n)
        elif sort_by == "date":
            # Только по дате (свежие сначала)
            analyzed_df = successful_ops.sort_values(
                "timestamp",
                ascending=False
            ).head(n)
        else:
            raise ValueError("sort_by должен быть 'amount' или 'date'")

        return analyzed_df[["op_type", "amount", "timestamp", "balance_after"]]
