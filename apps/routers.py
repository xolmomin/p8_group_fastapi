from fastapi import APIRouter, Request, Depends
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
import shutil
from apps import forms
from apps import models
from database import get_db

api = APIRouter()
templates = Jinja2Templates(directory="templates")


@api.get('/', name='employees_list')
def get_employees_list(request: Request, page: int = 1, size: int = 5, db: Session = Depends(get_db)):
    employees = db.query(models.Employee).order_by(desc(models.Employee.id)).limit(size).offset((page - 1) * size)
    count = db.query(models.Employee).count()
    context = {
        'page': page,
        'size': size,
        'count': count,
        'request': request,
        'employees': employees
    }
    return templates.TemplateResponse('main.html', context)


@api.post('/', name='create_employee')
def create_employee(
        form: forms.EmployeeForm = Depends(forms.EmployeeForm.as_form),
        db: Session = Depends(get_db)
):
    data = form.dict(exclude_unset=True)
    if len(form.image.filename):
        file_url = 'media/employee/' + form.image.filename
        with open(file_url, "wb") as buffer:
            shutil.copyfileobj(form.image.file, buffer)
        data.update({'image': file_url})

    db.add(models.Employee(**data))
    return RedirectResponse('/', status.HTTP_303_SEE_OTHER)


@api.get('/position/{pk}')
def get_employee(pk: int, db: Session = Depends(get_db)):
    result = db.query(models.Position).all()
    return result


@api.get('/company')
def get_employee(db: Session = Depends(get_db)):
    result = db.query(models.Position).all()
    return result
