"""
Задача 2: Парсинг животных с русскоязычной Wikipedia.

Скрипт получает список всех животных из категории "Животные по алфавиту"
и подсчитывает количество на каждую букву русского алфавита.
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin
import time
import sys
from typing import Dict, Optional


class WikipediaAnimalsParser:
    """Парсер для получения списка животных с Wikipedia."""
    
    def __init__(self):
        self.base_url = "https://ru.wikipedia.org"
        self.start_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
        self.russian_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"
        
        # Настройка сессии
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_animals_count(self, max_pages: int = 50) -> Dict[str, int]:
        """
        Получает количество животных на каждую букву алфавита.
        
        Args:
            max_pages: Максимальное количество страниц для обработки
            
        Returns:
            Словарь с количеством животных для каждой буквы
        """
        animals_count = {letter: 0 for letter in self.russian_alphabet}
        
        current_url = self.start_url
        page_count = 0
        
        print(f"Начинаем парсинг животных с Wikipedia...")
        print(f"Максимальное количество страниц: {max_pages}")
        
        while current_url and page_count < max_pages:
            print(f"Обрабатываем страницу {page_count + 1}: {current_url}")
            
            try:
                next_url = self._process_page(current_url, animals_count)
                current_url = next_url
                page_count += 1
                
                # Пауза между запросами для вежливости к серверу
                time.sleep(1)
                
            except Exception as e:
                print(f"Ошибка при обработке страницы {current_url}: {e}")
                break
        
        total_animals = sum(animals_count.values())
        print(f"\nПарсинг завершен. Обработано страниц: {page_count}")
        print(f"Всего найдено животных: {total_animals}")
        
        return animals_count
    
    def _process_page(self, url: str, animals_count: Dict[str, int]) -> Optional[str]:
        """
        Обрабатывает одну страницу категории.
        
        Args:
            url: URL страницы для обработки
            animals_count: Словарь для накопления результатов
            
        Returns:
            URL следующей страницы или None, если следующей страницы нет
        """
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Находим контейнер с содержимым категории
        category_content = soup.find('div', {'id': 'mw-pages'})
        if not category_content:
            print("Не найден контейнер с содержимым категории")
            return None
        
        # Находим все ссылки на статьи в категории
        links = category_content.find_all('a', href=True)
        
        page_animals = 0
        for link in links:
            title = link.get_text().strip()
            if title and len(title) > 0:
                first_char = title[0].upper()
                if first_char in self.russian_alphabet:
                    animals_count[first_char] += 1
                    page_animals += 1
        
        print(f"  Найдено животных на странице: {page_animals}")
        
        # Ищем ссылку на следующую страницу
        next_link = self._find_next_page_link(soup)
        
        return next_link
    
    def _find_next_page_link(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Находит ссылку на следующую страницу категории.
        
        Args:
            soup: Объект BeautifulSoup текущей страницы
            
        Returns:
            URL следующей страницы или None
        """
        # Ищем ссылки на следующую страницу
        next_patterns = [
            r'следующие \d+',
            r'следующая страница',
            r'далее'
        ]
        
        for pattern in next_patterns:
            next_links = soup.find_all('a', string=re.compile(pattern, re.IGNORECASE))
            if next_links:
                return urljoin(self.base_url, next_links[0]['href'])
        
        # Альтернативный поиск по тексту ссылки
        for link in soup.find_all('a', href=True):
            link_text = link.get_text().strip().lower()
            if 'следующие' in link_text or 'далее' in link_text:
                return urljoin(self.base_url, link['href'])
        
        return None
    
    def save_to_csv(self, animals_count: Dict[str, int], filename: str = "beasts.csv") -> None:
        """
        Сохраняет результаты в CSV файл.
        
        Args:
            animals_count: Словарь с количеством животных
            filename: Имя файла для сохранения
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Записываем только буквы с животными, отсортированные по алфавиту
                for letter in sorted(animals_count.keys()):
                    if animals_count[letter] > 0:
                        writer.writerow([letter, animals_count[letter]])
            
            print(f"Результаты сохранены в файл: {filename}")
            
        except Exception as e:
            print(f"Ошибка при сохранении файла {filename}: {e}")
    
    def print_statistics(self, animals_count: Dict[str, int]) -> None:
        """
        Выводит статистику по найденным животным.
        
        Args:
            animals_count: Словарь с количеством животных
        """
        print("\n=== Статистика по буквам ===")
        
        total = sum(animals_count.values())
        letters_with_animals = sum(1 for count in animals_count.values() if count > 0)
        
        print(f"Всего животных: {total}")
        print(f"Букв с животными: {letters_with_animals} из {len(self.russian_alphabet)}")
        
        print("\nТоп-10 букв по количеству животных:")
        sorted_letters = sorted(animals_count.items(), key=lambda x: x[1], reverse=True)
        
        for i, (letter, count) in enumerate(sorted_letters[:10]):
            if count > 0:
                print(f"{i+1:2d}. {letter}: {count}")
        
        print("\nВсе буквы с животными:")
        for letter in sorted(animals_count.keys()):
            count = animals_count[letter]
            if count > 0:
                print(f"{letter}: {count}")


def main():
    """Основная функция для запуска парсинга."""
    parser = WikipediaAnimalsParser()
    
    try:
        # Получаем данные
        animals_count = parser.get_animals_count(max_pages=30)
        
        # Выводим статистику
        parser.print_statistics(animals_count)
        
        # Сохраняем в CSV
        parser.save_to_csv(animals_count)
        
        return animals_count
        
    except KeyboardInterrupt:
        print("\nПарсинг прерван пользователем")
        return {}
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return {}


if __name__ == "__main__":
    main()
