from flask import Flask, request
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1> Hola Mundo </h1>"

@app.route('/hello/<string:name>')
def grettings(name):
    return "<h1> Hola Mundo "+ name +  "</h1>"


#https://www.alkosto.com/fuente

#https://www.alkosto.com/?fuente=google&medio=cpc&campaign=AK_COL_SEM_PEF_CPC_PB_AON_TLP_TLP_Brand-General-AON_PAC&keyword=alkosto&gad_source=1&gad_campaignid=2018735487&gbraid=0AAAAADlnVbhjpa2yNJXbRpygnnsX8VizY&gclid=CjwKCAiAvaLLBhBFEiwAYCNTf7C40kfNPJpky3V0zSRGu-gSyhJjIbLtlSTqw3Q8kPaLJiK2O4N3lBoCGjoQAvD_BwE
#https://listado.mercadolibre.com.co/planta#D[A:planta]&origin=UNKNOWN&as.comp_t=SUG&as.comp_v=lapto&as.comp_id=SUG
#https://www.amazon.com/s?k=planta&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1FUXXWEL7GE7T&sprefix=planta%2Caps%2C167&ref=nb_sb_noss_1

saludo = {"ES": "Hola Mundo",
          "EN": "Hello World"}

@app.route('/dynamic-hello/<string:name>/')
def data(name):
    language = request.args.get("language", "EN")
    uppercase = request.args.get("uppercase", False)
    phase = saludo[language] + " " + name
    if uppercase == "True" or uppercase == "true":
        phase = phase.upper()
    return "<h1>" + phase + "</h1>"

plantas = { "1": {"name": "Rosa", "Irrigation": 3, "Requirement": "Luz solar directa", "Size": 90, "price": 12000},
        "2": {"name": "Aloe vera", "Irrigation": 2, "Requirement": "Luz solar indirecta", "Size": 60, "price": 12000},
        "3": {"name": "Girasol", "Irrigation": 3, "Requirement": "Luz solar directa", "Size": 100, "price": 10000},
        "4": {"name": "Orquidea", "Irrigation": 2, "Requirement": "Luz solar indirecta", "Size": 90, "price": 15000},
        "5": {"name": "Cactus", "Irrigation": 1, "Requirement": "Luz solar directa", "Size": 60, "price": 10000} }


@app.route('/api/planta/<string:id>/',methods = ["GET"])
def get_planta(id):   
    if id in plantas:
        return plantas[id], 200
    else:
        return {"message": "planta with "+id+" not found"}, 404
    
@app.route('/api/plantas/')
def get_plantas(): 
    Irrigation = request.args.get("Irrigation",0)
    Size =  request.args.get("Size",0)   
    filtered = list(filter(lambda key : plantas[key]["Irrigation"] >= int(Irrigation) 
                           and plantas[key]["Size"] >= int(Size) , plantas))
    return list(map(lambda k: plantas[k], filtered))


@app.route('/api/planta/', methods = ["POST"])
def post_plantas():
    body = request.json
    copy = body.copy()
    new_id = body["id"]
    if new_id in plantas:
        return {"message": "planta with id "+new_id + " already exist" }, 409    
    else:
        del body["id"]
        plantas[new_id] = body   
        return copy, 201
    

@app.route('/api/planta/<string:id>/', methods=["PATCH"])
def put_laptop(id):
    body = request.json
    price = body.get("price")
    name = body.get("name")
    if id in plantas:
        if price != None:
            plantas[id]["price"] = price
        if name != None:
            plantas[id]["name"] = name
        return plantas[id], 200
    else:
        return {"messsage": "planta with "+id+" not found"}, 404
    

@app.route('/api/plantas/', methods=["DELETE"])
def delete_plantas():
    global plantas
    if plantas:
        plantas_copy = plantas.copy()
        plantas.clear()
        return {"message": "All plantas deleted"}, 200
    else:
        return {"message": "No plantas to delete"}, 404
    

if __name__ == '__main__':
    app.run(debug=True,
            port=8002, 
            host='0.0.0.0')