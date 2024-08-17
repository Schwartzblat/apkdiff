from typing import Dict
from apkdiff.common import APKAnalysis
from androguard.core.analysis.analysis import ClassAnalysis, FieldAnalysis


class Comparer:
    classes: Dict[str, str]

    def __init__(self, analysis1: APKAnalysis, analysis2: APKAnalysis):
        self.analysis1 = analysis1
        self.analysis2 = analysis2
        self.classes = dict()

    @staticmethod
    def is_same_field(field1: FieldAnalysis, field2: FieldAnalysis) -> int:
        confidence = 0
        confidence += 25 if field1.field.access_flags_string == field2.field.access_flags_string else 0
        confidence += 5 if field1.field.init_value == field2.field.init_value else 0
        confidence += 50 if field1.field.class_name == field2.field.class_name else 0
        confidence += 25 if field1.field.field_idx == field2.field.field_idx else 0
        confidence += 50 if field1.field.get_raw() == field2.field.get_raw() else 0

        return confidence

    @staticmethod
    def same_fields_confidence(class1: ClassAnalysis, class2: ClassAnalysis) -> int:
        """Terrible logic I need to kill myself"""
        return 100
        if len(class1.get_fields()) == 0 or len(class2.get_fields()) == 0:
            return 0 if len(class1.get_fields()) != len(class2.get_fields()) else 100
        ratings = []
        for field1 in class1.get_fields():
            field_rating = [0]
            for field2 in class2.get_fields():
                field_rating.append(Comparer.is_same_field(field1, field2))
            ratings.append(max(field_rating))
        return (sum(ratings) // len(ratings)) // abs(len(class1.get_fields()) - len(class2.get_fields()))

    @staticmethod
    def same_methods_confidence(class1: ClassAnalysis, class2: ClassAnalysis) -> int:
        pass

    @staticmethod
    def same_class_confidence(class1: ClassAnalysis, class2: ClassAnalysis) -> int:
        result_confidence = Comparer.same_fields_confidence(class1, class2)

        return result_confidence

    def compare_classes(self):
        for class_to_match in self.analysis1.analysis.get_classes():
            rating = []
            for other in self.analysis2.analysis.get_classes():
                rating.append(self.same_class_confidence(class_to_match, other))
            print(rating)

    def compare(self):
        self.compare_classes()
