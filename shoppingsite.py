"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, session, render_template, redirect, flash
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = '\x03\xdf\x06\xd6\xe5\xd1j#\xc0\xf4\x84\xc1G0\xef\xa0\xcaK\xfa\xeb\xb3Z\xed\xe8'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # have a for loop that loops through the entire list of ids in session['cart']
    # do something like this  melon_data_by_id = melons.get_by_id(item)
    # then put it into the empty dictionary called melon_data, and assemble the dictionary
    # to hold a bunch of dictionaries

    # id,
    # melon_type,
    # common_name,
    # price,
    # img_url,
    # color,
    # seedless


    # holds all melon data to return
    melons_in_cart = {}

    # total_melon is the total for each melon type
    total_melon = 0
    # total_order_cost is the total for the entire order itself
    total_order_cost = 0
    # get a list of melon ids
    for id in session['cart']:
        melon_data_by_id = melons.get_by_id(id)
        if id in melons_in_cart:
            qty = melons_in_cart[id]['qty'] + 1
            melons_in_cart[id]['qty'] += 1
            melons_in_cart[id]['total_melon'] = melons_in_cart[id]['price'] * melons_in_cart[id]['qty']
        else:
            # move this line down, dawg!
            # total_melon = melons_in_cart[id].price
            melons_in_cart[id] = { 
                                    'melon_type': melon_data_by_id.melon_type,
                                    'common_name': melon_data_by_id.common_name,
                                    'price': melon_data_by_id.price,
                                    'img_url': melon_data_by_id.image_url,
                                    'color': melon_data_by_id.color,
                                    'seedless': melon_data_by_id.seedless,
                                    'qty': 1,
                                    'total_melon': melon_data_by_id.price
                                 }
        total_order_cost = total_order_cost + (melons_in_cart[id]['price'] * melons_in_cart[id]['qty'])

    return render_template("cart.html",
                            melons_in_cart=melons_in_cart,
                            total_order_cost=total_order_cost)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    if session['cart']:
        session['cart'].append(id)
    else:
        # create an empty list inside of the cart dictionary
        session['cart'] = []

        # append the id to the cart
        session['cart'].append(id)


    # for id in session['cart']:
    print "AAAAAAAAAAAAAAAAAAAAAA", session

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
