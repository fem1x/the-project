"""
Визуализация результатов
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict
import os


class ResultVisualizer:
    def __init__(self, results: Dict):
        self.results = results

    def create_plots(self, output_dir: str):
        """Создание всех графиков"""
        os.makedirs(output_dir, exist_ok=True)

        # 1. Распределение оценок
        if "student_performance" in self.results:
            self._plot_score_distribution(output_dir)

        # 2. Эффективность активностей
        if "activity_effectiveness" in self.results:
            self._plot_activity_effectiveness(output_dir)

        # 3. Временные паттерны
        if "time_patterns" in self.results:
            self._plot_time_patterns(output_dir)

        print(f"✓ Графики сохранены в {output_dir}/")

    def _plot_score_distribution(self, output_dir: str):
        """График распределения оценок"""
        perf_data = self.results["student_performance"]

        if "performance_distribution" in perf_data:
            fig, ax = plt.subplots(figsize=(10, 6))

            distribution = perf_data["performance_distribution"]
            bars = ax.bar(distribution.keys(), distribution.values())

            ax.set_title("Распределение студентов по успеваемости")
            ax.set_xlabel("Уровень успеваемости")
            ax.set_ylabel("Количество студентов")

            # Добавление значений на столбцы
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                )

            plt.tight_layout()
            plt.savefig(f"{output_dir}/score_distribution.png", dpi=150)
            plt.close()

    def _plot_activity_effectiveness(self, output_dir: str):
        """График эффективности активностей"""
        activities = self.results["activity_effectiveness"]

        if activities:
            df = pd.DataFrame(activities)

            fig, ax = plt.subplots(figsize=(12, 6))

            x = range(len(df))
            bars = ax.bar(x, df["avg_score"])

            ax.set_title("Эффективность типов активностей")
            ax.set_xlabel("Тип активности")
            ax.set_ylabel("Средний балл")
            ax.set_xticks(x)
            ax.set_xticklabels(df["activity_type"], rotation=45, ha="right")

            # Добавление количества
            for i, (bar, count) in enumerate(zip(bars, df["count"])):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 1,
                    f"n={count}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

            plt.tight_layout()
            plt.savefig(f"{output_dir}/activity_effectiveness.png", dpi=150)
            plt.close()

    def _plot_time_patterns(self, output_dir: str):
        """График временных паттернов"""
        time_data = self.results["time_patterns"]

        if "weekday_distribution" in time_data:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

            # График 1: Дни недели
            weekdays = time_data["weekday_distribution"]
            days = list(weekdays.keys())
            counts = list(weekdays.values())

            ax1.bar(days, counts)
            ax1.set_title("Активность по дням недели")
            ax1.set_xlabel("День недели")
            ax1.set_ylabel("Количество активностей")
            ax1.tick_params(axis="x", rotation=45)

            # График 2: Часы пик
            if "peak_hours" in time_data:
                hours = time_data["peak_hours"]["hours"]
                hour_counts = time_data["peak_hours"]["counts"]

                ax2.bar(hours, hour_counts)
                ax2.set_title("Часы наибольшей активности")
                ax2.set_xlabel("Час дня")
                ax2.set_ylabel("Количество активностей")

            plt.tight_layout()
            plt.savefig(f"{output_dir}/time_patterns.png", dpi=150)
            plt.close()
