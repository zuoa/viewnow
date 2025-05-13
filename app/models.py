import datetime
import secrets
import string
from peewee import (
    Model, SqliteDatabase, CharField, TextField, 
    DateTimeField
)
import config

# Connect to SQLite database
db = SqliteDatabase(config.DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class HtmlSnippet(BaseModel):
    """Model for storing HTML snippets"""
    id = CharField(primary_key=True, max_length=10)
    html_content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    @staticmethod
    def generate_short_id(length=8):
        """Generate a short, unique ID"""
        # Use a mix of lowercase letters and numbers for readability
        alphabet = string.ascii_lowercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @classmethod
    def create_snippet(cls, html_content):
        """Create a new HTML snippet"""
        # Generate a unique short ID
        while True:
            short_id = cls.generate_short_id()
            # Check if this ID already exists
            if not cls.select().where(cls.id == short_id).exists():
                break
                
        return cls.create(
            id=short_id,
            html_content=html_content
        )
    
    @classmethod
    def get_by_id_str(cls, id_str):
        """Get snippet by string ID"""
        try:
            return cls.get(cls.id == id_str)
        except cls.DoesNotExist:
            return None

def create_tables():
    """Create database tables if they don't exist"""
    with db:
        db.create_tables([HtmlSnippet])
