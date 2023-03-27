import tests

if __name__ == "__main__":
    for name in tests.__dict__:
        if name.startswith("test"):
            test_func = getattr(tests, name)
            if callable(test_func):
                test_func()