import shutil
import pathlib
import os.path
import re
import uuid
import pickle
from termcolor import cprint
from androguard.misc import AnalyzeAPK
from androguard.core.apk import APK
from androguard.core.dex import DEX
from androguard.core.analysis.analysis import Analysis
from androguard.core.analysis.analysis import ClassAnalysis
from typing import Optional, Tuple

_SCRAMBLED_NAME_RE: re.Pattern = re.compile(r"(?:\w+(?:/\w+)+)|(?:^\w{,2}$)")
_SCRAMBLED_WHITELIST = [
    'android',
    'androidx',
    'java',
    'kotlin'
]


def strip_class_name(class_name: str) -> str:
    matches = _SCRAMBLED_NAME_RE.findall(class_name)
    if len(matches) == 0:
        return class_name
    for group in matches:
        if group.split('/')[0] not in _SCRAMBLED_WHITELIST and group.split('/')[0][1:] not in _SCRAMBLED_WHITELIST:
            class_name = class_name.replace(group, '')
    return class_name


def get_apk_cache(apk_path: str, temp_path: str) -> Tuple[Optional[APK], Optional[Analysis]]:
    temp_path = pathlib.Path(temp_path) / os.path.basename(apk_path)
    if temp_path.exists():
        try:
            apk_cache_path = temp_path / 'apk'
            analysis_path = temp_path / 'analysis'
            with apk_cache_path.open('rb') as f:
                apk = pickle.load(f)
            with analysis_path.open('rb') as f:
                analysis = pickle.load(f)
            return apk, analysis
        except:
            pass
    return None, None


def save_apk_cache(apk_path: str, temp_path: str, apk: APK, analysis: Analysis) -> None:
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    temp_path = pathlib.Path(temp_path) / os.path.basename(apk_path)
    if not temp_path.exists():
        temp_path.mkdir()
    apk_cache_path = temp_path / 'apk'
    analysis_path = temp_path / 'analysis'
    with apk_cache_path.open('wb') as f:
        pickle.dump(apk, f)
    with analysis_path.open('wb') as f:
        pickle.dump(analysis, f)


def extract_apk(apk_path: str, temp_path: str) -> Tuple[Optional[APK], Optional[Analysis]]:
    cprint("[+] Running androguard to decompile the apk.", "green")
    try:
        apk, _, dx = AnalyzeAPK(apk_path)
    except Exception as e:
        print(e)
        cprint(f"Error processing {apk_path}.", "red")
        return None, None
    # save_apk_cache(apk_path, temp_path, apk, dx)
    cprint("[+] Androguard processed the apk.", "green")
    return apk, dx


def get_stripped_ast(class_analysis: ClassAnalysis) -> str:
    def _strip(value: Any) -> Any:
        if isinstance(value, str):
            return strip_class_name(value)
        if isinstance(value, list):
            return [_strip(item) for item in value]
        if isinstance(value, tuple):
            return tuple(_strip(item) for item in value)
        if isinstance(value, dict):
            return {key: _strip(value[key]) for key in value.keys()}
        if isinstance(value, bool) or isinstance(value, int) or isinstance(value, float) or value is None:
            return value
        raise ValueError(f"Wrong type! {type(value)}")

    ast = class_analysis.get_class().get_ast()

    return _strip(ast)


def get_strings(class_analysis: ClassAnalysis) -> List[str]:
    def _get_strings(value: Any) -> List[str]:
        if isinstance(value, list):
            if len(value) == 3 and value[0] == 'Literal' and value[2] == ('java/lang/String', 0):
                return [value[1]]
            return [string for item in value for string in _get_strings(item)]
        if isinstance(value, dict):
            return [item for key in value.keys() for item in _get_strings(value[key])]
        return []

    return _get_strings(class_analysis.get_class().get_ast())
