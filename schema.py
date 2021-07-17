schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "host": {"type": "string"},
        "port": {"type": "number"},
        "filters": {
            "type": "array",
            "properties": {
                "filter_type": {"type": "string"}, #supports DatePickerRange, DatePickerSingle
                "options": {"type": "object"}, # dynamic options set, in case of datetime it allows - https://dash.plotly.com/dash-core-components/datepickersingle
                "query": {"type": "string"}, # for datetime, use "{start}" and "{end}"
                "size": {"type": "number"}, # columns flexbox
            }
        },
        "graphs": {
            "type": "array",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "route": {"type": "string"},
                "colors": {"type": "array"},
                "db": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "credentials": {"type": "object"}
                    },
                    "required": ["type", "credentials"]
                },
                "queries": {
                    "type": "array",
                    "properties": {
                        "input": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "source": {"type": "string"},
                                "type": {"type": "string"}, # accepts - raw, aggregate
                            },
                            "required": ["type", "value"]
                        }, 
                        "output": {
                            "type": "object",
                            "properties": {
                                "info": {"type": "string"},
                                "title": {"type": "string"},
                                "type": {"type": "string"}, # accepts: indicator, piechart, map-scatter-plot, donut, 
                                "x_axis_label": {"type": "string"},
                                "y_axis_label": {"type": "string"},
                                "values": {"type": "string"},
                                "labels": {"type": "string"},
                                "color": {"type": "string"},
                            },
                            "required": ["type"]
                        },
                        "colors": {"type": "array"},
                        "size": {"type": "integer"}
                    },
                }
            },
            "required": ["name", "route", "db"]
        },
    },
    "required": ["name", "graphs"]
}