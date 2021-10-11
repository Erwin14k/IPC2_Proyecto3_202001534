from flask import Flask,jsonify
from flask_cors import CORS
from flask.globals import request
import json
from DTE_DAO import DTE_DAO
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
            if dte_dao_handler.validate_emitter_nit(date,emmiter_nit) and dte_dao_handler.validate_reciever_nit(date,reciever_nit) and dte_dao_handler.validate_value_tax_and_total(date,value,tax,total):
                dte_dao_handler.new_dte(reference,emmiter_nit,reciever_nit,date,value,tax,total)
        dte_dao_handler.print_all_dte()
        return jsonify({"status": 200, "mensaje": "Se guardaron con éxito los DTE correctos."})
        




if __name__ == "__main__":
    app.run(threaded=True, port=5000,debug=True)
    
