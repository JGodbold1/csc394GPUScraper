from website import create_app

# creates the main app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# david was here