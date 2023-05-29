from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)
# app.config.from_pyfile('config.py')

# Função para obter os dados da planilha
def get_sheet_data_4238():

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(credentials)
    sa = gspread.service_account('service_account.json')    

    name_sheet1 = 'RQ PCP-003-001 (APONTAMENTO ESTAMPARIA) / RQ PCP-009-000 (SEQUENCIAMENTO ESTAMPARIA) e RQ CQ-015-000 (Inspeção da Estamparia)'
    worksheet1 = 'OPERADOR 4238'
    sh1 = sa.open(name_sheet1)
    wks1 = sh1.worksheet(worksheet1)
    list1 = wks1.get()

    header = wks1.row_values(4)

    table1 = pd.DataFrame(list1)     
    table1 = table1.set_axis(header, axis=1)

    table1 = table1.iloc[4:]
    
    table1.reset_index(drop=True)

    table1 = table1.loc[(table1['CÓDIGO'] != '') & (table1['MÁQUINA'] == '')]

    table1 = table1[(table1['Finalizou?'] == 'Não') | (table1['Finalizou?'] == '')]

    values = table1.values.tolist()
    
    return values, table1

def att_linha(id, qtReal, maquina, qtMortas, finalizou):

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(credentials)
    sa = gspread.service_account('service_account.json')    

    name_sheet1 = 'RQ PCP-003-001 (APONTAMENTO ESTAMPARIA) / RQ PCP-009-000 (SEQUENCIAMENTO ESTAMPARIA) e RQ CQ-015-000 (Inspeção da Estamparia)'
    worksheet1 = 'OPERADOR 4238'
    sh1 = sa.open(name_sheet1)
    wks1 = sh1.worksheet(worksheet1)
    list1 = wks1.get()

    header = wks1.row_values(4)

    table1 = pd.DataFrame(list1)     
    table1 = table1.set_axis(header, axis=1)

    table1 = table1.iloc[4:]
    
    table1.reset_index(drop=True)

    table1 = table1[table1['ID'] == id]

    linha_planilha = table1.index[0]

    wks1.update("F" + str(linha_planilha + 1), qtReal) # qt real
    wks1.update("I" + str(linha_planilha + 1), qtMortas) # qt morta
    wks1.update("G" + str(linha_planilha + 1), maquina) # maquina
    wks1.update("M" + str(linha_planilha + 1), finalizou) # finalizou

# Rota inicial da aplicação
@app.route('/')
def index():
    sheet_data, table1 = get_sheet_data_4238()
    return render_template('index.html', sheet_data=sheet_data)

# Rota para enviar a linha para outra planilha
@app.route('/send_row', methods=['POST'])
def send_row():

    if request.method == 'POST':

        linha = request.get_json()  # Obter os dados da linha enviados pelo front-end

        id_linha = linha[0]
        qtReal = linha[5]
        maquina = linha[7]
        qtMortas = linha[6]
        finalizou = linha[8]

        print(id_linha, qtReal, maquina, qtReal, finalizou)

        att_linha(id_linha, qtReal, maquina, qtMortas, finalizou)
        print("ok, atualizou")
        
        #retorna mensagem de sucesso

        return render_template('index.html', sheet_data=sheet_data)

    else:
        sheet_data, table1 = get_sheet_data_4238()
        return render_template('index.html', sheet_data=sheet_data)

if __name__ == '__main__':
    app.run(debug=True)
