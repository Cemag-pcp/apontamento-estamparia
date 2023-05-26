from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)
# app.config.from_pyfile('config.py')

# Função para obter os dados da planilha
def get_sheet_data():

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(credentials)
    sa = gspread.service_account('service_account.json')    

    name_sheet1 = 'RQ PCP-003-001 (APONTAMENTO ESTAMPARIA) / RQ PCP-009-000 (SEQUENCIAMENTO ESTAMPARIA) e RQ CQ-015-000 (Inspeção da Estamparia)'
    worksheet1 = 'OPERADOR 4217'
    sh1 = sa.open(name_sheet1)
    wks1 = sh1.worksheet(worksheet1)
    list1 = wks1.get()

    header = wks1.row_values(5)

    table1 = pd.DataFrame(list1)     
    table1 = table1.set_axis(header, axis=1)

    table1 = table1.iloc[5:]
    
    table1.reset_index(drop=True)

    table1 = table1.loc[(table1['QTD REALIZADA'] == '') & (table1['CÓDIGO'] != '') & (table1['MÁQUINA'] == '')]

    values = table1.values.tolist()
    
    return values, table1

sheet_data, table1 = get_sheet_data()

# Rota inicial da aplicação
@app.route('/')
def index():
    sheet_data, table1 = get_sheet_data()
    return render_template('index.html', sheet_data=sheet_data)

# Rota para enviar a linha para outra planilha
@app.route('/send_row', methods=['POST'])
def send_row():

    row_data = request.json['row_data']
    dropdown1Value = request.json['dropdown1_value']
    dropdown2Value = request.json['dropdown2_value']

    id_tabela = row_data[0]
    maquina = dropdown1Value
    quantidade_realizada = row_data[5]
    finalizou = dropdown2Value

    print(id_tabela, maquina, quantidade_realizada, finalizou)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
