from pydantic import BaseModel, field_validator


class Test(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(cls, name):
        if name is None:
            raise ValueError('name cannot be None')
        return name


#name_is_none = Test(name=None)
#print(name_is_none)
name_is_not_none = Test(name="hello name is not None")
print(name_is_not_none)
