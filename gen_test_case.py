import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="gen_test_case.py",
        description="Testing tool for the first IPP Project",
        epilog="Author: Nick Settler (xmoise01)"
    )

    parser.add_argument("-n", "--name", action="store", help="Name of the test case", required=True)

    args = parser.parse_args()

    return args.name


def main():
    name = parse_args()

    with open(f"{name}.src", "w") as file:
        file.write("")

    with open(f"{name}.xml", "w") as file:
        file.write("")

    with open(f"{name}.code", "w") as file:
        file.write("0")

    pass


if __name__ == "__main__":
    main()
