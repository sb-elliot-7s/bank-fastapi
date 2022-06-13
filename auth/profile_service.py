from .interfaces.profile_repository_interface import ProfileRepositoryInterface
from .schemas import UpdateProfileSchema


class ProfileService:
    def __init__(self, repository: ProfileRepositoryInterface):
        self._repository = repository

    async def update_profile(self, updated_data: UpdateProfileSchema, user_id: str):
        return await self._repository.update_profile(user_id=user_id,
                                                     updated_data=updated_data.dict(exclude_none=True))
