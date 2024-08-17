import re
from androguard.core.analysis.analysis import ClassAnalysis
from apkdiff.utils import get_stripped_ast, get_strings
from deepdiff import DeepDiff
from difflib import SequenceMatcher
from apkdiff.common import ClassWeights


class ClassComparer:

    def __init__(self, class1: ClassAnalysis, class2: ClassAnalysis) -> None:
        self.class1 = class1
        self.class2 = class2

    def compare_ast(self) -> float:
        stripped_ast1 = get_stripped_ast(self.class1)
        stripped_ast2 = get_stripped_ast(self.class2)
        diff = DeepDiff(stripped_ast1, stripped_ast2)
        total_change = 0
        if diff == {}:
            return 100
        for change in diff['values_changed'].values():
            total_change += SequenceMatcher(None, change['new_value'], change['old_value']).quick_ratio()
        return 100 - (total_change / len(str(stripped_ast1))) * 100

    def compare_strings(self) -> float:
        strings1 = get_strings(self.class1)
        strings2 = get_strings(self.class2)
        diff = DeepDiff(strings1, strings2)
        if diff == {}:
            return 100
        return 100 - (len(diff['values_changed'].values()) / len(strings1))

    def get_confidence(self) -> float:
        confidence = self.compare_ast() * ClassWeights.AST_CONFIDENCE
        confidence += self.compare_strings() * ClassWeights.STRINGS_CONFIDENCE
        return confidence
