from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)

# 'app_errorhandler' decorator applies to the entire application
# instead of just working on this blueprint
@errors.app_errorhandler(404)
def error_404(error):
    # return 2 values
    # 2nd value is code returned by page
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500