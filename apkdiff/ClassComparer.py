import re
from androguard.core.analysis.analysis import ClassAnalysis
from apkdiff.utils import get_stripped_ast
from deepdiff import DeepDiff
from difflib import SequenceMatcher


class ClassComparer:

    def __init__(self, class1: ClassAnalysis, class2: ClassAnalysis) -> None:
        self.class1 = class1
        self.class2 = class2

    def compare_ast(self) -> float:
        stripped_ast1 = get_stripped_ast(self.class1)
        stripped_ast2 = get_stripped_ast(self.class2)
        diff = DeepDiff(stripped_ast1, stripped_ast2)
        average_change = 0
        if diff == {}:
            return 100
        for change in diff['values_changed'].values():
            average_change += SequenceMatcher(None, change['new_value'], change['old_value']).quick_ratio()
        return 100 - ((average_change / len(diff['values_changed'].values())) / len(str(stripped_ast1)))

    def get_confidence(self) -> float:
        confidence = self.compare_ast()

        return confidence
