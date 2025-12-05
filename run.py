"""Application entry point"""
from app import create_app, db

# Create app instance
app = create_app()

# CLI command to initialize database
@app.cli.command()
def init_db():
    """Create database tables"""
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    app.run(debug=True)
