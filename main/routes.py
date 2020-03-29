from flask import render_template, request, Blueprint
from ..models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # define a URL parameter with request
    # label of 'page', default value of 1
    # must be int
    # it can then be called like
    # .../?page=[int]
    page = request.args.get('page', 1, type=int)
    # paginate method allows to specify items per page
    # PROTIP - to get a list of all attributes of an entity
    # use the method dir()
    # i.e. dir(posts)
    # Get all posts in descending date order, 
    # and define pagination settings
    posts = Post.query.order_by(Post.date_posted.desc()) \
                .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')