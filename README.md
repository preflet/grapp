# Grapp

A dynamic visualization tool with Plotly.js, Dash, Fastapi and Redis. Currently it supports MongoDB and MySQL database.

## Features

- [x] Connect to a data source (Database, file path, FTP)
- [x] Run async multiple db queries (MongoDB, MySql)
- [ ] Preprocess data layer with general modules
- [x] Create graph objects (dash)
- [x] Add a cache layer (redis, in-memory)
- [ ] Create raw data API
- [ ] Create a dash app route with iframe support
- [x] Standlone deployment

## Create Standalone

- Windows

Run the command in `Command Prompt` and set environment variables.

```bash
pyinstaller test-grapp.py ^
    --name ENA ^
    --add-data ".env;." ^ # if needed and doesn't contain sensitive uri
    --add-data "assets/*;assets" ^
    --add-data "static/*;static" ^
    --add-data "test-meta.json;." ^
    --windowed ^
    --hidden-import uvicorn ^
    --hidden-import uvicorn.logging ^
    --hidden-import uvicorn.loops ^
    --hidden-import uvicorn.loops.auto ^
    --hidden-import uvicorn.protocols ^
    --hidden-import uvicorn.protocols.http ^
    --hidden-import uvicorn.protocols.http.auto ^
    --hidden-import uvicorn.protocols.websockets ^
    --hidden-import uvicorn.protocols.websockets.auto ^
    --hidden-import uvicorn.lifespan ^
    --hidden-import uvicorn.lifespan.on ^
    --hidden-import tornado ^
    --target-architecture x86_64 ^
    --onefile ^
    --icon "assets/favicon.ico"
```

- Linux

Run the command in `Command Prompt` and set environment variables.

```bash
pyinstaller test-grapp.py \
    --name ENA \
    --add-data ".env;." \ # if needed and doesn't contain sensitive uri
    --add-data "assets/*;assets" \
    --add-data "static/*;static" \
    --add-data "test-meta.json;." \
    --windowed \
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
    --target-architecture x86_64 \
    --onefile \
    --icon "assets/favicon.ico"
```
