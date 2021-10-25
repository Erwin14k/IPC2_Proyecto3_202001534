from flask import Flask,jsonify
from flask_cors import CORS
from flask.globals import request
import json
from DTE_DAO import DTE_DAO
from DTE_DAO import error_dao_handler
import xmltodict
dte_dao_handler=DTE_DAO()
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1>Ruta Principal 14k</h1>"

@app.route('/send', methods=['POST'])
def add_dte():
    if request.method == 'POST':
        params=request.get_json()
        for dte in params['dte']:
            date = dte['date']
            reference=dte['reference']
            emmiter_nit=dte['emmiter_nit']
            reciever_nit=dte['reciever_nit']
            value=dte['value']
            tax=dte['tax']
            total=dte['total']
            false_counter=0
            if dte_dao_handler.validate_emitter_nit(date,emmiter_nit):
                false_counter=false_counter
            else:
                false_counter+=1
            if dte_dao_handler.validate_reciever_nit(date,reciever_nit):
                false_counter=false_counter
            else:
                false_counter+=1
            if dte_dao_handler.validate_value_tax_and_total(date,value,tax,total):
                false_counter=false_counter
            else:
                false_counter+=1
            if dte_dao_handler.validate_reference(date,reference):
                false_counter=false_counter
            else:
                false_counter+=1

            if false_counter >0:
                dte_dao_handler.new_declined_dte(reference,emmiter_nit,reciever_nit,date,value,tax,total)
            else:
                dte_dao_handler.new_dte(reference,emmiter_nit,reciever_nit,date,value,tax,total)
        dte_dao_handler.print_all_dte()
        dte_dao_handler.xml_creator()
        error_dao_handler.print_all_errors()
        return jsonify({"status": 200, "mensaje": "Se guardaron con éxito los DTE correctos."})
        


#dte_dao_handler.validate_emitter_nit("15/01/2021","24959111")
#dte_dao_handler.validate_emitter_nit("15/01/2021","26706288")

@app.route('/date_filter_2', methods=['GET'])
def date_filter2():
    if request.method == 'GET':       
        route = "C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Tools/graphics_info.json"
        with open(route, 'r') as myfile:
            information = myfile
        return information
@app.route('/date_filter', methods=['GET'])
def date_filters():
    print("kkkkkkkkkkkkkkkkkkkkkkkkk")
    if request.method == 'GET':       
        route = "C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Tools/out.xml"
        with open(route, 'r') as myfile:
            obj = xmltodict.parse(myfile.read())
            print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
        return jsonify(json.dumps(obj))

if __name__ == "__main__":
    app.run(threaded=True, port=5000,debug=True)
