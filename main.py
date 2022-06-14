from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.auth_controllers import auth_router
from transactions.controllers import finance_router
from account.controllers import account_router
from auth.profile_controllers import profile_router

from currency_service.controllers import currency_router

from fastapi.responses import ORJSONResponse

app = FastAPI(title='bank', default_response_class=ORJSONResponse)

app.include_router(auth_router)
app.include_router(finance_router)
app.include_router(account_router)
app.include_router(profile_router)
app.include_router(currency_router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
