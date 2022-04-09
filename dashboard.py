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

    product = db.query(models.Product).first()

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
        'dashboard.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


@bp.route('/dashboard/categories')
@login_required
def categories():

    db = get_db()

    # db.query(models.ProductCategory)
