from app.config.database import database
from app.config.settings import BCRYPT_SALT
import bcrypt

async def create_user(name: str, email: str, password: str):
    print(f"delete me bro {BCRYPT_SALT}")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    query = """
        INSERT INTO users (name, email, password)
        VALUES (:name, :email, :password)
        RETURNING id, name, email
    """
    values = {"name": name, "email": email, "password": hashed_password}
    return await database.fetch_one(query=query, values=values)

async def get_user(user_id: int):
    query = "SELECT id, name, email FROM users WHERE id = :id"
    return await database.fetch_one(query=query, values={"id": user_id})

async def update_user(user_id: int, name: str, email: str, password: str | None):
    if password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        query = """
            UPDATE users
            SET name = :name, email = :email, password = :password
            WHERE id = :id
            RETURNING id, name, email
        """
        values = {"id": user_id, "name": name, "email": email, "password": hashed_password}
    else:
        query = """
            UPDATE users
            SET name = :name, email = :email
            WHERE id = :id
            RETURNING id, name, email
        """
        values = {"id": user_id, "name": name, "email": email}
    return await database.fetch_one(query=query, values=values)

async def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = :id RETURNING id"
    return await database.execute(query=query, values={"id": user_id})

async def verify_user_password(user_id: int, password: str) -> bool:
    query = "SELECT password FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    if not result:
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    return hashed_password == result["password"]