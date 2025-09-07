import pandas
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple Database server")
    args = parser.parse_args()
    print(args.accumulate(args.integers))
