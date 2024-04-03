class Config:
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/authors_api"

    JWT_SECRET_KEY = "authors"