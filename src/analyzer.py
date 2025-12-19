"""
Анализатор путей обучения
"""

import pandas as pd
from typing import Dict, List


class LearningAnalyzer:
    def __init__(self, logs: List[Dict]):
        self.logs = logs
        self.df = pd.DataFrame(logs)

    def analyze_all(self) -> Dict:
        """Выполнение всех анализов"""
        return {
            "basic_stats": self.get_basic_stats(),
            "student_performance": self.analyze_student_performance(),
            "activity_effectiveness": self.analyze_activity_effectiveness(),
            "time_patterns": self.analyze_time_patterns(),
            "recommendations": self.generate_recommendations(),
        }

    def get_basic_stats(self) -> Dict:
        """Базовая статистика"""
        stats = {
            "total_activities": len(self.df),
            "total_students": self.df["student_id"].nunique(),
            "date_range": {
                "start": self.df["timestamp"].min().strftime("%Y-%m-%d"),
                "end": self.df["timestamp"].max().strftime("%Y-%m-%d"),
            },
            "avg_activities_per_student": (
                len(self.df) / self.df["student_id"].nunique()
            ),
        }

        if "score" in self.df.columns:
            scores = self.df["score"].dropna()
            if len(scores) > 0:
                stats["score_stats"] = {
                    "avg": float(scores.mean()),
                    "max": float(scores.max()),
                    "min": float(scores.min()),
                    "std": float(scores.std()),
                }

        return stats

    def analyze_student_performance(self) -> Dict:
        """Анализ успеваемости студентов"""
        if "score" not in self.df.columns:
            return {}

        student_scores = (
            self.df.groupby("student_id")
            .agg({"score": "mean", "activity_type": "count"})
            .rename(columns={"activity_type": "activity_count"})
        )

        student_scores["performance_level"] = pd.cut(
            student_scores["score"],
            bins=[0, 60, 80, 100],
            labels=["низкий", "средний", "высокий"],
        )

        return {
            "top_students": (student_scores.nlargest(5, "score").to_dict("index")),
            "performance_distribution": (
                student_scores["performance_level"].value_counts().to_dict()
            ),
            "correlation_activity_score": float(
                student_scores["activity_count"].corr(student_scores["score"])
            ),
        }

    def analyze_activity_effectiveness(self) -> Dict:
        """Анализ эффективности активностей"""
        if "score" not in self.df.columns:
            return {}

        activity_scores = self.df.groupby("activity_type").agg(
            {"score": ["mean", "count", "std"]}
        )

        activity_scores.columns = ["avg_score", "count", "std_score"]
        activity_scores = activity_scores.reset_index()
        activity_scores["effectiveness_rank"] = activity_scores["avg_score"].rank(
            ascending=False
        )

        return activity_scores.to_dict("records")

    def analyze_time_patterns(self) -> Dict:
        """Анализ временных паттернов"""
        patterns = {}

        if "hour" in self.df.columns:
            hourly_counts = self.df["hour"].value_counts().sort_index()
            patterns["peak_hours"] = {
                "hours": hourly_counts.nlargest(3).index.tolist(),
                "counts": hourly_counts.nlargest(3).values.tolist(),
            }

        if "day_of_week" in self.df.columns:
            weekday_order = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            weekday_counts = self.df["day_of_week"].value_counts()
            weekday_counts = weekday_counts.reindex(weekday_order, fill_value=0)
            patterns["weekday_distribution"] = weekday_counts.to_dict()

        return patterns

    def generate_recommendations(self) -> List[Dict]:
        """Генерация рекомендаций"""
        recommendations = []

        activity_effectiveness = self.analyze_activity_effectiveness()
        if activity_effectiveness:
            best_activity = max(activity_effectiveness, key=lambda x: x["avg_score"])
            rec_desc = (
                f'Активность "{best_activity["activity_type"]}" '
                f"показывает наилучшие результаты"
            )
            recommendations.append(
                {
                    "type": "activity",
                    "title": "Эффективные активности",
                    "description": rec_desc,
                    "suggestion": "Уделяйте больше времени этому виду активности",
                }
            )

        time_patterns = self.analyze_time_patterns()
        if "peak_hours" in time_patterns:
            peak_hours = time_patterns["peak_hours"]["hours"]
            time_desc = (
                f"Наиболее продуктивные часы: " f'{", ".join(map(str, peak_hours))}:00'
            )
            recommendations.append(
                {
                    "type": "time",
                    "title": "Лучшее время для обучения",
                    "description": time_desc,
                    "suggestion": "Планируйте занятия в это время",
                }
            )

        stats = self.get_basic_stats()
        if "score_stats" in stats:
            avg_score = stats["score_stats"]["avg"]
            if avg_score < 70:
                score_desc = (
                    f"Средний балл ({avg_score:.1f}) ниже " f"рекомендуемого уровня"
                )
                recommendations.append(
                    {
                        "type": "general",
                        "title": "Улучшение успеваемости",
                        "description": score_desc,
                        "suggestion": "Увеличьте время подготовки к заданиям",
                    }
                )

        return recommendations
