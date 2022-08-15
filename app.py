from website import create_app

if __name__ == "__main__":
    # Create an app
    app = create_app()

    # Run the app
    app.run(debug=True)
