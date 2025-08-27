from fastapi import Request

def extract_user_from_jwt(request: Request) -> str:
    user_login = request.headers.get("x-user-login", "")
    if user_login and user_login.strip():
        return user_login.strip()
    return "anonymous"

async def get_current_user(request: Request) -> str:
    return extract_user_from_jwt(request)
