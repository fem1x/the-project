"""
Тесты для анализатора
"""

import unittest
import pandas as pd
from datetime import datetime
from src.analyzer import LearningAnalyzer


class TestLearningAnalyzer(unittest.TestCase):
    def setUp(self):
        """Создание тестовых данных с правильным форматом timestamp"""
        # Используем pd.Timestamp вместо строки
        self.test_logs = [
            {'student_id': 1, 'activity_type': 'login', 'timestamp': pd.Timestamp('2024-01-15 09:30:00'), 'score': 85},
            {'student_id': 1, 'activity_type': 'assignment', 'timestamp': pd.Timestamp('2024-01-15 10:00:00'), 'score': 90},
            {'student_id': 2, 'activity_type': 'login', 'timestamp': pd.Timestamp('2024-01-15 09:45:00'), 'score': 70},
            {'student_id': 2, 'activity_type': 'quiz', 'timestamp': pd.Timestamp('2024-01-16 11:00:00'), 'score': 80},
            {'student_id': 3, 'activity_type': 'forum', 'timestamp': pd.Timestamp('2024-01-17 14:20:00'), 'score': 75},
        ]
        
        self.analyzer = LearningAnalyzer(self.test_logs)
    
    def test_basic_stats(self):
        """Тест базовой статистики"""
        stats = self.analyzer.get_basic_stats()
        
        self.assertEqual(stats['total_activities'], 5)
        self.assertEqual(stats['total_students'], 3)
        self.assertIn('score_stats', stats)
        # Проверяем даты
        self.assertEqual(stats['date_range']['start'], '2024-01-15')
        self.assertEqual(stats['date_range']['end'], '2024-01-17')
    
    def test_student_performance(self):
        """Тест анализа успеваемости"""
        performance = self.analyzer.analyze_student_performance()
        
        self.assertIn('top_students', performance)
        self.assertIn('performance_distribution', performance)
        self.assertIsInstance(performance['correlation_activity_score'], float)
    
    def test_activity_effectiveness(self):
        """Тест анализа эффективности"""
        effectiveness = self.analyzer.analyze_activity_effectiveness()
        
        self.assertGreater(len(effectiveness), 0)
        for activity in effectiveness:
            self.assertIn('activity_type', activity)
            self.assertIn('avg_score', activity)
    
    def test_generate_recommendations(self):
        """Тест генерации рекомендаций"""
        recommendations = self.analyzer.generate_recommendations()
        
        self.assertGreater(len(recommendations), 0)
        for rec in recommendations:
            self.assertIn('title', rec)
            self.assertIn('description', rec)
            self.assertIn('suggestion', rec)


if __name__ == '__main__':
    unittest.main()