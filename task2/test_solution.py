"""
Тесты для парсера животных Wikipedia (Задача 2).
"""

import pytest
import csv
import os
from unittest.mock import Mock, patch, mock_open
from solution import WikipediaAnimalsParser


class TestWikipediaAnimalsParser:
    """Тесты для парсера животных Wikipedia."""
    
    def setup_method(self):
        """Подготовка для каждого теста."""
        self.parser = WikipediaAnimalsParser()
    
    def test_parser_initialization(self):
        """Тест инициализации парсера."""
        assert self.parser.base_url == "https://ru.wikipedia.org"
        assert "Категория:Животные_по_алфавиту" in self.parser.start_url
        assert len(self.parser.russian_alphabet) == 33
        assert "А" in self.parser.russian_alphabet
        assert "Я" in self.parser.russian_alphabet
    
    def test_russian_alphabet_completeness(self):
        """Тест полноты русского алфавита."""
        expected_letters = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"
        assert self.parser.russian_alphabet == expected_letters
    
    @patch('solution.requests.Session.get')
    def test_process_page_success(self, mock_get):
        """Тест успешной обработки страницы."""
        # Мокаем HTML ответ
        mock_html = """
        <html>
            <div id="mw-pages">
                <a href="/wiki/Аист">Аист</a>
                <a href="/wiki/Белка">Белка</a>
                <a href="/wiki/Волк">Волк</a>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.content = mock_html.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        animals_count = {letter: 0 for letter in self.parser.russian_alphabet}
        
        result = self.parser._process_page("http://test.url", animals_count)
        
        # Проверяем, что животные были подсчитаны
        assert animals_count['А'] == 1  # Аист
        assert animals_count['Б'] == 1  # Белка
        assert animals_count['В'] == 1  # Волк
        assert sum(animals_count.values()) == 3
    
    @patch('solution.requests.Session.get')
    def test_process_page_no_content(self, mock_get):
        """Тест обработки страницы без контента."""
        mock_html = "<html><body>No content</body></html>"
        
        mock_response = Mock()
        mock_response.content = mock_html.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        animals_count = {letter: 0 for letter in self.parser.russian_alphabet}
        
        result = self.parser._process_page("http://test.url", animals_count)
        
        assert result is None
        assert sum(animals_count.values()) == 0
    
    def test_save_to_csv(self):
        """Тест сохранения в CSV файл."""
        test_data = {'А': 5, 'Б': 3, 'В': 0, 'Г': 1}
        test_filename = "test_beasts.csv"
        
        try:
            self.parser.save_to_csv(test_data, test_filename)
            
            # Проверяем, что файл создан и содержит правильные данные
            assert os.path.exists(test_filename)
            
            with open(test_filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            # Проверяем содержимое (только буквы с животными)
            expected_rows = [['А', '5'], ['Б', '3'], ['Г', '1']]
            assert rows == expected_rows
            
        finally:
            # Удаляем тестовый файл
            if os.path.exists(test_filename):
                os.remove(test_filename)
    
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_save_to_csv_error(self, mock_open):
        """Тест обработки ошибки при сохранении CSV."""
        test_data = {'А': 5}
        
        # Не должно вызывать исключение, только вывести ошибку
        self.parser.save_to_csv(test_data, "test.csv")
    
    def test_print_statistics(self, capsys):
        """Тест вывода статистики."""
        test_data = {
            'А': 10, 'Б': 5, 'В': 0, 'Г': 1, 'Д': 0,
            'Е': 0, 'Ж': 0, 'З': 0, 'И': 0, 'Й': 0,
            'К': 0, 'Л': 0, 'М': 0, 'Н': 0, 'О': 0,
            'П': 0, 'Р': 0, 'С': 0, 'Т': 0, 'У': 0,
            'Ф': 0, 'Х': 0, 'Ц': 0, 'Ч': 0, 'Ш': 0,
            'Щ': 0, 'Э': 0, 'Ю': 0, 'Я': 0
        }
        
        self.parser.print_statistics(test_data)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Всего животных: 16" in output
        assert "Букв с животными: 3" in output
        assert "А: 10" in output
        assert "Б: 5" in output
        assert "Г: 1" in output
    
    def test_find_next_page_link(self):
        """Тест поиска ссылки на следующую страницу."""
        from bs4 import BeautifulSoup
        
        # HTML с ссылкой на следующую страницу
        html_with_next = """
        <html>
            <body>
                <a href="/wiki/Category:Animals?from=Б">следующие 200</a>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(html_with_next, 'html.parser')
        next_link = self.parser._find_next_page_link(soup)
        
        expected_url = "https://ru.wikipedia.org/wiki/Category:Animals?from=Б"
        assert next_link == expected_url
    
    def test_find_next_page_link_not_found(self):
        """Тест случая, когда ссылка на следующую страницу не найдена."""
        from bs4 import BeautifulSoup
        
        html_without_next = "<html><body>No next link</body></html>"
        soup = BeautifulSoup(html_without_next, 'html.parser')
        next_link = self.parser._find_next_page_link(soup)
        
        assert next_link is None


def run_manual_tests():
    """Запуск ручных тестов без pytest."""
    print("=== Запуск тестов для парсера животных ===")
    
    parser = WikipediaAnimalsParser()
    
    # Тест 1: Инициализация
    assert parser.base_url == "https://ru.wikipedia.org"
    assert len(parser.russian_alphabet) == 33
    print("✓ Тест 1 пройден: Инициализация парсера")
    
    # Тест 2: Сохранение в CSV
    test_data = {'А': 5, 'Б': 3, 'В': 0, 'Г': 1}
    test_filename = "test_manual.csv"
    
    try:
        parser.save_to_csv(test_data, test_filename)
        
        # Проверяем файл
        with open(test_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'А,5' in content
            assert 'Б,3' in content
            assert 'Г,1' in content
            assert 'В,0' not in content  # Нулевые значения не записываются
        
        print("✓ Тест 2 пройден: Сохранение в CSV")
        
    finally:
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    # Тест 3: Алфавит
    expected_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"
    assert parser.russian_alphabet == expected_alphabet
    print("✓ Тест 3 пройден: Русский алфавит")
    
    print("\n🎉 Все ручные тесты пройдены успешно!")


if __name__ == "__main__":
    run_manual_tests()
