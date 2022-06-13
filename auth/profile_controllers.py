from fastapi import APIRouter, status, Depends
from .schemas import UpdateProfileSchema, User
from permissions import Permission
from .token_service import TokenService
from .profile_service import ProfileService
from .profile_repository import ProfileRepository
from .deps import get_user_collection

profile_router = APIRouter(prefix='/profile', tags=['profile'])


@profile_router.patch('/', status_code=status.HTTP_200_OK, response_model=User, response_model_by_alias=False)
async def update_profile(profile_data: UpdateProfileSchema,
                         user_collection=Depends(get_user_collection),
                         user=Depends(Permission(token_service=TokenService()))):
    return await ProfileService(repository=ProfileRepository(user_collection=user_collection)) \
        .update_profile(updated_data=profile_data, user_id=user.id)
