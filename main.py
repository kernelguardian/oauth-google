from fastapi import FastAPI
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config

from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
import os
from dotenv import load_dotenv

load_dotenv()
SESSION_KEY = os.environ.get("SESSION_KEY")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
}
starlette_config = Config(environ=config_data)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_KEY)

oauth = OAuth(config=starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.route("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        print(error)
        return HTMLResponse(f"<h1>{error.error}</h1>")
    print(token)
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
        print(user)
    return RedirectResponse(url="/success")


@app.route("/success")
async def success(request: Request):
    # if request.session["user"]:
    #     print("session", request.session["user"])
    return HTMLResponse("<h1>Login successful</h1>")
