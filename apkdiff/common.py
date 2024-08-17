import dataclasses
import enum
from typing import Dict
from androguard.core.analysis.analysis import Analysis
from androguard.core.apk import APK


class ClassWeights(float, enum.Enum):
    AST_CONFIDENCE = 50 / 100
    STRINGS_CONFIDENCE = 25 / 100
    XREF_CONFIDENCE = 10 / 100
    METHODS_CONFIDENCE = 10 / 100
    FIELDS_CONFIDENCE = 5 / 100


class ClassMatchResult:
    pass


@dataclasses.dataclass
class APKAnalysis:
    apk: APK
    analysis: Analysis
