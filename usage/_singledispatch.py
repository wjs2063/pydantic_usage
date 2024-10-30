from functools import singledispatch, singledispatchmethod
from pydantic import BaseModel


class SingleDispatchTest(BaseModel):
    a: str | int

    def __init__(self, **data):
        super().__init__(**data)

    @singledispatchmethod
    def post_init(self, data):
        pass

    @post_init.register
    def _(self, data: int):
        print("this is int type")
        return data

    @post_init.register
    def _(self, data: str):
        print("this is str type")
        return data


singleddispatch_test = SingleDispatchTest()
singleddispatch_test.post_init("this is string test")
singleddispatch_test.post_init(3)
