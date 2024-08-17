import argparse
import os
from timeit import default_timer
from termcolor import cprint
from androguard.core.androconf import is_android
from androguard.core.analysis.analysis import Analysis
from androguard.util import set_log
from androguard.core.apk import APK
from androguard.misc import AnalyzeAPK
from apkdiff.utils import extract_apk
from apkdiff.common import *
from apkdiff.Comparer import Comparer

set_log('CRITICAL')


def compare(apk1: APK, dex1: Analysis, apk2: APK, dex2: Analysis) -> Comparer:
    result = Comparer(APKAnalysis(apk1, dex1), APKAnalysis(apk2, dex2))
    result.compare()
    return result


def main():
    start = default_timer()
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--path1", "-p1", dest="path1", type=str, required=True)
    parser.add_argument("--path2", "-p2", dest="path2", type=str, required=True)
    parser.add_argument("--jadx", "-j", dest="jadx", type=str, required=True)
    parser.add_argument("--temp_path", "-t", dest="temp_path", type=str, required=False, default='cache')
    args = parser.parse_args()
    apk1, dex1 = extract_apk(args.path1, args.temp_path)
    if apk1 is None:
        return -1
    apk2, dex2 = extract_apk(args.path2, args.temp_path)
    if apk2 is None:
        return -1
    result = compare(apk1, dex1, apk2, dex2)
    print('The results are: ')
    print(result)
    print(f"It took {default_timer() - start} seconds to complete the run.")


if __name__ == "__main__":
    exit(main())
