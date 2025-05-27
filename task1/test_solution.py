"""
Тесты для декоратора @strict (Задача 1).
"""

import pytest
from solution import strict


class TestStrictDecorator:
    """Тесты для декоратора @strict."""
    
    def setup_method(self):
        """Подготовка тестовых функций."""
        
        @strict
        def sum_two(a: int, b: int) -> int:
            return a + b
        
        @strict
        def concat_strings(s1: str, s2: str) -> str:
            return s1 + s2
        
        @strict
        def multiply_float(x: float, y: float) -> float:
            return x * y
        
        @strict
        def check_bool(flag: bool) -> str:
            return "True" if flag else "False"
        
        @strict
        def mixed_types(num: int, text: str, flag: bool, decimal: float) -> str:
            return f"{num}-{text}-{flag}-{decimal}"
        
        self.sum_two = sum_two
        self.concat_strings = concat_strings
        self.multiply_float = multiply_float
        self.check_bool = check_bool
        self.mixed_types = mixed_types
    
    def test_correct_int_types(self):
        """Тест корректных целочисленных аргументов."""
        assert self.sum_two(1, 2) == 3
        assert self.sum_two(0, 0) == 0
        assert self.sum_two(-5, 10) == 5
    
    def test_incorrect_int_types(self):
        """Тест некорректных типов для целочисленных аргументов."""
        with pytest.raises(TypeError, match="must be of type int"):
            self.sum_two(1, 2.4)
        
        with pytest.raises(TypeError, match="must be of type int"):
            self.sum_two("1", 2)
        
        with pytest.raises(TypeError, match="must be of type int"):
            self.sum_two(1.0, 2)
    
    def test_correct_string_types(self):
        """Тест корректных строковых аргументов."""
        assert self.concat_strings("hello", "world") == "helloworld"
        assert self.concat_strings("", "test") == "test"
        assert self.concat_strings("a", "") == "a"
    
    def test_incorrect_string_types(self):
        """Тест некорректных типов для строковых аргументов."""
        with pytest.raises(TypeError, match="must be of type str"):
            self.concat_strings("hello", 123)
        
        with pytest.raises(TypeError, match="must be of type str"):
            self.concat_strings(123, "world")
    
    def test_correct_float_types(self):
        """Тест корректных аргументов с плавающей точкой."""
        assert self.multiply_float(2.5, 3.0) == 7.5
        assert self.multiply_float(0.0, 5.5) == 0.0
        assert self.multiply_float(-2.5, 2.0) == -5.0
    
    def test_incorrect_float_types(self):
        """Тест некорректных типов для аргументов с плавающей точкой."""
        with pytest.raises(TypeError, match="must be of type float"):
            self.multiply_float(2, 3.0)
        
        with pytest.raises(TypeError, match="must be of type float"):
            self.multiply_float(2.5, 3)
    
    def test_correct_bool_types(self):
        """Тест корректных булевых аргументов."""
        assert self.check_bool(True) == "True"
        assert self.check_bool(False) == "False"
    
    def test_incorrect_bool_types(self):
        """Тест некорректных типов для булевых аргументов."""
        with pytest.raises(TypeError, match="must be of type bool"):
            self.check_bool(1)
        
        with pytest.raises(TypeError, match="must be of type bool"):
            self.check_bool(0)
        
        with pytest.raises(TypeError, match="must be of type bool"):
            self.check_bool("True")
    
    def test_mixed_types_correct(self):
        """Тест функции со смешанными типами - корректные аргументы."""
        result = self.mixed_types(42, "test", True, 3.14)
        assert result == "42-test-True-3.14"
    
    def test_mixed_types_incorrect(self):
        """Тест функции со смешанными типами - некорректные аргументы."""
        with pytest.raises(TypeError):
            self.mixed_types("42", "test", True, 3.14)  # str вместо int
        
        with pytest.raises(TypeError):
            self.mixed_types(42, 123, True, 3.14)  # int вместо str
        
        with pytest.raises(TypeError):
            self.mixed_types(42, "test", 1, 3.14)  # int вместо bool
        
        with pytest.raises(TypeError):
            self.mixed_types(42, "test", True, 3)  # int вместо float
    
    def test_keyword_arguments(self):
        """Тест именованных аргументов."""
        assert self.sum_two(a=1, b=2) == 3
        assert self.sum_two(b=2, a=1) == 3
        
        with pytest.raises(TypeError):
            self.sum_two(a=1, b=2.5)
    
    def test_mixed_positional_and_keyword(self):
        """Тест смешанных позиционных и именованных аргументов."""
        assert self.sum_two(1, b=2) == 3
        
        with pytest.raises(TypeError):
            self.sum_two(1, b=2.5)


def run_manual_tests():
    """Запуск ручных тестов без pytest."""
    print("=== Запуск тестов для декоратора @strict ===")
    
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b
    
    @strict
    def concat_strings(s1: str, s2: str) -> str:
        return s1 + s2
    
    @strict
    def multiply_float(x: float, y: float) -> float:
        return x * y
    
    @strict
    def check_bool(flag: bool) -> str:
        return "True" if flag else "False"
    
    # Тест 1: Корректные типы
    assert sum_two(1, 2) == 3
    print("✓ Тест 1 пройден: sum_two(1, 2) = 3")
    
    # Тест 2: Некорректные типы - должен вызвать TypeError
    try:
        sum_two(1, 2.4)
        assert False, "Should have raised TypeError"
    except TypeError:
        print("✓ Тест 2 пройден: sum_two(1, 2.4) вызвал TypeError")
    
    # Тест 3: Строки
    assert concat_strings("hello", "world") == "helloworld"
    print("✓ Тест 3 пройден: concat_strings работает корректно")
    
    # Тест 4: Некорректный тип для строк
    try:
        concat_strings("hello", 123)
        assert False, "Should have raised TypeError"
    except TypeError:
        print("✓ Тест 4 пройден: concat_strings с int вызвал TypeError")
    
    # Тест 5: Float
    assert multiply_float(2.5, 3.0) == 7.5
    print("✓ Тест 5 пройден: multiply_float работает корректно")
    
    # Тест 6: Bool
    assert check_bool(True) == "True"
    assert check_bool(False) == "False"
    print("✓ Тест 6 пройден: check_bool работает корректно")
    
    # Тест 7: Некорректный тип для bool
    try:
        check_bool(1)  # int вместо bool
        assert False, "Should have raised TypeError"
    except TypeError:
        print("✓ Тест 7 пройден: check_bool с int вызвал TypeError")
    
    print("\n🎉 Все тесты пройдены успешно!")


if __name__ == "__main__":
    run_manual_tests()
