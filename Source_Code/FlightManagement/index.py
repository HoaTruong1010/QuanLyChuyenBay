from flask import  render_template
from FlightManagement import app
from FlightManagement.models import *

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)