from pydantic import ValidationError, validate_call


@validate_call
def say_hello(user: str, seq: int) -> dict:
    return dict()

# validation check

say_hello(user="user_test", seq=1)

say_hello(user="3", seq=2)
