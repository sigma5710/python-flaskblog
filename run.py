from . import create_app

# run the create_app function defined in init
# which returns an app
app = create_app()
# old way of running in debug mode
# NOTE that when using the environment
# variables you will need to set them up
# every time you run the terminal
if(__name__ == '__main__'):
    app.run(debug=True)