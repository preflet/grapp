---
title: Grapp
---
## **Grapp**

**Grapp** is a modern day dynamic visualization tool made with **Plotly.js, Dash, Fastapi** and **Redis**. Currently it supports MongoDB and MySQL database.

## Features of Grapp

*  Can connect to a data source (Database, file path, FTP)
*  Run async multiple db queries (MongoDB, MySql) to fetch dataset
*  Preprocess data layer with general modules
*  Create graph objects (dash)
*  Add a cache layer (redis, in-memory)
*  Create a rawdata API
*  Create a dash app route with iframe support

Complete workflow of grapp is using meta.json .It is the entry point of Grapp app where it expects user to add hardcoded details of the application. The below attached meta_json_schema describes the structure of meta.json.

```json
meta_json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "host": {"type": "string"},
        "port": {"type": "number"},
        "graphs": {
            "type": "array",
            "properties": {
                "name": {"type": "string"},
                "route": {"type": "string"},
                "db": {"type": "object",
                       "properties": {
                           "type": {"type": "string"},
                           "credentials": {"type": "object"}
                       },
                       "required": ["type", "credentials"]
                       },
                "queries": {
                    "type": "array",
                    "properties": {
                        "table": {"type": "string"},
                        "type": {"type": "string"},
                        "input": {"type": "string"},
                    },
                }
            },
            "required": ["name", "route", "db"]
        },
    },
    "required": ["name", "graphs"]
}
```

### Properties and their use in meta.json

* name - Name of the application
* host - Host address
* port - Port number
* graphs - Array of objects containing meta info about the graphs

  * name - Title of the graph webpage also summarizes the graphs purpose
  * route - Route of the graph webpage
  * db - Database object which gives credentials of the database

    1. type - Tells about the type of database (mysql , mongo or file based)
    2. credentials - Object having fields for logging into the database.
  * queries - Array of database queries that will be executed to fetch data for plotting graphs.