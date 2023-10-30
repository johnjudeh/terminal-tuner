import tests
from time import time


if __name__ == "__main__":
    start = time()
    for name in tests.__dict__:
        if name.startswith("test"):
            test_func = getattr(tests, name)
            if callable(test_func):
                test_func()
    end = time()
    print(f"Tests ran in {end - start} seconds")
