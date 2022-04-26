import pymongo
import json
import plotly.graph_objs as go
import plotly.express as px
import dash_core_components as dcc
from dash_leaflet import Map, TileLayer, GeoJSON ,WMSTileLayer
from datetime import datetime
from dash_leaflet.express import dicts_to_geojson
from dash_extensions.javascript import assign
from os import getenv

myclient = pymongo.MongoClient(getenv('uri_name'))
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[getenv('db_name')]

data = mydb["DATA"]
from dateutil import parser

from millify import millify

plot_colors = {
    'background-color': 'rgb(244, 244, 244)'
} 

def create_filter(start_date=None,end_date=None,tepo=[]):
    match = {"$match":{}}
    print("--------")
    print(start_date)
    print(end_date)
    print("--------")
    if start_date and end_date:
        match = {"$match":{"DATETIME":{}}}
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)
        match['$match']['DATETIME']["$gte"] =  start_date
        match['$match']['DATETIME']["$lte"] =  end_date
    elif end_date:
        match = {"$match":{"DATETIME":{}}}
        end_date = parser.parse(end_date)
        match['$match']['DATETIME']["$lte"] =  end_date
    elif start_date:
        match = {"$match":{"DATETIME":{}}}
        start_date = parser.parse(start_date)
        match['$match']['DATETIME']["$gte"] =  start_date

    # if len(muni):
    #     match['$match'].update({"MUNICÍPIO":{ "$in":muni}})
    #     match['$match']['MUNICÍPIO']['$in'].append("$MUNICÍPIO") 

    if len(tepo):
        match['$match'].update({"TIPO_DE_EDIFICIO":{ "$in":tepo}})
        match['$match']['TIPO_DE_EDIFICIO']['$in'].append("$TIPO_DE_EDIFICIO") 

    if len(match['$match']):
        return match

    return ""

def indicator_total(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id': 'null', 'count': {'$sum': {'$toDouble': '$Consumo' }}}}]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(1,filter)
    print("PIPELINE"+str(pipeline))
    data = list(mydb.MAIA.aggregate(pipeline))
    print(data)
    c = 0
    if len(data) and 'count' in data[0]:
        c = data[0]['count']
        c = millify(c, precision=2)
        c = c.replace(".",",")

    return c

def indicator_fatura(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id': null, 'count':{'$sum': {'$toDouble': '$Fatura' }}}}]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))
    c = 0
    if len(data) and 'count' in data[0]:
        c = data[0]['count']
        c = millify(c, precision=2)
        c = c.replace(".",",")

    return c

def indicator_numero_de_edificios(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id': null, 'count':{'$addToSet': '$ID'}}}]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))
    c = 0
    if len(data) and 'count' in data[0]:
        c = len(data[0]['count'])
        c = millify(c, precision=2)
        c.replace(".",",")

    return c

def indicator_tipo_de_edifícios(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id': null, 'count':{'$addToSet': '$TIPO_DE_EDIFICIO'}}}]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))
    print(data)
    c = 0
    if len(data) and 'count' in data[0]:
        c = len(data[0]['count'])
        c = millify(c, precision=2)
        c = c.replace(".",",")

    return c



def single_line_chart(filter):
    str_query = "[ { '$group':{ '_id':{ 'month':{ '$toString':{ '$month': '$DATETIME' } }, 'year':{ '$toString':{ '$year': '$DATETIME' } }, 'day':{ '$toString':{ '$dayOfMonth': '$DATETIME' } } }, 'data':{ '$sum':'$CONSUMO' }, 'datetime':{ '$first': '$DATETIME' } } }, { '$project':{ 'Data':{ '$concat':['$_id.day','-','$_id.month','-','$_id.year'] }, 'Consumo': '$data', '_id':0, 'datetime':'$datetime'} }, { '$sort' : { 'datetime' : 1 } } ]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(0,filter)

    data = list(mydb.DATA.aggregate(pipeline))

    Data = [ d['Data'] for d in data ]
    Consumo = [ d['Consumo'] for d in data ]

    figure = px.line({"Data":Data,"Consumo":Consumo }, x="Data", y="Consumo", title="")
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )

    return figure

def donut_chart(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id': '$LOCAL', 'count':{'$sum': 1}}},{'$project':{'Local':'$_id','Contargem':'$count'}}]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))

    labels = [ d['Local'] for d in data ]
    values = [ d['Contargem'] for d in data ]

    color_discrete_map = {
                        "Palmela":"#7AABE5",
                        "Sesimbra": "#D35C59",
                        "Outros": "#FCB454",
                        "Setúbal": "#61DBA7"
                        }
    # figure = px.pie({'value': values,'label':labels}, 
    #     values='value',
    #     names='label',
    #     hole=0.5,
    #     color_discrete_map=color_discrete_map,
    #     color='label',
    # )
    figure = px.bar(  data,
                        x="Local", 
                        y="Contargem",
                        # barmode="group"
                        # color_discrete_map=color_discrete_map
                    )
    # figure.update_traces(
    #     hoverinfo='label+percent',
    #     textinfo='label+percent',
    #     textfont_size=20,
    #     # paper_bgcolor='rgb(244, 244, 244)',
    #     # marker=dict(colors=colors)
    # )
    
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def treechart_tipo_de_edifício(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id':'$TIPO_DE_EDIFICIO','count':{'$sum':1}}}]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)
    
    data = list(mydb.MAIA.aggregate(pipeline))

    labels = [ d['_id'] for d in data ]
    values = [ d['count'] for d in data ]
    parents = ["" for i in values ]

    figure = go.Figure(go.Treemap(
        labels = labels,
        values = values,
        parents = parents,
        root_color="rgb(244, 244, 244)",
        marker=dict(
            colors=['#0066CC', '#D35C59',  '#FCB454', '#61DBA7','#02124F','#CA3A38','#D77C04','#1A764E','#D4EEFF'])
    ))

    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def clustered_bar_chart_fatura(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{ '$group': { '_id': { 'month':'$TIPO_DE_EDIFICIO' , 'year': { '$year': { '$dateFromString': { 'dateString': '$Date' } } } }, 'data': { '$sum': {'$toDouble':'$Fatura'} } } }, { '$project': { '_id':0, 'month':'$_id.month', 'year':{'$toString':'$_id.year'}, 'Fatura':'$data' } } ,{ '$project':{ 'Tipo de edifício': '$month', 'Ano':'$year', 'Fatura':1 }} ]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))
    color_discrete_map = {
                            "Palmela":"#7AABE5",
                            "Sesimbra": "#D35C59",
                            "Outros": "#FCB454",
                            "Setúbal": "#61DBA7"
                        }
    if len(data) == 0:
        data = [{"Tipo de edifício":0,"Ano":0,"Fatura":0}]
    figure = px.bar(    data,
                        x="Tipo de edifício", 
                        y="Fatura",
                        color="Ano",
                        barmode="group"
                        # color_discrete_map=color_discrete_map
                    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def horizontal_barchart_sazonalidade_por_local(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id':{'month':{'$month':{'$dateFromString':{'dateString':'$Date'}}},'muni':'$LOCAL'},'data':{'$sum': {'$toDouble': '$Consumo' }}}},{'$project':{'res':{'$switch':{'branches':[{'case':{'$in':['$_id.month',[12,1,2]]},'then':'Winter'},{'case':{'$in':['$_id.month',[3,4,5]]},'then':'Spring'},{'case':{'$in':['$_id.month',[6,7,8]]},'then':'Summer'},{'case':{'$in':['$_id.month',[9,10,11]]},'then':'Antumn'}]}},'data':1}},{'$group':{'_id':{'local':'$_id.muni','season':'$res'},'count':{'$sum':'$data'}}},{'$project':{'Local':'$_id.local','Sazonalidade':'$_id.season','Soma':'$count','_id':0}}]"
    pipeline = json.loads(str_query.replace("'",'"'))
    
    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))

    Contar = [ d['Soma'] for d in data ]
    Temporadas = [ d['Sazonalidade'] for d in data ]
    local = [d['Local'] for d in data]
    color_discrete_map = {
                            "Palmela":"#7AABE5",
                            "Sesimbra": "#D35C59",
                            "Outros": "#FCB454",
                            "Setúbal": "#61DBA7"
                        }

    figure = px.bar(  { "Soma": Contar,
                        "Sazonalidade": Temporadas,
                        "Local": local }, 
                        x="Soma", 
                        y="Sazonalidade",
                        color="Local",
                        barmode="stack",
                        color_discrete_map=color_discrete_map
                    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def scatterchart_sazonalidade_por_pavilhão(filter):
    str_query = "[ { '$match':{ 'TIPO_DE_EDIFÍCIO':'Pavilhão' } }, { '$group':{ '_id':{ 'month':{ '$month': '$DATETIME'} }, 'data':{ '$sum':'$CONSUMO' } } }, { '$project': { 'res': { '$switch': { 'branches': [ { 'case':{ '$in': [ '$_id.month',[12,1,2] ] }, 'then': 'Inverno' }, { 'case': { '$in': [ '$_id.month', [3,4,5] ] }, 'then': 'Primavera' }, { 'case': { '$in': [ '$_id.month',[6,7,8,9] ] }, 'then': 'Verão' }, { 'case': { '$in': [ '$_id.month',[10,11] ] }, 'then': 'Outono' } ] } }, 'data': 1 } }, { '$group':{ '_id': { 'season': '$res' }, 'count':{ '$sum':'$data' } } }, { '$project':{ 'Temporadas':'$_id.season', 'Contagem':'$count', '_id':0 } } ]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(0,filter)

    data = list(mydb.DATA.aggregate(pipeline))

    Contar = [ d['Contagem'] for d in data ]
    Temporadas = [ d['Temporadas'] for d in data ]

    figure = go.Figure((go.Scatter(
            x=Temporadas, 
            y=Contar,
            fill="tonexty", 
            fillcolor="#7AABE5",
            line_color= "#0066CC"
        )))
    

    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def bubblechart_sazonalidade_por_edificio(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{ '$group':{ '_id':{ 'month':{ '$month': {'$dateFromString':{'dateString':'$Date'}} }, 'tepo_de_edificio': '$TIPO_DE_EDIFICIO' }, 'data':{'$sum': {'$toDouble': '$Consumo' }} } }, { '$project':{ 'res':{ '$switch': { 'branches': [ { 'case': { '$in': [ '$_id.month',[12,1,2] ] }, 'then': 'Winter' }, { 'case': { '$in': [ '$_id.month', [3,4,5] ] }, 'then': 'Spring' }, { 'case': { '$in': [ '$_id.month',[6,7,8] ] }, 'then': 'Summer' }, { 'case': { '$in': [ '$_id.month',[9,10,11] ] }, 'then': 'Antumn' } ] } }, 'data': 1 } }, { '$group':{ '_id': { 'tepo_de_edificio':'$_id.tepo_de_edificio', 'season': '$res' }, 'count':{ '$sum':'$data' } } }, { '$project': { 'TEPO DE EDIFICIO': '$_id.tepo_de_edificio', 'Sazonalidade':'$_id.season', 'Soma':'$count', '_id':0 } } ]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(1,filter)
    data = list(mydb.MAIA.aggregate(pipeline))

    Contar = [ d['Soma'] for d in data ]
    Temporadas = [ d['Sazonalidade'] for d in data ]
    tepo_de_edificio = [ d['TEPO DE EDIFICIO'] for d in data ]

    # print("tepo_de_edificio-----"+str(tepo_de_edificio))
    color_discrete_map ={   "Escola Básica":"#0066CC",
                            "Edifícios": "#D35C59",
                            "Biblioteca": "#FCB454",
                            "Centro Cultural": "#61DBA7",
                            "Pavilhão":"#02124F",
                            "Mercado":"#CA3A38",
                            "Centro":"#D77C04",
                            "Paços do Concelho":"#1A764E",
                            "Outros":"#585C61"
                        }
    # print("DATA"+str(data))
    figure = px.scatter( {"Sazonalidade": Temporadas,
                        "Soma": Contar,
                        "TEPO DE EDIFICIO": tepo_de_edificio}, 
                        x="Soma", 
                        y="Sazonalidade",
                        size="Soma",
                        color="TEPO DE EDIFICIO",
                        hover_name="TEPO DE EDIFICIO",
                        log_x=True,
                        size_max=60,
                        color_discrete_map=color_discrete_map
                    )
    

    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def linechart_padrão_por_hora_por_tipo_de_edifício(filter):
    str_query = "[ { '$group':{ '_id':{ 'hour':{ '$hour': '$DATETIME' }, 'TIPO_DE_EDIFÍCIO': '$TIPO_DE_EDIFÍCIO' }, 'count':{ '$sum': '$CONSUMO' } } },{ '$project': { 'Hora': '$_id.hour', 'TIPO_DE_EDIFÍCIO':'$_id.TIPO_DE_EDIFÍCIO', 'Contagem': '$count', '_id':0 } }, { '$sort' : { 'Hora' : 1 } } ]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(0,filter)

    data = list(mydb.DATA.aggregate(pipeline))

    Hora = [ d['Hora'] for d in data ]
    Contar = [ d['Contagem'] for d in data ]
    TIPO_DE_EDIFÍCIO = [ d['TIPO_DE_EDIFÍCIO'] for d in data ]

    color_discrete_map ={   "Escola Básica":"#0066CC",
                            "Edifícios": "#D35C59",
                            "Biblioteca": "#FCB454",
                            "Centro Cultural": "#61DBA7",
                            "Pavilhão":"#02124F",
                            "Mercado":"#CA3A38",
                            "Centro":"#D77C04",
                            "Paços do Concelho":"#1A764E",
                            "Outros":"#585C61"
                        }
    # print("DATA"+str(data))
    figure = px.line(  { "Contagem": Contar,
                        "Hora": Hora,
                        "Tipo de edifício": TIPO_DE_EDIFÍCIO }, 
                        x="Hora", 
                        y="Contagem",
                        color="Tipo de edifício",
                        color_discrete_map=color_discrete_map
                    )
    

    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def areachart_comparação_semanal(filter):
    # str_query = "[ { '$group':{ '_id':{ 'dayOfWeek': { '$dayOfWeek': '$DATETIME' }, 'MUNICÍPIO':'$MUNICÍPIO' }, 'count':{ '$sum': '$CONSUMO' } } }, { '$project': { 'Dia': '$_id.dayOfWeek', 'MUNICIPIO':'$_id.MUNICÍPIO', 'Contar': '$count', '_id':0 } }, { '$project':{ 'Dias da semana':{ '$switch': { 'branches': [ { 'case': { '$eq': [ '$Dia', 1 ] }, 'then': 'Domingo' }, { 'case': { '$eq': [ '$Dia', 2 ] }, 'then': 'Segunda' }, { 'case': { '$eq': [ '$Dia', 3 ] }, 'then': 'Terça' }, { 'case': { '$eq': [ '$Dia', 4 ] }, 'then': 'Quarta' }, { 'case': { '$eq': [ '$Dia', 5 ] }, 'then': 'Quinta' }, { 'case': { '$eq': [ '$Dia', 6 ] }, 'then': 'Sexta' }, { 'case': { '$eq': [ '$Dia', 7 ] }, 'then': 'Sábado' } ] } }, 'Dia':'$Dia', 'MUNICIPIO':'$MUNICIPIO', 'Contar': '$Contar' } }, { '$sort' : { 'Dia' : 1 } } ]"
    str_query = "[{ '$group':{ '_id':{ 'dayOfWeek': { '$dayOfWeek': '$DATETIME' }, 'MUNICÍPIO':'$MUNICÍPIO' }, 'count':{ '$sum': '$CONSUMO' } } }, { '$project': { 'Dia': '$_id.dayOfWeek', 'MUNICIPIO':'$_id.MUNICÍPIO', 'Contar': '$count', '_id':0 } }, { '$project':{ 'dias da semana':{ '$switch': { 'branches': [ { 'case': { '$eq': [ '$Dia', 1 ] }, 'then': 'Domingo' }, { 'case': { '$eq': [ '$Dia', 2 ] }, 'then': 'Segunda' }, { 'case': { '$eq': [ '$Dia', 3 ] }, 'then': 'Terça' }, { 'case': { '$eq': [ '$Dia', 4 ] }, 'then': 'Quarta' }, { 'case': { '$eq': [ '$Dia', 5 ] }, 'then': 'Quinta' }, { 'case': { '$eq': [ '$Dia', 6 ] }, 'then': 'Sexta' }, { 'case': { '$eq': [ '$Dia', 7 ] }, 'then': 'Sábado' } ] } }, 'Dia':'$Dia', 'MUNICIPIO':'$MUNICIPIO', 'Contar': '$Contar' } }, { '$project':{ 'week_order':{ '$switch': { 'branches': [ { 'case': { '$eq': [ '$dias da semana', 'Domingo' ] }, 'then': 7 }, { 'case': { '$eq': [ '$dias da semana', 'Segunda' ] }, 'then': 1 }, { 'case': { '$eq': [ '$dias da semana', 'Terça' ] }, 'then': 2 }, { 'case': { '$eq': [ '$dias da semana', 'Quarta' ] }, 'then': 3 }, { 'case': { '$eq': [ '$dias da semana', 'Quinta' ] }, 'then': 4 }, { 'case': { '$eq': [ '$dias da semana', 'Sexta' ] }, 'then': 5 }, { 'case': { '$eq': [ '$dias da semana', 'Sábado' ] }, 'then': 6 } ] } }, 'Dia':'$Dia', 'MUNICIPIO':'$MUNICIPIO', 'Contagem': '$Contar', 'Dias da semana':'$dias da semana' } }, { '$sort' : { 'week_order' : 1 } }]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(0,filter)

    data = list(mydb.DATA.aggregate(pipeline))

    Dias_da_semana = [ d['Dias da semana'] for d in data ]
    Contar = [ d['Contagem'] for d in data ]
    MUNICIPIO = [ d['MUNICIPIO'] for d in data ]

    # if len(Dias_da_semana):   
    #     dom_dia = Dias_da_semana[0]
    #     Dias_da_semana.pop(0)
    #     Dias_da_semana.append(dom_dia)
    # if len(Contar):
    #     dom_con = Contar[0]
    #     Contar.pop(0)
    #     Contar.append(dom_con)
    
    # print("Dias_da_semana"+str(Dias_da_semana))

    # if len(MUNICIPIO):
    #     dom_muni = MUNICIPIO[0]
    #     MUNICIPIO.pop(0)
    #     MUNICIPIO.append(dom_muni)
    
    # print()


    color_discrete_map ={
                            "Palmela":"#7AABE5",
                            "Sesimbra": "#D35C59",
                            "Outros": "#FCB454",
                            "Setúbal": "#61DBA7"
                        }
    # print("DATA"+str(data))
    figure = px.area(  { "Contagem": Contar,
                        "Dias da semana": Dias_da_semana,
                        "Município": MUNICIPIO }, 
                        x="Dias da semana", 
                        y="Contagem",
                        color_discrete_map=color_discrete_map,
                        color="Município",
                        line_group="Município"
                    )
    

    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def piechart_padrão_do_fim_de_semana(filter):
    str_query = "[{'$project':{'dayOfWeek':{'$dayOfWeek':'$DATETIME'},'consumo':'$CONSUMO'}},{'$project':{'res':{'$switch':{'branches':[{'case':{'$in':['$dayOfWeek',[1,7]]},'then':'Fim de semana'},{'case':{'$in':['$dayOfWeek',[2,3,4,5,6]]},'then':'Dias da semana'}]}},'consumo':'$consumo'}},{'$group':{'_id':'$res','count':{'$sum':'$consumo'}}}]"
    pipeline = json.loads(str_query.replace("'",'"'))
    if filter != "":
        pipeline.insert(0,filter)

    data = list(mydb.DATA.aggregate(pipeline))

    labels = [ d['_id'] for d in data ]
    values = [ d['count'] for d in data ]
    color_discrete_map = {
                            "Dias da semana":"#7AABE5",
                            "Fim de semana": "#0066CC"
                        }
    figure = px.pie({'value': values,'label':labels}, 
        values='value',
        names='label',
        hole=0.0,
        color_discrete_map=color_discrete_map,
        color='label',
    )
    figure.update_traces(
        hoverinfo='label+percent',
        textinfo='label+percent',
        textfont_size=20,
        # paper_bgcolor='rgb(244, 244, 244)',
        # marker=dict(colors=colors)
    )
    

    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure

def barchart_tempordas(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id':{'month':{'$month':{'$dateFromString':{'dateString':'$Date'}}}},'data':{'$sum':{'$sum': {'$toDouble': '$Consumo' }}}}},{'$project':{'res':{'$switch':{'branches':[{'case':{'$in':['$_id.month',[12,1,2]]},'then':'Winter'},{'case':{'$in':['$_id.month',[3,4,5]]},'then':'Spring'},{'case':{'$in':['$_id.month',[6,7,8]]},'then':'Summer'},{'case':{'$in':['$_id.month',[9,10,11]]},'then':'Antumn'}]}},'data':1}},{'$group':{'_id':{'season':'$res'},'count':{'$sum':'$data'}}},{'$project':{'Sazonalidade':'$_id.season','Soma':'$count','_id':0}}]"
    pipeline = json.loads(str_query.replace("'",'"'))
    
    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))
    print("B-A-R-C-H-A-R-T")
    print(data)
    print("B-A-R-C-H-A-R-T")
    Contar = [ d['Soma'] for d in data ]
    Temporadas = [ d['Sazonalidade'] for d in data ]

    color_discrete_map ={
                            "Winter":"#02124F",
                            "Spring": "#CA3A38",
                            "Summer": "#D77C04",
                            "Antumn": "#1A764E"
                        }
    figure = px.bar({ "Soma": Contar,
                            "Sazonalidade": Temporadas,
                        }, 
                        x="Soma", 
                        y="Sazonalidade",
                        color_discrete_map=color_discrete_map
                    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # print("DATA"+str(data))
    return figure
def geomap(filter):
    str_query = "[{'$addFields':{'DATETIME':{'$dateFromString':{'dateString':'$Date'}}}},{'$group':{'_id': {'LONGITUDE': '$LONGITUDE', 'LATITUDE': '$LATITUDE'},'data':{'$first': '$NOME'}}},{'$project': {'lon': '$_id.LONGITUDE','lat':'$_id.LATITUDE','name': '$data','_id':0}}]"
    pipeline = json.loads(str_query.replace("'",'"'))

    if filter != "":
        pipeline.insert(1,filter)

    data = list(mydb.MAIA.aggregate(pipeline))

    geojson = dicts_to_geojson([{**d, **dict(tooltip=d['name'])} for d in data])
    dd_options = [dict(value=c['name'], label=c['name']) for c in data]
    dd_defaults = [o['value'] for o in dd_options]
    dd_defaults = list(set(dd_defaults))

    point_to_layer = assign("""function(feature, latlng, context){
        return L.circleMarker(latlng);  // sender a simple circle marker.
    }""")
    map = Map(
        children=[
            TileLayer(),
            GeoJSON(
                data=geojson, hideout=dd_defaults, id='geojson', zoomToBounds=True, options=dict(pointToLayer=point_to_layer)
            )
        ], style={'width': '100%', 'height': '50vh', 'margin': 'auto', 'display': 'block'}, id='geomap'
    )
    return geojson