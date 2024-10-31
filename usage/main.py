from typing import Any

from pydantic import BaseModel, field_validator, Field


class Test(BaseModel):
    name: str
    required_info: str = Field()

    @field_validator('name')
    def validate_name(cls, name):
        if name is None:
            raise ValueError('name cannot be None')
        return name

    def model_post_init(self, __context: Any) -> None:
        """
        model_post_init 후에는 validation 진행안함
        validation 진행후 model_post_init 진행
        :param __context:
        :return:
        """
        self.name = "after_init"
        self.required_info = "after_init_required_info"

# name_is_none = Test(name=None)
# print(name_is_none)
name_is_not_none = Test(name="hello name is not None",required_info="required_info")
print(name_is_not_none)
