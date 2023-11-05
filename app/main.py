from fastapi import FastAPI
from app.routes import product, cart, founder, testimony, user, auth
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=database.engine)

origins = [
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(product.router)
app.include_router(cart.router)
app.include_router(founder.router)
app.include_router(testimony.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get('/')
def root():
    return {"message": "Welcome to Northstar backend"}
