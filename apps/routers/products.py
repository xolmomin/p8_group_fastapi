import os
import shutil

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse

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


async def get_or_create(db: Session, model, **kwargs) -> tuple:
    try:
        return db.query(model).filter_by(**kwargs).one(), False
    except NoResultFound as e:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
    return instance, True


async def get_or_404(db: Session, model, **kwargs):
    try:
        return db.query(model).filter_by(**kwargs).one()
    except NoResultFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


async def create_or_delete(db: Session, model, **kwargs):
    try:
        instance = db.query(model).filter_by(**kwargs).one()
    except NoResultFound as e:
        instance = model(**kwargs)
        db.add(instance)
    else:
        db.delete(instance)

    db.commit()


@product_api.get('/favorite/{pk}', name='add_favorite')
async def product_add(
        pk: int,
        db: Session = Depends(get_db),
        current_user=Depends(manager)
):
    product = await get_or_404(db, models.Product, id=pk)
    favorite, created = await get_or_create(db, models.Favorite, product=product, user=current_user)
    if not created:
        db.delete(favorite)
        db.commit()

    return RedirectResponse('/', status.HTTP_303_SEE_OTHER)
