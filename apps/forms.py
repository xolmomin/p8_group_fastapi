from fastapi import Form, File, UploadFile
from pydantic import BaseModel


class EmployeeForm(BaseModel):
    name: str
    email: str
    address: str
    phone: str
    image: UploadFile

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            email: str = Form(...),
            address: str = Form(...),
            phone: str = Form(...),
            image: UploadFile = File(...)
    ):
        return cls(name=name, email=email, address=address, phone=phone, image=image)
