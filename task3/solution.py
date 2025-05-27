"""
Задача 3: Функция appearance для вычисления времени общего присутствия.

Функция вычисляет время, когда ученик и учитель одновременно 
присутствовали на уроке.
"""

from typing import List, Tuple, Dict


def appearance(intervals: Dict[str, List[int]]) -> int:
    """
    Вычисляет время общего присутствия ученика и учителя на уроке.
    
    Args:
        intervals: Словарь с интервалами времени:
            - lesson: [start, end] - время урока
            - pupil: [start1, end1, start2, end2, ...] - интервалы ученика
            - tutor: [start1, end1, start2, end2, ...] - интервалы учителя
    
    Returns:
        Время общего присутствия в секундах
    """
    
    def parse_intervals(interval_list: List[int]) -> List[Tuple[int, int]]:
        """
        Преобразует список временных меток в список кортежей (начало, конец).
        
        Args:
            interval_list: Список временных меток [start1, end1, start2, end2, ...]
            
        Returns:
            Список кортежей [(start1, end1), (start2, end2), ...]
        """
        intervals = []
        for i in range(0, len(interval_list), 2):
            start = interval_list[i]
            end = interval_list[i + 1]
            intervals.append((start, end))
        return intervals
    
    def intersect_intervals(intervals1: List[Tuple[int, int]], 
                          intervals2: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Находит пересечения между двумя списками интервалов.
        
        Args:
            intervals1: Первый список интервалов
            intervals2: Второй список интервалов
            
        Returns:
            Список пересечений интервалов
        """
        intersections = []
        
        for start1, end1 in intervals1:
            for start2, end2 in intervals2:
                # Находим пересечение двух интервалов
                intersection_start = max(start1, start2)
                intersection_end = min(end1, end2)
                
                # Если пересечение существует (начало меньше конца)
                if intersection_start < intersection_end:
                    intersections.append((intersection_start, intersection_end))
        
        return intersections
    
    def merge_overlapping_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Объединяет перекрывающиеся или касающиеся интервалы.
        
        Args:
            intervals: Список интервалов для объединения
            
        Returns:
            Список объединенных интервалов
        """
        if not intervals:
            return []
        
        # Сортируем интервалы по времени начала
        sorted_intervals = sorted(intervals)
        merged = [sorted_intervals[0]]
        
        for current_start, current_end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]
            
            # Если интервалы перекрываются или касаются друг друга
            if current_start <= last_end:
                # Объединяем интервалы, расширяя конец до максимального
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                # Интервалы не пересекаются, добавляем новый
                merged.append((current_start, current_end))
        
        return merged
    
    def calculate_total_time(intervals: List[Tuple[int, int]]) -> int:
        """
        Вычисляет общее время для списка интервалов.
        
        Args:
            intervals: Список интервалов
            
        Returns:
            Общее время в секундах
        """
        return sum(end - start for start, end in intervals)
    
    # Парсим интервалы из входных данных
    lesson_intervals = parse_intervals(intervals['lesson'])
    pupil_intervals = parse_intervals(intervals['pupil'])
    tutor_intervals = parse_intervals(intervals['tutor'])
    
    # Ограничиваем интервалы ученика и учителя временем урока
    # (убираем время до начала и после окончания урока)
    pupil_in_lesson = intersect_intervals(pupil_intervals, lesson_intervals)
    tutor_in_lesson = intersect_intervals(tutor_intervals, lesson_intervals)
    
    # Находим п��ресечения между присутствием ученика и учителя
    common_intervals = intersect_intervals(pupil_in_lesson, tutor_in_lesson)
    
    # Объединяем перекрывающиеся интервалы общего присутствия
    merged_common = merge_overlapping_intervals(common_intervals)
    
    # Вычисляем общее время присутствия
    return calculate_total_time(merged_common)


def debug_appearance(intervals: Dict[str, List[int]]) -> Dict:
    """
    Отладочная версия функции appearance с подробным выводом.
    
    Args:
        intervals: Словарь с интервалами времени
        
    Returns:
        Словарь с результатами и промежуточными данными
    """
    def parse_intervals(interval_list):
        intervals = []
        for i in range(0, len(interval_list), 2):
            intervals.append((interval_list[i], interval_list[i + 1]))
        return intervals
    
    def intersect_intervals(intervals1, intervals2):
        intersections = []
        for start1, end1 in intervals1:
            for start2, end2 in intervals2:
                intersection_start = max(start1, start2)
                intersection_end = min(end1, end2)
                if intersection_start < intersection_end:
                    intersections.append((intersection_start, intersection_end))
        return intersections
    
    def merge_overlapping_intervals(intervals):
        if not intervals:
            return []
        sorted_intervals = sorted(intervals)
        merged = [sorted_intervals[0]]
        for current_start, current_end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]
            if current_start <= last_end:
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                merged.append((current_start, current_end))
        return merged
    
    def calculate_total_time(intervals):
        return sum(end - start for start, end in intervals)
    
    # Парсим интервалы
    lesson_intervals = parse_intervals(intervals['lesson'])
    pupil_intervals = parse_intervals(intervals['pupil'])
    tutor_intervals = parse_intervals(intervals['tutor'])
    
    # Промежуточные вычисления
    pupil_in_lesson = intersect_intervals(pupil_intervals, lesson_intervals)
    tutor_in_lesson = intersect_intervals(tutor_intervals, lesson_intervals)
    common_intervals = intersect_intervals(pupil_in_lesson, tutor_in_lesson)
    merged_common = merge_overlapping_intervals(common_intervals)
    total_time = calculate_total_time(merged_common)
    
    return {
        'lesson_intervals': lesson_intervals,
        'pupil_intervals': pupil_intervals,
        'tutor_intervals': tutor_intervals,
        'pupil_in_lesson': pupil_in_lesson,
        'tutor_in_lesson': tutor_in_lesson,
        'common_intervals': common_intervals,
        'merged_common': merged_common,
        'total_time': total_time
    }


def run_provided_tests():
    """Запуск предоставленных тестовых случаев."""
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

    print("=== Запуск предоставленных тестов ===")
    
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        expected = test['answer']
        
        print(f"Тест {i+1}: получено {test_answer}, ожидалось {expected}")
        
        if test_answer == expected:
            print(f"✓ Тест {i+1} пройден")
        else:
            print(f"✗ Тест {i+1} провален")
            # Выводим отладочную информацию
            debug_info = debug_appearance(test['intervals'])
            print(f"  Отладочная информация:")
            for key, value in debug_info.items():
                print(f"    {key}: {value}")
        
        print()
    
    print("Проверка завершена")


if __name__ == '__main__':
    run_provided_tests()
