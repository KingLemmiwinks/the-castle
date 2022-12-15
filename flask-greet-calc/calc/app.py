# Put your app in here.
from flask import Flask, request
from operations import add, sub, mult, div

app = Flask(__name__)

@app.route('/add')
def add_operation():
    """Add a and b"""

    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    result = add(a,b)
    return str(result)

@app.route('/sub')
def subtract_operation():
    """Subtract a and b"""

    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    result = sub(a, b)
    return str(result)

@app.route('/mult')
def mult_operation():
    """Multiply a and b"""

    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    result = mult(a, b)
    return str(result)

@app.route('/div')
def div_operation():
    """Divide a and b"""

    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    result = div(a, b)
    return str(result)

operators = {
    "add": add,
    "sub": sub,
    "mult": mult,
    "div": div
}

@app.route("/math/<operation>")
def do_math(operation):
    """Use operations on a and b"""

    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    result = operators[operation](a, b)
    return str(result)
