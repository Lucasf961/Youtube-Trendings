from functions import *
import streamlit as st; st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide')

#### SIDEBAR ####
st.sidebar.text('')

st.sidebar.markdown("**Primeiro ajuste os filtros de sua preferência:** 👇")

lista_paises = ['Brasil','Portugal','Estados Unidos','Reino Unido','Espanha','França']
option1 = st.sidebar.selectbox('Selecione o País de sua preferência:', lista_paises)

lista_categorias = ['Geral (Em Alta) 🌐','Música 🎶','Jogos 🎮','Esportes ⚽','Entretenimento 🎡','Notícias e Política 📰']
option2 = st.sidebar.selectbox('Selecione a categoria de sua preferência:', lista_categorias)

codigo_categoria = None

if option2 == 'Geral (Em Alta) 🌐':
    codigo_categoria = None
elif option2 == 'Música 🎶':
    codigo_categoria = 10
elif option2 == 'Jogos 🎮':
    codigo_categoria = 20
elif option2 == 'Esportes ⚽':
    codigo_categoria = 17
elif option2 == 'Entretenimento 🎡':
    codigo_categoria = 24
else:
    codigo_categoria = 25


codigo_regiao = None

if option1 == 'Brasil':
    codigo_regiao = 'br'
elif option1 == 'Portugal':
    codigo_regiao = 'pt'
elif option1 == 'Estados Unidos':
    codigo_regiao = 'us'
elif option1 == 'Reino Unido':
    codigo_regiao = 'gb'
elif option1 == 'Espanha':
    codigo_regiao = 'es'
else:
    codigo_regiao = 'fr'

yt_geral = request_api(id_category = codigo_categoria, region_code = codigo_regiao)
tabela_tags, wordcloud = ranktags_and_wordcloud_generator(yt_geral['Tags'])

### INTRODUCTION ###
title = '<span style="color:#DE0F0F; font-size: 45px;"><b>YouTube</b></span><span style="color:#252121; font-size: 45px;"><b>Trending</b></span>'
st.markdown(title, unsafe_allow_html=True)

st.markdown("Streamlit App atualizado em tempo real com os [50 vídeos em Alta do Youtube](https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl), utilizando a [API](https://developers.google.com/youtube/v3) disponibilizada pelo Google.")
st.markdown("Repositório do código disponível no [Github](https://github.com/Lucasf961/Youtube).")

st.text('')
subt = '<span style="color:#252121; font-size: 20px;">Quais assuntos</span> <span style="color:#DE0F0F; font-size: 20px;"><b>em Alta</b></span> <span style="color:#252121; font-size: 20px;"> agora? 📈</span>'
st.markdown(subt, unsafe_allow_html=True)

#### WORDCLOUD/TABELA ####
col1, col2_space, col3 = st.columns([4.5,0.5,2.9])
with col1:
    fig = plt.figure()
    fig.set_facecolor('xkcd:white')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt.show())
with col3:
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    see_data = st.expander('Clique aqui para ver em forma de tabela 👉')

    with see_data:
        st.table(tabela_tags)

#### TABELA VIDEOS EM ALTA ####
st.text('')
st.text('')
subtitle2 = '<span style="color:#252121; font-size: 20px;">Vídeos</span> <span style="color:#DE0F0F; font-size: 20px;"><b>em Alta</b></span> <span style="color:#252121; font-size: 20px;">no Momento 🎥</span> '
st.markdown(subtitle2, unsafe_allow_html=True)

row_1, row_space, row_2, row_space2 = st.columns((1,.1, 1, 1))
with row_1:
    orderby = st.selectbox("Ordenar Tabela por:", ["Ranking do Youtube","Número de Views","Número de Likes","Views a cada Like"])

with row_2:
    orderby2 = st.selectbox("Ordenar a partir do:", ["Melhor para o Pior", "Pior para o Melhor"])

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)

tb = plot_table(yt_geral)

if (orderby == "Ranking do Youtube") & (orderby2 == "Pior para o Melhor"):
    tb.sort_index(ascending = False, inplace = True)

if (orderby == "Número de Views") & (orderby2 == "Pior para o Melhor"):
    tb.sort_values(by = 'Número de Views', inplace = True)
elif (orderby == "Número de Views") & (orderby2 == "Melhor para o Pior"):
    tb.sort_values(by = 'Número de Views', ascending = False, inplace = True)

if (orderby == "Número de Likes") & (orderby2 == "Pior para o Melhor"):
    tb.sort_values(by = "Número de Likes", inplace = True)
elif (orderby == "Número de Likes") & (orderby2 == "Melhor para o Pior"):
    tb.sort_values(by = "Número de Likes", ascending = False, inplace = True)

if (orderby == "Views a cada Like") & (orderby2 == "Pior para o Melhor"):
    tb.sort_values(by = "Views a cada Like", ascending = False, inplace = True)
    st.warning('Nesse caso, quanto menor o número de views a cada like, menos views o vídeo precisa, em média, para conseguir um like. Resumindo, quanto menor, melhor.')
elif (orderby == "Views a cada Like") & (orderby2 == "Melhor para o Pior"):
    tb.sort_values(by = "Views a cada Like", inplace = True)
    st.warning('Nesse caso, quanto menor o número de views a cada like, menos views o vídeo precisa, em média, para conseguir um like. Resumindo, quanto menor, melhor.')

st.table(tb.head(10))

#### CANAIS ####
st.text('')
st.text('')
subtitle3 = '<p style="color:#252121; font-size: 20px;">Algum Canal se Destaca? 📺</p>'
st.markdown(subtitle3, unsafe_allow_html=True)

col1, col2_space, col3 = st.columns([2,0.5,1])
with col1:
    plot_canais, canais_table = plot_canais_destaque(yt_geral)
    if len(canais_table) < 1:
        st.warning('Nenhum Canal aparece mais de uma vez no "Em Alta" na categoria e país selecionados!')
    else:
        st.plotly_chart(plot_canais)
with col3:
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    see_data2 = st.expander('Clique aqui para ver em forma de tabela 👉')

    with see_data2:
        st.table(canais_table)