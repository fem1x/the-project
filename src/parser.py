"""
Парсер логов LMS
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict


class LogParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def parse(self) -> List[Dict]:
        """Чтение и обработка CSV файла"""
        try:
            # Чтение CSV
            df = pd.read_csv(self.filepath)
            
            # Проверка необходимых колонок
            required = ['student_id', 'activity_type', 'timestamp', 'score']
            for col in required:
                if col not in df.columns:
                    raise ValueError(f"Отсутствует колонка: {col}")
            
            # Преобразование данных
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            
            # Заполнение пропущенных значений
            if 'duration_minutes' in df.columns:
                df['duration_minutes'] = df['duration_minutes'].fillna(0)
            
            # Конвертация в список словарей
            logs = df.to_dict('records')
            
            print(f"✓ Успешно прочитано {len(logs)} записей")
            print(f"✓ Уникальных студентов: {df['student_id'].nunique()}")
            
            return logs
            
        except Exception as e:
            print(f"❌ Ошибка при чтении файла: {e}")
            return []
    
    def get_stats(self, logs: List[Dict]) -> Dict:
        """Базовая статистика данных"""
        if not logs:
            return {}
        
        df = pd.DataFrame(logs)
        
        return {
            'total_records': len(df),
            'unique_students': df['student_id'].nunique(),
            'start_date': df['timestamp'].min().strftime('%Y-%m-%d'),
            'end_date': df['timestamp'].max().strftime('%Y-%m-%d'),
            'activity_types': df['activity_type'].value_counts().to_dict(),
            'avg_score': df['score'].mean() if 'score' in df.columns else None
        }