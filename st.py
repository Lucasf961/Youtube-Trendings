from functions import *
import streamlit as st; st.set_option('deprecation.showPyplotGlobalUse', False)
import pandas as pd

yt_geral = request_api()
categories = pd.read_csv('catdata.csv')

st.set_page_config(layout = 'wide')

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Youtube Trending')
# with row0_2:
#     st.text("")
#     st.subheader('Streamlit App by [Tim Denzler](https://www.linkedin.com/in/tim-denzler/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Quais assuntos em alta no momento?")

st.sidebar.text('')
st.sidebar.text('')

st.sidebar.markdown("**Primeiro ajuste os filtros de sua preferência:** 👇")

lista_categorias = list(categories['category_name'])
lista_categorias.append('- Geral (Em Alta)')
lista_categorias.sort()
option = st.sidebar.selectbox('Selecione a categoria abaixo:', lista_categorias, index = 0)

wc = word_cloud_tags(yt_geral['tags'])

st.pyplot(fig = wc, clear_figure = True)