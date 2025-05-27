"""
Тесты для функции appearance (Задача 3).
"""

import pytest
from solution import appearance, debug_appearance


class TestAppearanceFunction:
    """Тесты для функции appearance."""
    
    def test_provided_test_case_1(self):
        """Тест первого предоставленного случая."""
        intervals = {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
        }
        expected = 3117
        result = appearance(intervals)
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_provided_test_case_2(self):
        """Тест второго предоставленного случая."""
        intervals = {
            'lesson': [1594702800, 1594706400],
            'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 
                     1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 
                     1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 
                     1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 
                     1594706524, 1594706524, 1594706579, 1594706641],
            'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
        }
        expected = 3577
        result = appearance(intervals)
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_provided_test_case_3(self):
        """Тест третьего предоставленного случая."""
        intervals = {
            'lesson': [1594692000, 1594695600],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
        }
        expected = 3565
        result = appearance(intervals)
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_no_intersection(self):
        """Тест случая без пересечений."""
        intervals = {
            'lesson': [100, 200],
            'pupil': [50, 90],
            'tutor': [210, 250]
        }
        expected = 0
        result = appearance(intervals)
        assert result == expected
    
    def test_full_overlap(self):
        """Тест случая полного совпадения."""
        intervals = {
            'lesson': [100, 200],
            'pupil': [100, 200],
            'tutor': [100, 200]
        }
        expected = 100
        result = appearance(intervals)
        assert result == expected
    
    def test_partial_overlap(self):
        """Тест случая частичного пересечения."""
        intervals = {
            'lesson': [100, 200],
            'pupil': [150, 250],
            'tutor': [50, 175]
        }
        expected = 25  # Пересечение с 150 по 175
        result = appearance(intervals)
        assert result == expected
    
    def test_multiple_pupil_intervals(self):
        """Тест с несколькими интервалами ученика."""
        intervals = {
            'lesson': [100, 300],
            'pupil': [110, 130, 140, 160, 170, 190],
            'tutor': [105, 195]
        }
        # Ученик: (110,130), (140,160), (170,190)
        # Учитель: (105,195)
        # Пересечения: (110,130)=20, (140,160)=20, (170,190)=20
        # Итого: 60
        expected = 60
        result = appearance(intervals)
        assert result == expected
    
    def test_multiple_tutor_intervals(self):
        """Тест с несколькими интервалами учителя."""
        intervals = {
            'lesson': [100, 300],
            'pupil': [105, 195],
            'tutor': [110, 130, 140, 160, 170, 190]
        }
        # Учитель: (110,130), (140,160), (170,190)
        # Ученик: (105,195)
        # Пересечения: (110,130)=20, (140,160)=20, (170,190)=20
        # Итого: 60
        expected = 60
        result = appearance(intervals)
        assert result == expected
    
    def test_overlapping_intervals(self):
        """Тест с перекрывающимися интервалами."""
        intervals = {
            'lesson': [100, 300],
            'pupil': [110, 150, 140, 180],  # Перекрывающиеся интервалы
            'tutor': [105, 195]
        }
        # Ученик после объединения: (110, 180)
        # Учитель: (105, 195)
        # Пересечение: (110, 180) = 70
        expected = 70
        result = appearance(intervals)
        assert result == expected
    
    def test_outside_lesson_time(self):
        """Тест с интервалами вне времени урока."""
        intervals = {
            'lesson': [100, 200],
            'pupil': [50, 150, 180, 250],  # Частично вне урока
            'tutor': [75, 175, 190, 300]   # Частично вне урока
        }
        # Ученик в рамках урока: (100, 150)
        # Учитель в рамках урока: (100, 175)
        # Пересечение: (100, 150) = 50
        expected = 50
        result = appearance(intervals)
        assert result == expected
    
    def test_touching_intervals(self):
        """Тест с касающимися интервалами."""
        intervals = {
            'lesson': [100, 300],
            'pupil': [110, 150, 150, 190],  # Касающиеся интервалы
            'tutor': [105, 195]
        }
        # Ученик после объединения: (110, 190)
        # Учитель: (105, 195)
        # Пересечение: (110, 190) = 80
        expected = 80
        result = appearance(intervals)
        assert result == expected
    
    def test_empty_intervals(self):
        """Тест с пустыми интервалами."""
        intervals = {
            'lesson': [100, 200],
            'pupil': [],
            'tutor': [110, 150]
        }
        expected = 0
        result = appearance(intervals)
        assert result == expected
    
    def test_single_point_intervals(self):
        """Тест с интервалами нулевой длины."""
        intervals = {
            'lesson': [100, 200],
            'pupil': [110, 110, 120, 130],  # Один интервал нулевой длины
            'tutor': [105, 125]
        }
        # Ученик: (120, 130)
        # Учитель: (105, 125)
        # Пересечение: (120, 125) = 5
        expected = 5
        result = appearance(intervals)
        assert result == expected


def run_manual_tests():
    """Запуск ручных тестов без pytest."""
    print("=== Запуск тестов для функции appearance ===")
    
    # Предоставленные тесты
    tests = [
        {'intervals': {'lesson': [1594663200, 1594666800],
                 'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                 'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
         'answer': 3117
        },
        {'intervals': {'lesson': [1594702800, 1594706400],
                 'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                 'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
        'answer': 3577
        },
        {'intervals': {'lesson': [1594692000, 1594695600],
                 'pupil': [1594692033, 1594696347],
                 'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
        'answer': 3565
        },
    ]

    print("Предоставленные тесты:")
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        expected = test['answer']
        
        print(f"Тест {i+1}: получено {test_answer}, ожидалось {expected}")
        assert test_answer == expected, f'Ошибка в тесте {i+1}: получено {test_answer}, ожидалось {expected}'
        print(f"✓ Тест {i+1} пройден")
    
    # Дополнительные тесты
    print("\nДополнительные тесты:")
    
    # Тест: нет пересечений
    test1 = {
        'lesson': [100, 200],
        'pupil': [50, 90],
        'tutor': [210, 250]
    }
    assert appearance(test1) == 0
    print("✓ Тест без пересечений пройден")
    
    # Тест: полное совпадение
    test2 = {
        'lesson': [100, 200],
        'pupil': [100, 200],
        'tutor': [100, 200]
    }
    assert appearance(test2) == 100
    print("✓ Тест полного совпадения пройден")
    
    # Тест: частичное пересечение
    test3 = {
        'lesson': [100, 200],
        'pupil': [150, 250],
        'tutor': [50, 175]
    }
    assert appearance(test3) == 25
    print("✓ Тест частичного пересечения пройден")
    
    print("\n🎉 Все тесты пройдены успешно!")


if __name__ == "__main__":
    run_manual_tests()
