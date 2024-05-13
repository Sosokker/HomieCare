"""
This file is used to store the configuration of the project.

Attributes:
    DB_HOST: The host of the MySQL database
    DB_USER: The username of the MySQL database
    DB_PASSWD: The password of the MySQL database
    DB_NAME: The name of the MySQL database
    MINIO_ENDPOINT: The endpoint of the MinIO storage
    MINIO_ACCESS_KEY: The access key of the MinIO storage
    MINIO_SECRET_KEY: The secret key of the MinIO storage
    VIDEO_BUCKET: The bucket name for storing video files
"""

from decouple import config


DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASSWD = config('DB_PASSWD')
DB_NAME = config('DB_NAME')
MINIO_ENDPOINT = config('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY')
VIDEO_BUCKET = config('VIDEO_BUCKET')
CONFIG_FILE = config('CONFIG_FILE')
YOLO_WEIGHT_FILE = config('YOLO_WEIGHT_FILE')
SPPE_WEIGHT_FILE = config('SPPE_WEIGHT_FILE')
TSSTG_WEIGHT_FILE = config('TSSTG_WEIGHT_FILE')
LINE_NOTIFY_TOKEN = config('LINE_NOTIFY_TOKEN')
WEATHER_API_KEY = config('WEATHER_API_KEY')
LAT = config('LAT')
LON = config('LON')