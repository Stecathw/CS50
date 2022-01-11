import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    
    transactions = db.execute(
        'SELECT symbol, name, SUM(shares) AS shares, price, SUM(total) AS total FROM transactions where user_id=? GROUP BY name', user_id)
    for transaction in transactions:
        transaction['price'] = usd(transaction['price'])
        transaction['total'] = usd(transaction['total'])
    
    row = db.execute('SELECT * FROM users WHERE id=?', user_id)
    cash = row[0]['cash']
    
    row_sum = db.execute('SELECT SUM(total) FROM transactions WHERE user_id=?', user_id)
    total_stock = row_sum[0]['SUM(total)']
    if total_stock is None:
        amount = float(cash)
    else:
        amount = cash + float(total_stock)
    
    return render_template("/index.html", transactions=transactions, cash=usd(cash), amount=usd(amount))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    if request.method == "POST":
        
        user_id = session["user_id"]
        
        # Users input, symbol and shares
        symbol = request.form.get('symbol').upper()
        shares = request.form.get('shares')
        
        # Finding stock
        stock = lookup(symbol)
        
        # Handling inputs errors
        if not symbol:
            return apology("Missing symbol", 400)
        elif not stock:
            return apology("Invalid symbol", 400)
        elif shares is None or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number", 400)
            
        # Buying action :
        name = str(stock['name'])
        price = float(stock['price'])
        total_price = int(shares)*price
        
        # Query users db to find user's cash.
        try:
            row = db.execute('SELECT * FROM users WHERE id=?', user_id)
            user_cash = row[0]['cash']
        except:
            return apology("Server error", 403)
        
        # Checking if user has enough cash
        if user_cash < total_price:
            return apology("Not enough money", 400)
        user_cash -= total_price
        
        # Updating databases users/transactions/history according to buy action:
        try:
            db.execute('UPDATE users SET cash=? WHERE id=?', user_cash, user_id)
            db.execute('INSERT INTO transactions (user_id, symbol, shares, price, name, total) VALUES (?, ?, ?, ?, ?, ?)', 
                        user_id, symbol, shares, price, name, total_price)
            db.execute('INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)', user_id, symbol, shares, price)
        except:
            return apology("Server error", 403)
        
        # Return to portfolio    
        flash("Bought !")   
        return redirect("/")
    
    return render_template("/buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    
    user_id = session["user_id"]
    
    history = db.execute("SELECT * FROM history WHERE user_id =? ORDER BY transacted DESC", user_id)
    
    return render_template("/history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        
        # From input search for stock informations
        symbol = request.form.get('symbol').upper()
        stock = lookup(symbol)
        
        # Handling missing or inexesting symbol input
        if stock is None:
            return apology('Invalid symbol', 400)
            
        # Converting to dollar format, could also be done in templates with "| usd"
        stock['price'] = usd(stock['price'])
        
        # Return to quoted.html with explicit informations and price.
        return render_template("/quoted.html", stock=stock)
        
    return render_template("/quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        
        # Collecting user imput
        username = request.form.get('username')
        password1 = request.form.get('password')
        password2 = request.form.get('confirmation')
        
        # Opening users database and search if username exist.
        try:
            is_existing = db.execute("SELECT username FROM users GROUP BY USERNAME HAVING username=?", username)
        except:
            return apology("Server error", 403)
        
        # Handling errors
        if not username:
            return apology("Missing username", 400)
        elif is_existing:
            return apology("Username already exist", 400)
        elif not password1:
            return apology("Missing password", 400)
        elif not password2:
            return apology("Missing password confirmation", 400)
        elif password1 != password2:
            return apology("Mismatching passwords", 400)
        else:
            # No errors, we can update users database accordingly to inputs
            
            # Generating hash password
            password = generate_password_hash(password1, method='sha256')
            
            try:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
            except:
                return apology("Server error", 403)
                
            # Return to home page for login
            flash('Registered !')
            return redirect(url_for("login"))
    
    return render_template("/register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    
    if request.method == "POST":
        
        # User inputs
        symbol = request.form.get('symbol')
        shares = int(request.form.get('shares'))
        
        # Handling errors :
        if not request.form.get('symbol'):
            return apology("Missing stock", 400)
        elif not request.form.get('shares'):
            return apology("Missing share(s)", 400)
        
        # Selecting user's cash and total price of selected owned stock
        try:
            cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)
            row = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE symbol=? AND user_id=?", symbol, user_id)
        except:
            return apology("Server error")
        
        # How much shares is owned
        max_shares = int(row[0]['shares'])
        
        # Checking if possible to sells this quantity
        if max_shares < shares:
            return apology("Do not own that many stocks", 400)
        
        # Stock price
        price = float(lookup(symbol)['price'])
        
        # Amount of selling operation
        amount = shares*price
        
        # Updating user's cash after selling operation
        new_cash = float(cash[0]['cash']) + amount
        
        # Updating user's shares of that stock
        new_shares = int(row[0]['shares']) - shares
        
        # Updating user's total price of owned shares
        new_total = new_shares*price
        
        # After sell operation, if owned shares isn't null, updating transactions database accordingly
        if new_shares != 0:
            transactions = db.execute("UPDATE transactions SET shares=?, total=? WHERE symbol=?", new_shares, new_total, symbol)
        # Otherwise, deleting user's transaction from database
        else:
            transactions = db.execute("DELETE from transactions WHERE id=? AND symbol=?", user_id, symbol)
        
        # Update users and history transaction
        try:
            db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)
            db.execute('INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)', user_id, symbol, -shares, price)
        except:
            return apology("Server error")
        
        # Return to portfolio
        flash("Sold !")
        return redirect("/")
    
    # Listing possible stocks' selections in template
    try:
        rows = db.execute('SELECT symbol FROM transactions WHERE user_id=? GROUP BY symbol', user_id)
    except:
        return apology("Server error")
        
    return render_template("/sell.html", rows=rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
