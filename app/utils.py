from bcrypt import hashpw, gensalt


def hash_password(password: str):
  """Hash a password
  """
  if not password:
    raise ValueError("A password must be provided")
  encoded = password.encode('utf-8')
  hashed_password = hashpw(encoded, gensalt(12))
  return hashed_password.decode('utf-8')