from passlib.context import CryptContext
from fastapi.concurrency import run_in_threadpool

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash(password: str) -> str:
    # bcrypt has a 72-byte limit; truncating safely
    password_bytes = password.encode("utf-8")[:72]

    password_truncated = password_bytes.decode("utf-8", errors="ignore")

    # Offload the heavy hashing to a threadpool
    return await run_in_threadpool(password_context.hash, password_truncated)

async def verify(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    
    # Offload the heavy verification to a threadpool
    return await run_in_threadpool(password_context.verify, plain_password, hashed_password)
