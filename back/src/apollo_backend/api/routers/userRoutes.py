from fastapi import APIRouter, Depends

from ...models.dto.userDTO import UserOutDTO
from ...api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "success": True,
        "status_code": 200,
        "message": "Fetched user",
        "data": UserOutDTO.model_validate(user),
    }
