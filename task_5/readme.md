## Архитектура системы:

### Классы счетов:

- Account - базовый класс

- CheckingAccount - расчетный счет

- SavingsAccount - сберегательный счет

### Сервисные классы:

- OperationHistory - управление историей операций

- AccountVisualizer - визуализация графиков

- TransactionAnalyzer - анализ транзакций

### Связи:

- Наследование: CheckingAccount и SavingsAccount наследуют Account

- Композиция: Account содержит OperationHistory

- Зависимость: Визуализатор и анализатор работают с Account

![Описание картинки](/task_5/assets/diagram.svg)