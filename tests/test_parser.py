"""
Тесты для парсера
"""

import unittest
import pandas as pd
from io import StringIO
from src.parser import LogParser


class TestLogParser(unittest.TestCase):
    def setUp(self):
        """Создание тестовых данных"""
        csv_data = """student_id,activity_type,timestamp,score,duration_minutes
1,login,2024-01-15 09:30:00,85,5
1,assignment,2024-01-15 10:00:00,85,45
2,login,2024-01-15 09:45:00,78,5
2,forum,2024-01-16 14:20:00,,20
3,quiz,2024-01-17 11:15:00,92,30"""
        
        # Сохранение во временный файл
        with open('test_data.csv', 'w') as f:
            f.write(csv_data)
        
        self.parser = LogParser('test_data.csv')
    
    def tearDown(self):
        """Очистка после тестов"""
        import os
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')
    
    def test_parse_valid_data(self):
        """Тест парсинга валидных данных"""
        logs = self.parser.parse()
        
        self.assertEqual(len(logs), 5)
        self.assertEqual(logs[0]['student_id'], 1)
        self.assertEqual(logs[0]['activity_type'], 'login')
    
    def test_stats_calculation(self):
        """Тест расчета статистики"""
        logs = self.parser.parse()
        stats = self.parser.get_stats(logs)
        
        self.assertEqual(stats['total_records'], 5)
        self.assertEqual(stats['unique_students'], 3)


if __name__ == '__main__':
    unittest.main()