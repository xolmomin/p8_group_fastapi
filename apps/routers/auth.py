from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse

from apps import forms, models
from apps.utils.token import send_email, make_token
from config import manager, templates
from database import get_db

auth = APIRouter()


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
            return RedirectResponse("/login", status.HTTP_302_FOUND)

        access_token = manager.create_access_token(
            data={"sub": user.email}
        )
        resp = RedirectResponse("/", status.HTTP_302_FOUND)
        manager.set_cookie(resp, access_token)
        return resp


@auth.get('/register', name='register')
def register_page(request: Request, db: Session = Depends(get_db), ):
    user = db.query(models.Users).first()
    token = make_token(user)
    print(token)
    context = {
        'request': request
    }
    return templates.TemplateResponse('auth/register.html', context)


@auth.post('/register', name='register')
def register_page(
        request: Request,
        background_task: BackgroundTasks,
        form: forms.RegisterForm = Depends(forms.RegisterForm.as_form),
        db: Session = Depends(get_db),
):
    if errors := form.is_valid(db):
        context = {
            'errors': errors,
            'request': request
        }
        return templates.TemplateResponse('auth/register.html', context)
    else:
        data = form.dict(exclude_none=True)
        background_task.add_task(send_email, data['email'], data['name'])
        user = models.Users(**data)
        db.add(user)
        db.commit()
        return RedirectResponse('/login', status.HTTP_303_SEE_OTHER)


# https://localhost:8000/e26781dguc62gug176dg716gs7126s6712g

'''

author product qoshish joyida

activate user, forgot password
product images,
product detail

profile update
profile page

cart page bolishi kk ishlashi ham kk

product-list pagination
not found 404 page

'''
