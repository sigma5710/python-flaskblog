from . import create_app

# run the create_app function defined in init
# which returns an app
app = create_app()

if(__name__ == '__main__'):
    app.run(debug=True)