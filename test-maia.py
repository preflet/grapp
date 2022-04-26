from grapp import Grapp

grapp = Grapp(meta_path="test-maia.json")
grapp.start()


# generate code

# pyinstaller test-maia.py \
#     --name MAIA \
#     --add-data ".env;." \ 
#     --add-data "assets/*;assets" \
#     --add-data "static/*;static" \
#     --add-data "test-maia.json;." \
#     --windowed \
#     --hidden-import uvicorn \
#     --hidden-import uvicorn.logging \
#     --hidden-import uvicorn.loops \
#     --hidden-import uvicorn.loops.auto \
#     --hidden-import uvicorn.protocols \
#     --hidden-import uvicorn.protocols.http \
#     --hidden-import uvicorn.protocols.http.auto \
#     --hidden-import uvicorn.protocols.websockets \
#     --hidden-import uvicorn.protocols.websockets.auto \
#     --hidden-import uvicorn.lifespan \
#     --hidden-import uvicorn.lifespan.on \
#     --hidden-import tornado \
#     --target-architecture x86_64 \
#     --onefile \
#     --icon "assets/favicon.ico"