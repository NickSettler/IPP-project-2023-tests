import os
import argparse
import subprocess
from termcolor import colored
from lxml import etree
from xmldiff import main as xmldiff


def help():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Testing tool for the first IPP Project",
        epilog="Author: Nick Settler (xmoise01)",
        add_help=False
    )

    parser.add_argument("--help", "-h", action="help", help=argparse.SUPPRESS)
    parser.add_argument("-i", "--interpret", action="store", help="PHP 8.1 interpreter", required=True)
    parser.add_argument("-s", "--source", action="store", help="Path to parse.php file", required=True)

    args = parser.parse_args()
    return [args.interpret, args.source]


class Test:
    def __init__(self, src):
        self.name = src.replace(".src", "").split('/')[-1]

        self.src_file = src
        self.out_file = src.replace(".src", ".out")
        self.rc_file = src.replace(".src", ".code")

        self.actual_rc = ""
        self.actual_out = ""

        with open(self.out_file, "r") as file:
            self.expected_out = file.read()

        with open(self.rc_file, "r") as file:
            self.expected_rc = file.read()

    def __str__(self):
        return self.name


class TestRunner:
    def __init__(self, interpret, source):
        self.interpret = interpret
        self.source = source

    def run(self, test):
        with open(test.src_file, "r") as file:
            try:
                result = subprocess.run([self.interpret, self.source], stdin=file, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL)
                test.actual_rc = result.returncode
                test.actual_out = result.stdout.decode("utf-8")
            except subprocess.CalledProcessError as e:
                test.actual_rc = e.returncode
        pass


def get_tests():
    tests = []

    for root, dirs, files in os.walk("tests"):
        for file in files:
            if file.endswith(".src"):
                tests.append(Test(os.path.join(os.path.dirname(os.path.abspath(__file__)), root, file)))

    return tests


def main():
    interpret, source = help()

    tests = get_tests()
    tests.sort(key=lambda x: x.src_file)

    tests_runner = TestRunner(interpret, source)

    succeed = 0
    failed = 0

    xml_parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

    for test in tests:
        tests_runner.run(test)

        if int(test.actual_rc) != int(test.expected_rc):
            failed += 1
            print(colored(f"Test {test.name} failed: RC {test.actual_rc} != {test.expected_rc}", "red"))
            continue

        if test.actual_out.strip() and test.expected_out.strip():
            left_tree = etree.XML(bytes(bytearray(test.actual_out, encoding='utf-8')), parser=xml_parser)
            right_tree = etree.XML(bytes(bytearray(test.expected_out, encoding='utf-8')), parser=xml_parser)
            output_diff = xmldiff.diff_trees(left_tree, right_tree)

            if len(output_diff):
                failed += 1
                print(colored(f"Test {test.name} failed: OUT {test.actual_out} != {test.expected_out}", "red"))
                continue

        elif test.actual_out.strip() != test.expected_out.strip():
            failed += 1
            print(colored(f"Test {test.name} failed: OUT {test.actual_out} != {test.expected_out}", "red"))
            continue

        succeed += 1
        print(colored(f"Test {test.name} passed", "green"))

    percent = succeed / (succeed + failed) * 100
    print(colored(f"Passed: {succeed}\t\tFailed: {failed}\t\tPercent: {percent:.2f}%",
                  "green" if failed == 0 else percent > 50 and "yellow" or "red"))

    stats_length = 54
    stats = int(percent / 100 * stats_length)
    print(colored(f"[{'=' * stats}{' ' * (stats_length - stats)}] {percent:.2f}%",
                  "green" if failed == 0 else percent > 50 and "yellow" or "red"))

    pass


if __name__ == '__main__':
    main()
