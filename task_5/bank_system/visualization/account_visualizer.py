"""
Визуализация счетов

Класс для построения графиков истории операций банковских счетов.
Обеспечивает наглядное представление изменений баланса во времени.
Требует установки библиотеки matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from bank_system.accounts import Account


class AccountVisualizer:
    """Класс для визуализации истории операций счетов"""

    @staticmethod
    def plot_account_history(account: Account) -> None:
        """Построение графика истории операций для счета"""
        try:
            # Получаем историю операций
            history_df = account.get_history()

            if history_df.empty:
                raise ValueError(
                    "Нет данных для построения графика. "
                    + "Выполните операции со счетом."
                )

            # Создаем график
            plt.figure(figsize=(12, 6))

            # Строим линейный график: время операции -> баланс после операции
            plt.plot(
                history_df["timestamp"],
                history_df["balance_after"],
                marker="o",
                linewidth=2,
                markersize=6,
                color="blue",
                alpha=0.7,
            )

            # Настраиваем оформление графика
            plt.title(
                f"История изменения баланса счета\nВладелец: {account.holder}",
                fontsize=14,
                fontweight="bold",
                pad=20,
            )
            plt.xlabel("Время операции", fontsize=12)
            plt.ylabel("Баланс", fontsize=12)

            # Форматируем ось X (время)
            ax = plt.gca()

            # Настраиваем формат отображения дат
            date_format = mdates.DateFormatter("%d.%m.%Y %H:%M")
            ax.xaxis.set_major_formatter(date_format)

            # Автоматический поворот дат для лучшей читаемости
            plt.gcf().autofmt_xdate()

            # Добавляем сетку для удобства чтения
            plt.grid(True, alpha=0.3)

            # Подписываем точки на графике
            for timestamp, balance, op_type, amount in zip(
                history_df["timestamp"],
                history_df["balance_after"],
                history_df["op_type"],
                history_df["amount"],
            ):

                # Определяем цвет и формат суммы в зависимости от типа операции
                if op_type == "deposit":
                    amount_str = f"+{amount}"
                    color = "green"
                elif op_type == "withdraw":
                    amount_str = f"-{amount}"
                    color = "red"
                else:  # interest
                    amount_str = f"+{amount}"
                    color = "blue"

                plt.annotate(
                    f"{op_type}\n{amount_str}",
                    (timestamp, balance),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                    fontsize=9,
                    alpha=0.8,
                    color=color,
                    bbox={
                        "boxstyle": "round,pad=0.3",
                        "facecolor": "white",
                        "alpha": 0.8,
                    },
                )

            # Настраиваем внешний вид
            plt.tight_layout()

            # Показываем график
            plt.show()

        except ImportError as exc:
            raise ImportError(
                "Для графиков необходимо matplotlib: pip install matplotlib"
            ) from exc
        except Exception as e:
            raise e
