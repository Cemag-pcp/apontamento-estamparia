from flask import Flask, render_template, request, jsonify,redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

app = Flask(__name__)
# app.config.from_pyfile('config.py')

# Função para obter os dados da planilha

# Rota inicial da aplicação
@app.route('/4238')
def operador_4238():

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

        table1.fillna('',inplace=True)

        table1 = table1[(table1['MÁQUINA'] == '') & (table1['CÓDIGO'] != '')]
                        
        table1 = table1[(table1['Finalizou?'] == 'Não') | (table1['Finalizou?'] == '')]

        values = table1.values.tolist()
        
        return values, table1

    sheet_data, table1 = get_sheet_data_4238()
    print(table1)

    return render_template('operador_4238.html', sheet_data=sheet_data)

# Rota para enviar a linha para outra planilha
@app.route('/send_row_4238', methods=['POST'])
def send_row_4238():

    def att_linha(id, qtReal, maquina, qtMortas, finalizou,motivo):

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
        wks1.update("J" + str(linha_planilha + 1), motivo) # motivo


    if request.method == 'POST':

        linha = request.get_json()  # Obter os dados da linha enviados pelo front-end

        id_linha = linha[0]
        qtReal = linha[5]
        maquina = linha[8]
        qtMortas = linha[6]
        finalizou = linha[9]
        motivo = linha[7]

        print(linha)

        att_linha(id_linha, qtReal, maquina, qtMortas, finalizou, motivo)
        print("ok, atualizou")
        
        #sheet_data, table1 = get_sheet_data_4238()

        #retorna mensagem de sucesso
        return jsonify({'mensagem': 'Dados enviados com sucesso'})

# Rota inicial da aplicação
@app.route('/')
def operador_4217():

    def get_sheet_data_4217():

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

        table1.fillna('',inplace=True)

        table1 = table1.loc[(table1['CÓDIGO'] != '') & (table1['MÁQUINA'] == '')]

        table1 = table1[(table1['Finalizou?'] == 'Não') | (table1['Finalizou?'] == '')]

        values = table1.values.tolist()
        
        return values, table1

    sheet_data, table1 = get_sheet_data_4217()
    print(table1)

    return render_template('operador_4217.html', sheet_data=sheet_data)

# Rota para enviar a linha para outra planilha
@app.route('/send_row_4217', methods=['POST'])
def send_row_4217():

    def att_linha(id, qtReal, maquina, qtMortas, finalizou, motivo):

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

        table1 = table1[table1['ID'] == id]

        linha_planilha = table1.index[0]

        wks1.update("F" + str(linha_planilha + 1), qtReal) # qt real
        wks1.update("I" + str(linha_planilha + 1), qtMortas) # qt morta
        wks1.update("G" + str(linha_planilha + 1), maquina) # maquina
        wks1.update("M" + str(linha_planilha + 1), finalizou) # finalizou
        wks1.update("J" + str(linha_planilha + 1), motivo) # motivo

    if request.method == 'POST':

        linha = request.get_json()  # Obter os dados da linha enviados pelo front-end

        id_linha = linha[0]
        qtReal = linha[5]
        maquina = linha[8]
        qtMortas = linha[6]
        finalizou = linha[9]
        motivo = linha[7]

        print(id_linha, qtReal, maquina, qtReal, finalizou)

        att_linha(id_linha, qtReal, maquina, qtMortas, finalizou, motivo)
        print("ok, atualizou")
        
        #sheet_data, table1 = get_sheet_data_4238()

        #retorna mensagem de sucesso
        return jsonify({'mensagem': 'Dados enviados com sucesso'})

# Rota inicial da aplicação
@app.route('/3654')
def operador_3654():

    def get_sheet_data_3654():

        scope = ['https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive"]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(credentials)
        sa = gspread.service_account('service_account.json')    

        name_sheet1 = 'RQ PCP-003-001 (APONTAMENTO ESTAMPARIA) / RQ PCP-009-000 (SEQUENCIAMENTO ESTAMPARIA) e RQ CQ-015-000 (Inspeção da Estamparia)'
        worksheet1 = 'OPERADOR 3654'
        sh1 = sa.open(name_sheet1)
        wks1 = sh1.worksheet(worksheet1)
        list1 = wks1.get()

        header = wks1.row_values(5)

        table1 = pd.DataFrame(list1)     
        table1 = table1.set_axis(header, axis=1)

        table1 = table1.iloc[5:]
        
        table1.reset_index(drop=True)

        table1.fillna('',inplace=True)

        table1 = table1.loc[(table1['CÓDIGO'] != '') & (table1['MÁQUINA'] == '')]

        table1 = table1[(table1['Finalizou?'] == 'Não') | (table1['Finalizou?'] == '')]

        values = table1.values.tolist()
        
        return values, table1

    sheet_data, table1 = get_sheet_data_3654()
    print(table1)

    return render_template('operador_3654.html', sheet_data=sheet_data)

# Rota para enviar a linha para outra planilha
@app.route('/send_row_4217', methods=['POST'])
def send_row_3654():

    def att_linha(id, qtReal, maquina, qtMortas, finalizou, motivo):

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

        table1 = table1[table1['ID'] == id]

        linha_planilha = table1.index[0]

        wks1.update("F" + str(linha_planilha + 1), qtReal) # qt real
        wks1.update("I" + str(linha_planilha + 1), qtMortas) # qt morta
        wks1.update("G" + str(linha_planilha + 1), maquina) # maquina
        wks1.update("M" + str(linha_planilha + 1), finalizou) # finalizou
        wks1.update("J" + str(linha_planilha + 1), motivo) # motivo

    if request.method == 'POST':

        linha = request.get_json()  # Obter os dados da linha enviados pelo front-end

        id_linha = linha[0]
        qtReal = linha[5]
        maquina = linha[8]
        qtMortas = linha[6]
        finalizou = linha[9]
        motivo = linha[7]

        print(id_linha, qtReal, maquina, qtReal, finalizou)

        att_linha(id_linha, qtReal, maquina, qtMortas, finalizou,motivo)
        print("ok, atualizou")
        
        #sheet_data, table1 = get_sheet_data_4238()

        #retorna mensagem de sucesso
        return jsonify({'mensagem': 'Dados enviados com sucesso'})

# Rota inicial da aplicação
@app.route('/4200')
def operador_4200():

    def get_sheet_data_4200():

        scope = ['https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive"]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(credentials)
        sa = gspread.service_account('service_account.json')    

        name_sheet1 = 'RQ PCP-003-001 (APONTAMENTO ESTAMPARIA) / RQ PCP-009-000 (SEQUENCIAMENTO ESTAMPARIA) e RQ CQ-015-000 (Inspeção da Estamparia)'
        worksheet1 = 'OPERADOR 4200'
        sh1 = sa.open(name_sheet1)
        wks1 = sh1.worksheet(worksheet1)
        list1 = wks1.get()

        header = wks1.row_values(5)

        table1 = pd.DataFrame(list1)     
        table1 = table1.iloc[:,:14].set_axis(header, axis=1)

        table1 = table1.iloc[5:]
        
        table1.reset_index(drop=True)

        table1.fillna('',inplace=True)

        table1 = table1.loc[(table1['CÓDIGO'] != '') & (table1['MÁQUINA'] == '')]

        table1 = table1[(table1['Finalizou?'] == 'Não') | (table1['Finalizou?'] == '')]

        values = table1.values.tolist()
        
        return values, table1

    sheet_data, table1 = get_sheet_data_4200()
    print(table1)

    return render_template('operador_4200.html', sheet_data=sheet_data)

# Rota para enviar a linha para outra planilha
@app.route('/send_row_4200', methods=['POST'])
def send_row_4200():

    def att_linha(id, qtReal, maquina, qtMortas, finalizou, motivo):

        scope = ['https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive"]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(credentials)
        sa = gspread.service_account('service_account.json')    

        name_sheet1 = 'RQ PCP-003-001 (APONTAMENTO ESTAMPARIA) / RQ PCP-009-000 (SEQUENCIAMENTO ESTAMPARIA) e RQ CQ-015-000 (Inspeção da Estamparia)'
        worksheet1 = 'OPERADOR 4200'
        sh1 = sa.open(name_sheet1)
        wks1 = sh1.worksheet(worksheet1)
        list1 = wks1.get()

        header = wks1.row_values(5)

        table1 = pd.DataFrame(list1)     
        table1 = table1.iloc[:,:14].set_axis(header, axis=1)

        table1 = table1.iloc[5:]
        
        table1.reset_index(drop=True)

        table1 = table1[table1['ID'] == id]

        linha_planilha = table1.index[0]

        wks1.update("F" + str(linha_planilha + 1), qtReal) # qt real
        wks1.update("I" + str(linha_planilha + 1), qtMortas) # qt morta
        wks1.update("G" + str(linha_planilha + 1), maquina) # maquina
        wks1.update("M" + str(linha_planilha + 1), finalizou) # finalizou
        wks1.update("J" + str(linha_planilha + 1), motivo) # motivo

    if request.method == 'POST':

        linha = request.get_json()  # Obter os dados da linha enviados pelo front-end

        id_linha = linha[0]
        qtReal = linha[5]
        maquina = linha[8]
        qtMortas = linha[6]
        finalizou = linha[9]
        motivo = linha[7]

        print(id_linha, qtReal, maquina, qtReal, finalizou, motivo)

        att_linha(id_linha, qtReal, maquina, qtMortas, finalizou, motivo)
        print("ok, atualizou")
        
        #sheet_data, table1 = get_sheet_data_4238()

        #retorna mensagem de sucesso
        return jsonify({'mensagem': 'Dados enviados com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)
