from app import app, db


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will now be executed within the app context
    app.run(debug=True, port=5000)
