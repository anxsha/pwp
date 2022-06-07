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

        sales = product.sales

        sale_quantity = list()
        sale_date = list()
        sale_price = list()

        for sale in sales:
            sale_price.append(sale.sale_price)
            sale_quantity.append(sale.sale_quantity)
            sale_date.append(sale.datetime_of_sale)

        deliveries = product.deliveries

        delivery_quantity = list()
        delivery_date = list()
        delivery_price = list()

        for delivery in deliveries:
            delivery_price.append(delivery.unit_price)
            delivery_quantity.append(delivery.quantity)
            delivery_date.append(delivery.datetime_of_delivery)

        prices = list()
        dates = list()

        for price_change in price_changes:
            prices.append(price_change.price)
            dates.append(price_change.datetime_of_change)

        fig_pc = figure(plot_width=600, plot_height=600, x_axis_type='datetime')
        fig_pc.line(
            x=dates,
            y=prices,
            color='red',
            line_width=1.5
        )

        fig_sales = figure(plot_width=600, plot_height=600, x_axis_type='datetime')
        fig_sales.line(
            x=sale_date,
            y=sale_quantity,
            color='green',
            line_width=1.5
        )

        fig_del = figure(plot_width=600, plot_height=600, x_axis_type='datetime')
        fig_del.line(
            x=delivery_date,
            y=delivery_quantity,
            color='blue',
            line_width=1.5
        )


        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        script_pc, div_pc = components(fig_pc)
        script_sales, div_sales = components(fig_sales)
        script_del, div_del = components(fig_del)
        html = render_template(
            'dashboard-product.html',
            product=product,
            plot_script_pc=script_pc,
            plot_script_sales=script_sales,
            plot_script_del=script_del,
            plot_div_pc=div_pc,
            plot_div_sales=div_sales,
            plot_div_del=div_del,
            js_resources=js_resources,
            css_resources=css_resources,
        )
        return encode_utf8(html)

    return render_template('dashboard-products.html')
