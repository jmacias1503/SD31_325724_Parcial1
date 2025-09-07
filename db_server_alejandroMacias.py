import pandas
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Hola desde el server")
    args = parser.parse_args()
    print(args.accumulate(args.integers))
