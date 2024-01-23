from astro import app, admin, db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin.create_admin_user()
    app.run(host='0.0.0.0', port=5001)
