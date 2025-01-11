import streamlit as st
import os
import json
import datetime
import time

def msg_sucesso():
    st.success("Operação realizada com sucesso!")
    time.sleep(1)
    #st.rerun()

def verifica_se_existe(caminho):
    if os.path.isfile(caminho):
        return True
    else:
        return False

def verifica_se_agente_existe(agente_a_inserir):
    caminho = "db/agentes.json"
    lista_agentes = ler_arquivo(caminho)
    for agente_encontrado in lista_agentes:
        if agente_encontrado['matricula'] == agente_a_inserir['matricula']:
            return True
        
    return False

def validar_formulario(nome, matricula, graduacao, face):
    if(not nome or not matricula or not graduacao or not face):
        st.error('Preencha todos os campos antes de continuar.')
        return False
    return True

def gerar_string_momento_atual():
    momento_atual = datetime.datetime.now()
    momento_atual_string = momento_atual.strftime(format="%d-%m-%Y-%H-%M-%S-%f")
    return momento_atual_string

def ler_arquivo(caminho):
    if os.path.isfile(caminho):
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            res = json.load(arquivo)
            return res

# def salvar_face(face, nome):
#     if face is not None:
#         pasta = 'uploaded_faces'
#         os.makedirs('uploaded_faces', exist_ok=True)
#         caminho = os.path.join(pasta, nome)
#         with open(caminho, 'wb') as arquivo:
#             arquivo.write(face.getbuffer())

def salvar_face(face, nome, pasta):
    if face is not None and hasattr(face, 'getbuffer'):
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome)        
        with open(caminho, 'wb') as arquivo:
            arquivo.write(face.getbuffer())
    else:
        print("O objeto 'face' não é válido ou não possui o método 'getbuffer'.")


def inserir_cadastro(nome, matricula, graduacao, face):
    if validar_formulario(nome, matricula, graduacao, face):
        caminho = "db/agentes.json"
        ext = face.name.split('.')[1]
        agente = {
            "nome": nome.upper(),
            "matricula": matricula.upper(),
            "graduacao": graduacao.upper(),
            "img": f"{gerar_string_momento_atual()}.{ext}"
        }
        if not verifica_se_existe(caminho):
            lista = []
            lista.append(agente)
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                json.dump(lista, arquivo, ensure_ascii=False, indent=4)

            salvar_face(face, agente['img'], 'uploaded_faces')
            msg_sucesso()
        else:
            if not verifica_se_agente_existe(agente):
                lista = ler_arquivo(caminho)
                lista.append(agente)
                with open(caminho, 'w', encoding='utf-8') as arquivo:
                    json.dump(lista, arquivo, ensure_ascii=False, indent=4)

                salvar_face(face, agente['img'], 'uploaded_faces')
                msg_sucesso()
    



