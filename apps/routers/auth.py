from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
import shutil
from apps import models
from apps import forms
from config import templates
from database import get_db

auth = APIRouter()


@auth.get('/login', name='login')
def auth_login(request: Request):
    context = {
        'request': request
    }
    return templates.TemplateResponse('auth/login.html', context)


@auth.post('/login', name='login')
def auth_login(
        request: Request,
        response: Response,
        form: forms.LoginForm = Depends(forms.LoginForm.as_form),
        db: Session = Depends(get_db)
):
    # TODO to finish
    if form.is_valid(db):
        pass
    context = {
        'request': request
    }
    return templates.TemplateResponse('auth/login.html', context)


@auth.get('/register', name='register')
def register_page(request: Request):
    context = {
        'request': request
    }
    return templates.TemplateResponse('auth/register.html', context)


@auth.post('/register', name='register')
def register_page(
        request: Request,
        form: forms.RegisterForm = Depends(forms.RegisterForm.as_form),
        db: Session = Depends(get_db)
):
    if errors := form.is_valid(db):
        context = {
            'errors': errors,
            'request': request
        }
        return templates.TemplateResponse('auth/register.html', context)
    else:
        data = form.dict(exclude_none=True)
        user = models.Users(**data)
        db.add(user)
        context = {
            'request': request
        }
        # TODO to finish
        return RedirectResponse('')
