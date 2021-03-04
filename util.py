import time


def stopwatch(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__

        def arg_name(arg):
            try:
                return f"{type(arg.__self__).__name__}#{arg.__name__}"
            except AttributeError:
                return arg.__name__

        arg_str = ', '.join(arg_name(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked
