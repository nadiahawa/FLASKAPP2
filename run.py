from app import app
from app.models import db, Animal
from app.models import db, User
from app.models import db, Post

@app.shell_context_processor
def shell_context():
    return{'db': db, 'Animal': Animal, 'User': User, 'Post' : Post}
