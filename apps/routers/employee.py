from fastapi import APIRouter, Request, Depends

from config import manager
from config import templates

api = APIRouter()


@api.get('/public')
async def public_page(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('public.html', context)


@api.get('/private')
async def private_page(request: Request, current_user=Depends(manager)):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('private.html', context)
