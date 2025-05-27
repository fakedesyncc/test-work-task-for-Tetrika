"""
Задача 1: Декоратор @strict для проверки типов аргументов функции.

Декоратор проверяет соответствие типов переданных аргументов 
типам, объявленным в аннотациях функции.
"""

import inspect
from functools import wraps


def strict(func):
    """
    Декоратор для проверки соответствия типов аргументов функции их аннотациям.
    
    Args:
        func: Декорируемая функция с аннотациями типов
        
    Returns:
        Обертка функции с проверкой типов
        
    Raises:
        TypeError: При несоответствии типов аргументов аннотациям
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов из функции
        annotations = func.__annotations__
        
        # Получаем сигнатуру функции для извлечения имен параметров
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        
        # Проверяем позиционные аргументы
        for i, arg in enumerate(args):
            if i < len(param_names):
                param_name = param_names[i]
                if param_name in annotations:
                    expected_type = annotations[param_name]
                    if not isinstance(arg, expected_type):
                        raise TypeError(
                            f"Argument '{param_name}' must be of type "
                            f"{expected_type.__name__}, got {type(arg).__name__}"
                        )
        
        # Проверяем именованные аргументы
        for param_name, arg in kwargs.items():
            if param_name in annotations:
                expected_type = annotations[param_name]
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument '{param_name}' must be of type "
                        f"{expected_type.__name__}, got {type(arg).__name__}"
                    )
        
        return func(*args, **kwargs)
    
    return wrapper


# Примеры использования
@strict
def sum_two(a: int, b: int) -> int:
    """Складывает два целых числа."""
    return a + b


@strict
def concat_strings(s1: str, s2: str) -> str:
    """Объединяет две строки."""
    return s1 + s2


@strict
def multiply_float(x: float, y: float) -> float:
    """Умножает два числа с плавающей точкой."""
    return x * y


@strict
def check_bool(flag: bool) -> str:
    """Возвращает строковое представление булевого значения."""
    return "True" if flag else "False"


if __name__ == "__main__":
    # Демонстрация работы
    print("=== Демонстрация работы декоратора @strict ===")
    
    # Корректные вызовы
    print(f"sum_two(1, 2) = {sum_two(1, 2)}")
    print(f"concat_strings('hello', 'world') = {concat_strings('hello', 'world')}")
    print(f"multiply_float(2.5, 3.0) = {multiply_float(2.5, 3.0)}")
    print(f"check_bool(True) = {check_bool(True)}")
    
    # Некорректные вызовы
    print("\n=== Примеры ошибок ===")
    
    try:
        sum_two(1, 2.4)
    except TypeError as e:
        print(f"sum_two(1, 2.4) -> {e}")
    
    try:
        concat_strings("hello", 123)
    except TypeError as e:
        print(f"concat_strings('hello', 123) -> {e}")
    
    try:
        check_bool(1)
    except TypeError as e:
        print(f"check_bool(1) -> {e}")
