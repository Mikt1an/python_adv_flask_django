from pydantic import (BaseModel,
                      EmailStr,
                      ValidationError,
                      model_validator,
                      field_validator,
                      Field)


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must only contain letters")
        return v

    @model_validator(mode="after")
    def validate_user_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(f"If user is employed, age must be between 18 and 65 = {self.age}")
        return self


def register_user(json_input: str) -> str:
    try:
        user = User.model_validate_json(json_input, strict=True)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return f"Validation error: {e}"


json_input = [ """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}""",
"""{
    "name": "Anna Swarowsky",
    "age": 30,
    "email": "anna.swa@example.com",
    "is_employed": true,
    "address": {
        "city": "Innschbruck",
        "street": "strasse 15",
        "house_number": 5
    }
}""",
"""{
    "name": "Mark Louis",
    "age": 10,
    "email": "mark.lo@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "115th street",
        "house_number": 3
    }
}""",
]



for user_json in json_input:
    result = register_user(user_json)
    print(result)
    print("*" * 50)
