# src/__init__.py
from .parser import LogParser
from .analyzer import LearningAnalyzer  # Измените LearningPathAnalyzer на LearningAnalyzer
from .visualizer import ResultVisualizer

__all__ = ['LogParser', 'LearningAnalyzer', 'ResultVisualizer']