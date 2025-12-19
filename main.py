#!/usr/bin/env python3
"""
Learning Path Analyzer - простой запуск
"""

import argparse
import json
import os
from src.parser import LogParser
from src.analyzer import LearningAnalyzer
from src.visualizer import ResultVisualizer


def main():
    parser = argparse.ArgumentParser(description='Анализ путей обучения студентов')
    parser.add_argument('--input', required=True, help='CSV файл с логами')
    parser.add_argument('--output', default='results', help='Папка для результатов')
    parser.add_argument('--student-id', type=int, help='Анализ конкретного студента')
    
    args = parser.parse_args()
    
    print("=== Learning Path Analyzer ===")
    
    # СОЗДАЁМ ПАПКУ ДЛЯ РЕЗУЛЬТАТОВ
    os.makedirs(args.output, exist_ok=True)
    
    # 1. Парсинг данных
    print("📊 Чтение данных...")
    parser = LogParser(args.input)
    logs = parser.parse()
    
    if not logs:
        print("❌ Нет данных для анализа")
        return
    
    print(f"✓ Прочитано {len(logs)} записей")
    
    # 2. Анализ
    print("\n🔍 Анализ данных...")
    analyzer = LearningAnalyzer(logs)
    results = analyzer.analyze_all()
    
    # 3. Сохранение результатов
    with open(os.path.join(args.output, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("✓ Результаты сохранены")
    
    # 4. Визуализация
    print("\n📈 Создание графиков...")
    visualizer = ResultVisualizer(results)
    visualizer.create_plots(args.output)
    
    print("\n✅ Анализ завершен!")
    print(f"Результаты в папке: {args.output}")


if __name__ == "__main__":
    main()