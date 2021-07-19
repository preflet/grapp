export GRAPP_META_FILE="test-meta.json"
export GRAPP_PY_FILE="test-grapp.py" 
export GRAPP_PORT=8000
export APP_NAME="ENA"

pyinstaller ${GRAPP_PY_FILE} \
    --name ${APP_NAME} \
    --add-data "assets/*:assets" \
    --add-data "static/*:static" \
    --add-data "${GRAPP_META_FILE}:." \
    --hidden-import uvicorn \
    --hidden-import uvicorn.logging \
    --hidden-import uvicorn.loops \
    --hidden-import uvicorn.loops.auto \
    --hidden-import uvicorn.protocols \
    --hidden-import uvicorn.protocols.http \
    --hidden-import uvicorn.protocols.http.auto \
    --hidden-import uvicorn.protocols.websockets \
    --hidden-import uvicorn.protocols.websockets.auto \
    --hidden-import uvicorn.lifespan \
    --hidden-import uvicorn.lifespan.on \
    --hidden-import tornado \
    --onefile \
    --clean \
    --icon "assets/favicon.ico"