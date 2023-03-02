import json

from fastapi import APIRouter, Request, Depends, Response
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.authentication import BaseUser
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
import shutil
from apps import models
from apps import forms
from config import templates
from database import get_db
from config import manager

auth = APIRouter()


@manager.user_loader()
def load_user(email: str):
    db = next(get_db())
    user = db.query(models.Users).where(models.Users.email == email).first()
    return user


@auth.get('/login', name='login')
def auth_login(request: Request):
    context = {
        'request': request
    }
    return templates.TemplateResponse('auth/login.html', context)


@auth.get('/logout', name='logout')
def auth_logout(request: Request, response: Response, current_user=Depends(manager)):
    response = templates.TemplateResponse("auth/login.html", {"request": request})
    response.delete_cookie("access-token")
    return response


@auth.post('/login', name='login')
def auth_login(
        request: Request,
        response: Response,
        form: forms.LoginForm = Depends(forms.LoginForm.as_form),
        db: Session = Depends(get_db)
):
    errors, user = form.is_valid(db)
    if errors:
        context = {
            'request': request,
            'errors': errors
        }
        return templates.TemplateResponse('auth/login.html', context)
    else:

        # user = load_user(form.email)
        if not user or form.password != user.password:
            RedirectResponse("/login", status.HTTP_302_FOUND)

        access_token = manager.create_access_token(
            data={"sub": user.email}
        )
        resp = RedirectResponse("/", status.HTTP_302_FOUND)
        manager.set_cookie(resp, access_token)
        return resp


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
    db = next(get_db())

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
