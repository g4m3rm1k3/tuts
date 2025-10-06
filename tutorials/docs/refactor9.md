Let's keep the momentum going. We'll now move the rest of the authentication-related endpoints into our new `auth.py` router, completing the separation of our authentication logic.

---

### Stage 3.3: Completing the Authentication Router

We're going to take all the remaining endpoints from `mastercam_main.py` that deal with user accounts—setting up passwords, checking passwords, validating tokens, and password resets—and move them into `auth.py`.

#### The "Why"

This step completes the creation of our self-contained **authentication module**. By grouping all these related functions, our `auth.py` file becomes the single source of truth for how users interact with the authentication system at the API level. This organization is clean, intuitive, and makes the system much easier to manage.

#### Your Action Item

Replace the entire contents of your `backend/app/api/routers/auth.py` file with the following code. This includes the `/login` route we already created, plus all the other refactored authentication routes.

Notice how each function now declares `auth_service: UserAuth = Depends(get_user_auth)` in its signature to get access to the authentication logic.

```python
from fastapi import APIRouter, Depends, HTTPException, Response, status, Form
from app.core.security import UserAuth, ADMIN_USERS
from app.api.dependencies import get_user_auth, get_current_user
from app.models import schemas

router = APIRouter(
  prefix="/auth",
  tags=["Authentication"],
)

@router.post("/login")
async def login(
  response: Response,
  username: str = Form(...),
  password: str = Form(...),
  auth_service: UserAuth = Depends(get_user_auth)
):
  """Handles user login and sets a secure, httpOnly cookie for authentication."""
  if not auth_service.verify_user(username, password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
    )

  access_token = auth_service.create_access_token(username)

  response.set_cookie(
    key="auth_token",
    value=access_token,
    httponly=True,
    secure=False, # Set to True in production with HTTPS
    samesite="lax",
    max_age=28800 # 8 hours
  )

  return {
    "status": "success",
    "username": username,
    "is_admin": username in ADMIN_USERS
  }

@router.post("/setup_password")
async def setup_password(
  username: str = Form(...),
  password: str = Form(...),
  auth_service: UserAuth = Depends(get_user_auth)
):
  """Allows a new user to set their initial password."""
  # In a real app, you might add more validation here, e.g., using a one-time setup token.
  if auth_service.create_user_password(username, password):
    token = auth_service.create_access_token(username)
    # Note: We are returning the token directly here. The login endpoint is preferred
    # as it sets a secure cookie. This endpoint is for initial setup.
    return {"status": "success", "access_token": token, "token_type": "bearer"}
  else:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Failed to create password for user."
    )

@router.post("/check_password")
async def check_password(
  username: str = Form(...),
  auth_service: UserAuth = Depends(get_user_auth)
):
  """Checks if a password has been set for a given username."""
  users = auth_service._load_users() # Accessing a "private" method is okay here as it's part of the same logical domain.
  return {"has_password": username in users}


@router.post("/validate")
async def validate_token(current_user: dict = Depends(get_current_user)):
  """Validates a token. The dependency 'get_current_user' does all the work."""
  # If get_current_user succeeds, the token is valid. It will raise an exception if not.
  return {"valid": True, "user": current_user}

@router.post("/request_reset")
async def request_password_reset(
  username: str = Form(...),
  auth_service: UserAuth = Depends(get_user_auth)
):
  """Generates a password reset token for a user."""
  try:
    reset_token = auth_service.reset_password_request(username)
    # In a real application, you would email this token to the user.
    # For this app, we return it directly for the user to copy/paste.
    return {"status": "success", "reset_token": reset_token}
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/reset_password")
async def reset_password(
  username: str = Form(...),
  reset_token: str = Form(...),
  new_password: str = Form(...),
  auth_service: UserAuth = Depends(get_user_auth)
):
  """Resets a user's password using a valid reset token."""
  success = auth_service.reset_password(username, reset_token, new_password)
  if success:
    return {"status": "success", "message": "Password has been reset successfully."}
  else:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid or expired reset token."
    )
```

---

Fantastic\! We have now fully migrated all authentication endpoints. Our `auth.py` file is a complete, self-contained module for user management, and our `mastercam_main.py` is another big step closer to being empty.

Let me know when you're ready to create our next, and largest, router: the one for file management.
