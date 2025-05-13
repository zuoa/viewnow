import datetime
from flask import request, g
from app import create_app
from app.models import db, create_tables

app = create_app()

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

@app.before_request
def before_request():
    g.now = datetime.datetime.now()

@app.teardown_request
def teardown_request(exception):
    if not db.is_closed():
        db.close()

@app.cli.command("init-db")
def init_db():
    """Initialize the database tables"""
    create_tables()
    print("Database tables created successfully!")

if __name__ == "__main__":
    # Create tables if they don't exist
    create_tables()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=7080)
