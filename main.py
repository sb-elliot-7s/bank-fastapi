from fastapi import FastAPI

from auth.auth_controllers import user_routers
from transactions.controllers import finance_router
from account.controllers import account_routers
from auth.profile_controllers import profile_router
from fastapi.responses import ORJSONResponse

app = FastAPI(title='bank', default_response_class=ORJSONResponse)

app.include_router(user_routers)
app.include_router(finance_router)
app.include_router(account_routers)
app.include_router(profile_router)
