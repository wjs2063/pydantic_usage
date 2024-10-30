from pydantic import BaseModel, model_validator
from functools import singledispatchmethod, singledispatch
import base64
from typing import Dict
import json

important_data = {"a": "this is decoded str"}
json_str = json.dumps(important_data).encode("utf-8")
_base64_encode_str = base64.b64encode(json_str)


class PostInitTest(BaseModel):
    a: str
    b: str
    important_data: dict

    @model_validator(mode='before')
    @classmethod
    def validate_and_modify_data(cls, values):
        if values.get("important_data"):
            values["important_data"] = cls.decode_important_data(values.get("important_data"))
        return values


    @singledispatchmethod
    @classmethod
    def decode_important_data(cls, important_data):
        """
        import_data 의 type 에 따라 다른행동
        :param important_data:
        :return:
        """
        raise ValueError("important_data is not valid type, must be string or NoneType")

    @decode_important_data.register
    @classmethod
    def _(cls, important_data: str) -> Dict:
        """
        일반 문자열일때는 dict 로 리턴
        :param important_data:
        :return:
        """
        return dict()

    @decode_important_data.register
    @classmethod
    def _(cls, important_data: bytes) -> Dict:
        """
        base64 기반 bytes 일때는 decode 작업 진행
        :param important_data:
        :return:
        """
        return json.loads(base64.b64decode(important_data).decode("utf-8"))

    @decode_important_data.register
    @classmethod
    def _(cls, important_data: None) -> Dict:
        """
        None 일떄는 dict 로 바꿔서 진행
        :param important_data:
        :return:
        """
        return dict()


post_init_test = PostInitTest(a="a", b="b", important_data=_base64_encode_str)

print(post_init_test)
