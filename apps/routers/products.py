from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from apps import models
from apps.forms import ProductForm
from config import manager
from config import templates
from database import get_db

product_api = APIRouter()


@product_api.get('/', name='product_list')
async def public_page(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(-models.Product.id)
    context = {
        'request': request,
        'products': products
    }
    return templates.TemplateResponse('products/product-list.html', context)


@product_api.get('/detail/{pk}', name='product_detail')
async def private_page(request: Request, pk: int):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('products/product-details.html', context)


@product_api.get('/add', name='product_add')
async def private_page(request: Request, current_user=Depends(manager)):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('products/product-add.html', context)


@product_api.post('/add', name='product_add')
async def product_add(
        request: Request,
        form: ProductForm = Depends(ProductForm.as_form),
        db: Session = Depends(get_db),
        current_user=Depends(manager)
):
    data = form.dict(exclude_none=True)
    db.add(models.Product(**data))
    db.commit()
    context = {
        'request': request,
    }
    return templates.TemplateResponse('products/product-add.html', context)
