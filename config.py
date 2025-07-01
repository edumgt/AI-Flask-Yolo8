import os

class Config:
    """Flask 앱 설정"""

    SECRET_KEY = 'asdf-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    JWT_SECRET_KEY = '938a3jbcx2gwoi2876831dhagb'
    SESSION_TYPE = 'filesystem'

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-2')
    S3_BUCKET = os.getenv('S3_BUCKET', 'my-bucket')

    UPLOAD_FOLDER = 'uploads'
    RESULT_FOLDER = 'results'
    SAMPLE_FOLDER = 'samples'
