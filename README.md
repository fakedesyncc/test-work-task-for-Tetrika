# Python Tasks Solutions for Tetrika

Решения трех задач на Python с тестами и документацией.

## Требования

- Python 3.9 или выше
- Библиотеки из requirements.txt (только для задачи 2)

## Установка

1. Клонируйте репозиторий или скачайте файлы
2. Установите зависимости:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Описание задач

### Задача 1: Декоратор @strict

Реализация декоратора для проверки соответствия типов аргументов функции их аннотациям.

**Запуск:**
\`\`\`bash
cd task1
python solution.py
python test_solution.py
\`\`\`

### Задача 2: Парсер животных Wikipedia

Скрипт для получения списка животных с русскоязычной Wikipedia и подсчета количества на каждую букву алфавита.

**Запуск:**
\`\`\`bash
cd task2
python solution.py
\`\`\`

### Задача 3: Функция appearance

Функция для вычисления времени общего присутствия ученика и учителя на уроке.

**Запуск:**
\`\`\`bash
cd task3
python solution.py
python test_solution.py
\`\`\`

## Запуск всех тестов

Для запуска всех тестов с помощью pytest:

\`\`\`bash
pytest -v
\`\`\`

Для запуска с покрытием кода:

\`\`\`bash
pytest --cov=. --cov-report=html
\`\`\`

## Примеры использования

### Задача 1
\`\`\`python
from task1.solution import strict

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))    # 3
print(sum_two(1, 2.4))  # TypeError
\`\`\`

### Задача 2
\`\`\`python
from task2.solution import get_animals_from_wikipedia, save_to_csv

animals_count = get_animals_from_wikipedia()
save_to_csv(animals_count, "beasts.csv")
\`\`\`

### Задача 3
\`\`\`python
from task3.solution import appearance

intervals = {
    'lesson': [1594663200, 1594666800],
    'pupil': [1594663340, 1594663389, 1594663390, 1594663395],
    'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
}

result = appearance(intervals)  # 3117
\`\`\`

## Результаты

### Задача 1
Декоратор успешно проверяет типы аргументов и бросает TypeError при несоответствии.

### Задача 2
Создается файл `beasts.csv` с количеством животных на каждую букву русского алфавита в формате:
\`\`\`
А,642
Б,412
В,318
...
\`\`\`

### Задача 3
Функция корректно вычисляет время общего присутствия для всех тестовых случаев.
