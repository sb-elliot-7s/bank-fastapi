from .interfaces.profile_repository_interface import ProfileRepositoryInterface
from .schemas import User
from bson import ObjectId


class ProfileRepository(ProfileRepositoryInterface):
    def __init__(self, user_collection):
        self._user_collection = user_collection

    async def update_profile(self, user_id: str, updated_data: dict) -> User:
        user = await self._user_collection.find_one_and_update(
            filter={'_id': ObjectId(user_id)},
            update={'$set': updated_data},
            return_document=True
        )
        return user
