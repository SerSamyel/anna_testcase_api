
class Config:
    SECRET_KEY = '5626973cbe3e4f8ba6593e4ba6124dd6'
    CSRF_ENABLED = True
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/taskmaker'

