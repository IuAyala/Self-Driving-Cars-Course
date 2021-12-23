import contextlib


@contextlib.contextmanager
def debug_logging(level):
    print("inside function" + str(level))


with debug_logging(["aaa", "bbbb"]):
    print("aaaaaaaa")
