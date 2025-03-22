from utils import utils

def main():
    x, y = 5, 10
    print(f"{x} + {y} = {utils.add(x, y)}")
    print(f"{x} * {y} = {utils.multiply(x, y)}")

if __name__ == "__main__":
    main()
