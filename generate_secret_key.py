import os


secret_key = os.urandom(32).hex()
print(f"SECRET_KEY = '{secret_key}'")