from fastapi import APIRouter, Request, Depends
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
import shutil
from apps import forms
from apps import models
from config import templates
from database import get_db

api = APIRouter()


@api.get('/', name='employees_list')
def get_employees_list(request: Request, db: Session = Depends(get_db)):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('main.html', context)

#
# @api.post('/', name='create_employee')
# def create_employee(
#         form: forms.EmployeeForm = Depends(forms.EmployeeForm.as_form),
#         db: Session = Depends(get_db)
# ):
#     data = form.dict(exclude_unset=True)
#     if len(form.image.filename):
#         file_url = 'media/employee/' + form.image.filename
#         with open(file_url, "wb") as buffer:
#             shutil.copyfileobj(form.image.file, buffer)
#         data.update({'image': file_url})
#
#     db.add(models.Employee(**data))
#     return RedirectResponse('/', status.HTTP_303_SEE_OTHER)
#
#
# @api.get('/position/{pk}')
# def get_employee(pk: int, db: Session = Depends(get_db)):
#     result = db.query(models.Position).all()
#     return result
#
#
# @api.get('/company')
# def get_employee(db: Session = Depends(get_db)):
#     result = db.query(models.Position).all()
#     return result
#