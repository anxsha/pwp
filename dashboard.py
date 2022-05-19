from typing import List

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from textblob._text import encode_utf8
from werkzeug.exceptions import abort

import models
from auth import login_required
from database import get_db

bp = Blueprint('dashboard', __name__)


@bp.route('/dashboard')
@login_required
def dashboard_index():
    db = get_db()

    # product = db.query(models.Product).first()
    #
    # price_changes = product.price_changes
    #
    # prices = list()
    # dates = list()
    #
    # for price_change in price_changes:
    #     prices.append(price_change.price)
    #     dates.append(price_change.datetime_of_change)
    #
    # fig = figure(plot_width=600, plot_height=600, x_axis_type='datetime')
    # fig.line(
    #     x=dates,
    #     y=prices,
    #     color='red',
    #     line_width=1.5
    # )
    #
    # js_resources = INLINE.render_js()
    # css_resources = INLINE.render_css()
    #
    # script, div = components(fig)
    return render_template(
        'dashboard.html',
    )


@bp.route('/dashboard/brands', defaults={'id': None})
@bp.route('/dashboard/brand/<id>')
@login_required
def brands(id):
    db = get_db()

    rows_per_page = 20

    if not id:
        page = request.args.get('page', default=1, type=int)
        if page < 1:
            page = 1
        total_count = db.query(models.Brand).count()
        brands_paginated = db.query(models.Brand).order_by(models.Brand.name) \
            .offset((int(page) - 1) * rows_per_page).limit(rows_per_page).all()
        return render_template('dashboard-brands.html', brands=brands_paginated, total_count=total_count, page=page,
                               rows_per_page=rows_per_page)
    # return render_template('dashboard-categories.html', categories=cats)


@bp.route('/dashboard/categories', defaults={'id': None})
@bp.route('/dashboard/categories/<id>')
@login_required
def categories(id):
    db = get_db()

    cats = db.query(models.ProductCategory).all()

    rows_per_page = 20

    if id:
        page = request.args.get('page', default=1, type=int)
        if page < 1:
            page = 1
        cats = db.query(models.ProductCategory).all()
        category = db.query(models.ProductCategory).get(id)  # type: models.ProductCategory
        total_count = len(category.products)
        cat_products = db.query(models.Product).order_by(models.Product.name) \
            .filter(models.Product.category.has(name=category.name)) \
            .offset((int(page) - 1) * rows_per_page).limit(rows_per_page).all()
        return render_template('dashboard-category.html', category=category, categories=cats,
                               cat_products=cat_products, total_count=total_count, page=page,
                               rows_per_page=rows_per_page)
    return render_template('dashboard-categories.html', categories=cats)


@bp.route('/dashboard/products', defaults={'id': None}, methods=['GET', 'POST'])
@bp.route('/dashboard/products/<id>')
@login_required
def products(id):
    db = get_db()

    if request.method == 'POST':
        name = request.form['product-name']
        matching_products = db.query(models.Product).filter(models.Product.name.contains(name)).limit(20)
        return render_template('dashboard-products.html', matching_products=matching_products)
    if id:
        product = db.query(models.Product).get(id)

        price_changes = product.price_changes

        prices = list()
        dates = list()

        for price_change in price_changes:
            prices.append(price_change.price)
            dates.append(price_change.datetime_of_change)

        fig = figure(plot_width=600, plot_height=600, x_axis_type='datetime')
        fig.line(
            x=dates,
            y=prices,
            color='red',
            line_width=1.5
        )

        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        script, div = components(fig)
        html = render_template(
            'dashboard-product.html',
            product=product,
            plot_script=script,
            plot_div=div,
            js_resources=js_resources,
            css_resources=css_resources,
        )
        return encode_utf8(html)

    return render_template('dashboard-products.html')
