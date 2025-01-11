import streamlit as st
from utils import conn
import os
import json
import time
from deepface import DeepFace
from utils import conn

destino = "upload_temp"

st.write("""
    <style>
         h1, h2, h3, h4, p{
            width: 100%;
            text-align: center;
         }
        .area_msg{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 10px;
            background-color: none;
            margin-top: 30px;
        }
        img{
            width: 70px;
        }
        .texto{
            text-align: center;
            width: 250px;
        }

    </style>
""", unsafe_allow_html=True)

st.write('### Confirmação de Presença')

matricula = st.text_input('Informa a matrícula do agente')
entrada = st.file_uploader("Imagem do agente")



if st.button("INICIAR RECONHECIMENTO FACIAL"):
    if not matricula:
        st.error('O campo matrícula é obrigatório.')
    elif entrada == None:
        st.error('Envie uma imagem do agente para continuar.')
    else:  
        if conn.verifica_se_agente_existe({'matricula': matricula}):
            caminho_img2 = ''
            if os.path.isfile('db/agentes.json'):
                with open('db/agentes.json', 'r') as arquivo:
                    agentes = json.load(arquivo)
                    for agente in agentes:
                        if agente['matricula'] == matricula:
                            nome = 'temp'
                            conn.salvar_face(entrada, nome, destino)
                            #st.write(f'### {agente['graduacao']} {agente['nome']}')

                            caminho_img2 = f'uploaded_faces/{agente['img']}'

                            placeholder = st.empty()
                            placeholder.write("""
                                <div class='area_msg'>
                                    <img src='https://th.bing.com/th/id/R.bb01ab84dfdb6aeceb578d37f5d388eb?rik=v4uPpPrfY5ll0Q&riu=http%3a%2f%2fportal.ufvjm.edu.br%2fa-universidade%2fcursos%2fgrade_curricular_ckan%2floading.gif&ehk=ds5MQkjMPrEiICt9x0IUfY7cEV5HYfovGFN2cNoPRfI%3d&risl=&pid=ImgRaw&r=0' alt="icone carregando.">
                                    <p class="texto">Confirmando identidando do agente. Por favor aguarde...</p>
                                </div>
                            """, unsafe_allow_html=True)

                            caminho_img1 = 'upload_temp/temp'
                            print(caminho_img1)
                            print(caminho_img2)

                            resultado = DeepFace.verify(
                                img1_path = caminho_img1,
                                img2_path = caminho_img2,
                            )                        
                            if resultado['verified']:
                                placeholder.empty()

                                # Lógica para inserir no banco de dados a confirmação de presença.
                                st.success(f"""
                                        ## PRESENÇA CONFIRMADA
                                        - {agente['graduacao']} {agente['nome']}
                                """)
                            else:
                                placeholder.empty()
                                st.error("""
                                    Erro: Identificação não confirmada. 

                                    A imagem fornecida não corresponde ao agente registrado. Por favor, verifique as seguintes informações:
                                    - Certifique-se de que a matrícula inserida está correta.
                                    - Garanta que a imagem capturada seja clara e bem iluminada.

                                    Caso o problema persista, entre em contato com o suporte técnico para assistência adicional.

                                """)
        else:
            st.error('Nenhum agente foi encontrado com a matrícula informada.')                




