import dataclasses
import enum
from typing import Dict
from androguard.core.analysis.analysis import Analysis
from androguard.core.apk import APK


class Weights(enum.IntEnum):
    pass


class ClassMatchResult:
    pass


@dataclasses.dataclass
class APKAnalysis:
    apk: APK
    analysis: Analysis
