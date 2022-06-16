from fastapi import APIRouter, status, Depends, Form, Body
from .constants import email_service_data
from .schemas import CreateUserSchema, Token
from .deps import get_auth_service
from .auth_services import AuthUserService
from .token_service import TokenService
from .push_services import EmailPushService
from permissions import Permission

auth_router = APIRouter(prefix='/auth', tags=['auth'])

response_data = {
    'registration': {
        'status_code': status.HTTP_201_CREATED
    },
    'login_and_confirm_code': {
        'status_code': status.HTTP_200_OK,
        'response_model': Token
    }
}


@auth_router.post('/registration', **response_data.get('registration'))
async def registration(user_data: CreateUserSchema, values=Depends(get_auth_service)):
    return await AuthUserService(**values).registration(user_data=user_data)


@auth_router.post('/login', **response_data.get('login_and_confirm_code'))
async def login(email: str = Form(...), password: str = Form(...), values=Depends(get_auth_service)):
    return await AuthUserService(**values) \
        .login(email=email, password=password, context=EmailPushService(**email_service_data))


@auth_router.post('/confirm', **response_data.get('login_and_confirm_code'))
async def confirm_code(code: str = Body(embed=True), user=Depends(Permission(token_service=TokenService())),
                       values=Depends(get_auth_service)):
    return await AuthUserService(**values).verify_code(code=code, user=user)
