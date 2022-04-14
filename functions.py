##### REQUEST NA API DO YOUTUBE / RETORNA UM DATAFRAME #####
def request_api(id_category = None, region_code = 'br'):
    from googleapiclient.discovery import build
    from pandas import DataFrame
    import numpy as np
    import streamlit as st

    key = st.secrets.api_key.api
    service_name = 'youtube'
    api_version = 'v3'

    youtube = build(serviceName = service_name, version = api_version, developerKey = key)
    request = youtube.videos().list(part = ['snippet','statistics'], videoCategoryId = id_category, maxResults=50, chart = 'mostPopular', regionCode = region_code)
    response = request.execute()
    
    titulo = []
    n_views = []
    n_likes = []
    nome_canal = []
    id_categoria = []
    tags = []

    for i in range(0, len(response['items'])):
        titulo.append(response['items'][i]['snippet']['title'])
        nome_canal.append(response['items'][i]['snippet']['channelTitle'])
        
        try:
            tags.append(response['items'][i]['snippet']['tags'])
        except:
            tags.append(np.nan)
            
        try:
            n_views.append(response['items'][i]['statistics']['viewCount'])
        except:
            n_views.append(np.nan)
            
        try:
            n_likes.append(response['items'][i]['statistics']['likeCount'])
        except:
            n_likes.append(np.nan)
        
        try:
            id_categoria.append(response['items'][i]['snippet']['categoryId'])
        except:
            id_categoria.append(np.nan)
            
    ranking = []
    for i in list(range(1,len(titulo) + 1)):
        ranking.append("#"+str(i))
    
    data = {'Ranking do Em Alta do Youtube': ranking,
            'Título do Vídeo':titulo,
            'Nome do Canal':nome_canal,
            'ID da Categoria':id_categoria,
            'Número de Views':n_views,
            'Número de Likes':n_likes,
            'Tags':tags}
    
    api = DataFrame(data = data)
    return api

##### RETORNA DATAFRAME E WORDCLOUD COM O RANKING DE TAGS #####
def ranktags_and_wordcloud_generator(dftags):
    import pandas as pd
    import numpy as np
    from wordcloud import WordCloud
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    
    _stopwords = []
    for word in stopwords.words(['portuguese','english','spanish','french']):
        _stopwords.append(word)
    
    # 1 - Desconsiderando valores NAN
    not_nan = [i for i in dftags if i is not np.nan]

    # 2 - Transformando listas em strings
    string = [str(i) for i in not_nan]
    
    # 3 - Convertendo letras maiusculas para minusculas
    lower = [i.lower() for i in string]
    
    # 4 - Split por vírgula. Ex: "Flamengo, Vasco, Botafogo" > "Flamengo", "Vasco", "Botafogo"
    split = [i.split(',') for i in lower]
    
    # 5 - Filtrando apenas strings com letras(a-z)
    tokenizer = RegexpTokenizer(r'\w+')
    token = []
    for i in split:
        for x in i:
            token.append(tokenizer.tokenize(x))
        
    # 6 - Juntando palavras compostas em uma string. Ex: "Campeonato Brasileiro" > "Campeonato_Brasileiro"
    join = ['_'.join(i) for i in token]

    # 7 - Filtrando palavras que não aparecem nas Stopwords
    keywords = []
    for lista in join:
        if lista not in _stopwords:
            keywords.append(lista)
            
    # 8 - Ranking
    ranking=dict(zip(list(keywords),[list(keywords).count(i) for i in list(keywords)]))
    
    # 9 - DataFrame
    df_final = pd.DataFrame(ranking.items(), columns = ['Tags', 'Contagem'])
    rank = df_final.sort_values(by = 'Contagem', ascending = False).reset_index(drop = True)
    tops = rank[rank['Contagem'] >= 3]
    
    # 10 - wordcloud
    words = [word for word in keywords if word in tops['Tags'].tolist()]
    wc = ' '.join(words)
    wordcloud = WordCloud(collocations=False, height= 325, mode = "RGBA", background_color=None, colormap='inferno').generate(wc)
    
    return tops, wordcloud

##### RETORNA A TABELA #####
def plot_table(df):
    videos = df[['Ranking do Em Alta do Youtube','Título do Vídeo','Nome do Canal','Número de Views','Número de Likes']]
    
    videos.fillna(0, inplace = True)
    
    videos['Número de Views'] = videos['Número de Views'].astype('int')
    videos['Número de Likes'] = videos['Número de Likes'].astype('int')
    
    videos['Views a cada Like'] = round(videos['Número de Views'] / videos['Número de Likes'] , 2)
    
    return videos

##### FUNÇÃO QUE PLOTA O GRÁFICO DE BARRAS #####
def plot_canais_destaque(df):
    import plotly.express as px
    canais = df.groupby('Nome do Canal').size().sort_values(ascending = False).reset_index().rename(columns = {0:'Contagem de Aparições'})
    
    top_canais = canais[canais['Contagem de Aparições'] > 1]

    fig = px.bar(top_canais, x='Nome do Canal', y='Contagem de Aparições',
                 text_auto='.0s',
                 labels=dict(nome_canal="Nome do Canal", count='Contagem de aparições'))

    fig.update_traces(marker_color = '#CD1414', textfont_size=20, textangle=0, textposition="inside")

    fig.update_layout(plot_bgcolor='white',
                      yaxis = dict(visible = False), 
                      xaxis =  dict(tickfont_size=14,
                                    tickfont_family='Open Sans'))
    
    return fig, top_canais


