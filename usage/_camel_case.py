from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class CamelCaseTest(BaseModel):
    snake_case: str

    # Serialization 할때 to_camel 로
    model_config = ConfigDict(alias_generator=AliasGenerator(
        serialization_alias=to_camel
    ))


camel_case_test = CamelCaseTest(snake_case="hello_world")
print(camel_case_test.dict())

# camelCase 로 Serialization
print(camel_case_test.model_dump(by_alias=True))