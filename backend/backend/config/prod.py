import os
from .base import *

DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,.onrender.com').split(',')

# HTTPS / SSL Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Proxy headers for Render/Load Balancers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- CORS & CSRF TRUSTED ORIGINS CONFIG ---
CORS_ALLOW_ALL_ORIGINS = False

cors_env = os.getenv('CORS_ALLOWED_ORIGINS', '')
if cors_env:
    CORS_ALLOWED_ORIGINS = [url.strip() for url in cors_env.split(',') if url.strip()]
    CSRF_TRUSTED_ORIGINS = [url.strip() for url in cors_env.split(',') if url.strip()]
else:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True