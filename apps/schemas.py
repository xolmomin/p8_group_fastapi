from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str
    image: str

    class Config:
        orm_mode = True
