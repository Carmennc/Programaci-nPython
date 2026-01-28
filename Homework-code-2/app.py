from flask import Flask, request, render_template_string
import uuid
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt


app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'informacion-privada'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)

jwt = JWTManager(app)
host = 'mongodb://localhost'
port = 27017
db_name = 'planta_flask'
# admin , manager , user
user_collection = None
planta_collection = None

def connect_db():
    try:
        client = MongoClient(host+":"+str(port)+"/")
        db = client[db_name]
        client.admin.command('ping')
        global user_collection
        user_collection = db.users
        global planta_collection
        planta_collection = db.plantas
        print("✅ Conexión a MongoDB exitosa")
        print(f"DB Check : {db!=None}")        
        print(f"DB planta_collection : {planta_collection!=None}") 
        print(f"DB user_collection : {user_collection!=None}")         
    except Exception as e:
        pass
 
# Returns list    
def check_if_usr_exist(username): 
    global user_collection
    print(f"Debug username: {username}")
    query = {"username" : {"$eq": username }}
    return list(user_collection.find(query))
    
def create_usr(usr):
    global user_collection
    result = user_collection.insert_one(usr)
    print( f"DEBUG ID value {result.inserted_id} type {type(result.inserted_id)}")
    usr["_id"] = str(result.inserted_id)
    return usr

def create_admin_if_exist(usr):
    check_admin = check_if_usr_exist(usr["username"])
    if len(check_admin) > 0:
        return check_admin
    else:
        return create_usr(usr)

def get_token_role():
    try:
        claims = get_jwt()
        return claims.get('role','user')
    except:
        return None
    

def manager_required(f):
    @jwt_required()
    def custom_validation(*args,**kwargs):
        role = get_token_role()
        if role == 'manager' or role == 'admin' :
            return f(*args,**kwargs)
        else:
            print(f"Debug Role: {role}")
            return {
                'error': 'Acceso denegado',
                'message': 'Solo los manager pueden acceder a este endpoint'
            }, 403
    return custom_validation


def admin_required(f):
    @jwt_required()
    def manager_validation(*args,**kwargs):
        role = get_token_role()
        if role == 'admin':
            return f(*args,**kwargs)
        else:
            print(f"Debug Role: {role}")
            return {
                'error': 'Acceso denegado',
                'message': 'Solo los admin pueden acceder a este endpoint'
            }, 403
    return manager_validation  



@app.route('/api/planta/<string:id>/',methods = ["GET", "DELETE"])
@jwt_required()
def get_planta(id):   
    print(f"METHOD {request.method}")
    global planta_collection
    found = planta_collection.find_one({"_id": ObjectId(id)})
    found["_id"] = str(found["_id"])
    if request.method == "GET":        
        if id is not None:
            return found, 200
        else:
            return {"messsage": "planta with "+id+" not found"}, 404
    else:
        if id is not None:
            planta_collection.delete_one({"_id": ObjectId(id)})
            return found , 200
        else:
            return {}, 204
    
def normalize_id(item):
    item["_id"] = str(item["_id"])
    return item    
    
@app.route('/api/plantas/')
@jwt_required()
def get_plantas(): 
    Irrigation = request.args.get("Irrigation",0)
    Size =  request.args.get("Size",0)   
    query = {"Irrigation" : {"$gte": int(Irrigation) },
             "Size" : {"$gte": int(Size) }}
    global planta_collection    
    result = list(planta_collection.find(query))
    results = list(map(lambda pla: normalize_id(pla), result))
    return result, 200

def insert_planta(body):
    global planta_collection    
    result = planta_collection.insert_one(body)
    body["_id"] = str(result.inserted_id)
    return body

@app.route('/api/planta/', methods = ["POST"])
@manager_required
def POST_plantas():   
    return insert_planta(request.json), 200    
 
@app.route('/api/planta/<string:id>/', methods=["PATCH"])
@jwt_required()
def put_planta(id):
    body = request.json
    price = body.get("price")
    name = body.get("name")
    found = planta_collection.find_one({"_id": ObjectId(id)})
    query = {"$set":{}}
    if found is not None:
        if price != None:
            query["$set"]["price"] = price
        if name != None:
            query["$set"]["name"] = name
        planta_collection.update_one({"_id": ObjectId(id)}, query)
        found = planta_collection.find_one({"_id": ObjectId(id)})
        found["_id"] = str(found["_id"])
        return found , 200
    else:
        return {"messsage": "planta with "+id+" not found"}, 404

@app.route('/api/admin/signIn/manager', methods= ['POST'])
@admin_required
def admin_sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos invalidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        if len(check_if_usr_exist(username)) >0:
            return {
            'error': 'Datos invalidos',
            'message': 'el usuario ya existe'}, 400
        else:
            new_user = {
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'manager'
            }
            user_created = create_usr(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'manager'}, 201
   

@app.route('/api/signIn', methods= ['POST'])
def sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos invalidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        if len(check_if_usr_exist(username) ) >0:
            return {
            'error': 'Datos invalidos',
            'message': 'el usuario ya existe'}, 400
        else:
            new_user = {
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'user'
            }
            user_created = create_usr(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'user'}, 201
        
@app.route('/api/signIn/customer', methods= ['POST'])
def customer_sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos invalidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        if len(check_if_usr_exist(username) ) >0:
            return {
            'error': 'Datos invalidos',
            'message': 'el usuario ya existe'}, 400
        else:
            new_user = {
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'customer'
            }
            user_created = create_usr(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'customer'}, 201
        
@app.route('/api/login', methods= ['POST'])
def log_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos invalidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        body_password = request.json['password']
        if len(check_if_usr_exist(username) ) == 0:
            return {
            'error': 'Datos invalidos',
            'message': 'el usuario no existe'}, 400
        else:
            user = check_if_usr_exist(username)[0]
            user_password = user["password_hash"]
            if check_password_hash(user_password, body_password):
                token = create_access_token(identity=username,additional_claims={
                    "user_id" : user.get('user_id'),
                     "role": user.get('role')
                })
                return { 'message': "login correcto",
                        'token': token}, 200
            else:
                 return { 'message': "contraseña incorrecta"}, 401
   
        

#https://www.alkSizeto.com/fuente

#https://www.alkSizeto.com/?fuente=google&medio=cpc&campaign=AK_COL_SEM_PEF_CPC_PB_AON_TLP_TLP_Brand-General-AON_PAC&keyword=alkSizeto&gad_source=1&gad_campaignid=2018735487&gbraid=0AAAAADlnVbhjpa2yNJXbRpygnnsX8VizY&gclid=CjwKCAiAvaLLBhBFEiwAYCNTf7C40kfNPJpky3V0zSRGu-gSyhJjIbLtlSTqw3Q8kPaLJiK2O4N3lBoCGjoQAvD_BwE
#https://listado.mercadolibre.com.co/planta#D[A:planta]&origin=UNKNOWN&as.comp_t=SUG&as.comp_v=plato&as.comp_id=SUG
#https://www.amazon.com/s?k=planta&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1FUXXWEL7GE7T&sprefix=planta%2Caps%2C167&ref=nb_sb_nSizes_1
tienda = {"ES": "Jardín Verde",
         "EN": "Green Garden"}

@app.route('/dynamic-home')
def tienda_plantas():
    """Tienda de plantas - página principal"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jardín Verde - Tienda de plantas</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(45deg, #27ae60, #229954); 
                margin: 0; 
                padding: 50px; 
                min-height: 100vh; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            .card { 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                text-align: center; 
                max-width: 400px; 
            }
            h1 { 
                color: #27ae60; 
                margin-bottom: 10px; 
            }
            p { 
                color: #666; 
                line-height: 1.6; 
            }
            .highlight { 
                background: #27ae60; 
                color: white; 
                padding: 5px 10px; 
                border-radius: 20px; 
                display: inline-block; 
                margin: 10px 0; 
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌿 Jardín Verde - Plantas</h1>
            <p>Tu vivero de confianza para plantas de calidad.</p>
            <div class="highlight">{{ fecha_hora }}</div>
            <p>🌱 Inventario: <strong>{{ estado_bd }}</strong></p>
        </div>
    </body>
    </html>
    """
    global planta_collection
    return render_template_string(
        html_content, 
        fecha_hora=datetime.now().strftime("%d/%m/%Y - %H:%M:%S"), 
        estado_bd="En Línea" if planta_collection != None else "Fuera de Línea"
    )
   
            
if __name__ == '__main__':
    connect_db()
    admin_usr =    {
                'username': "admin",
                'password_hash': generate_password_hash('123456'),
                'created_at': datetime.now(),
                'role': "admin"
            }
    print( f"Admin user: {create_admin_if_exist(admin_usr)}")
    app.run(debug=True,
            port=8002, 
            host='0.0.0.0')