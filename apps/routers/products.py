import os
import shutil

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

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


def save_image(images, product_id, db: Session):
    if isinstance(images, list):
        images_list = []
        for image in images:
            if len(image.filename):
                folder = 'media/product/'
                if not os.path.exists(folder):
                    os.mkdir(folder)
                file_url = folder + image.filename
                with open(file_url, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                    images_list.append(models.ProductImage(product_id=product_id, image=file_url))

        db.add_all(images_list)
        db.commit()


@product_api.post('/add', name='product_add')
async def product_add(
        request: Request,
        form: ProductForm = Depends(ProductForm.as_form),
        db: Session = Depends(get_db),
        current_user=Depends(manager)
):
    data = form.dict(exclude_none=True)
    images = data.pop('images')
    data.update({'author_id': current_user.id})
    product = models.Product(**data)
    db.add(product)
    db.commit()
    save_image(images, product.id, db)
    context = {
        'request': request,
    }
    return templates.TemplateResponse('products/product-add.html', context)
