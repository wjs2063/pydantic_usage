from functools import wraps


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result

    return wrapper


@my_decorator
def my_function():
    """This is My Function"""
    print("Hello")
    return "My_Function"


print(my_function.__name__)
print(my_function.__doc__)



def _test_decorator(func):

    @wraps(func)