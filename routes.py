from all_routes.manager_routes import *
from all_routes.user_routes import *



@app.route("/" , methods =["GET"])
def HomePage():
    return render_template("unauthorized_user.html" )

@app.errorhandler(404)
def handle_404(e):
    return render_template("404.html")