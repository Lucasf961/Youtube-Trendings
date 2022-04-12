##### REQUEST NA API DO YOUTUBE / RETORNA UM DATAFRAME #####

def request_api(id_category = None):
    from googleapiclient.discovery import build
    from datetime import date
    from pandas import DataFrame
    import numpy as np
    import json

    with open('key.json', 'r') as file:
        data = file.read()

    dictionary = json.loads(data)
    value = list(dictionary.values())

    key = value
    service_name = 'youtube'
    api_version = 'v3'

    youtube = build(serviceName = service_name, version = api_version, developerKey = key)
    request = youtube.videos().list(part = ['snippet','statistics'], videoCategoryId = id_category, maxResults=50, chart = 'mostPopular', regionCode = 'br')
    response = request.execute()

    id_video = []
    data_publicacao = []
    titulo = []
    n_views = []
    n_likes = []
    n_comments = []
    id_canal = []
    thumbnail_image = []
    nome_canal = []
    id_categoria = []
    tags = []

    for i in range(0, len(response['items'])):
        id_video.append(response['items'][i]['id'])
        data_publicacao.append(response['items'][i]['snippet']['publishedAt'])
        titulo.append(response['items'][i]['snippet']['title'])
        id_canal.append(response['items'][i]['snippet']['channelId'])
        thumbnail_image.append(response['items'][i]['snippet']['thumbnails']['default']['url'])
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
            n_comments.append(response['items'][i]['statistics']['commentCount'])
        except:
            n_comments.append(np.nan)
        
        try:
            id_categoria.append(response['items'][i]['snippet']['categoryId'])
        except:
            id_categoria.append(np.nan)
            
    ranking = []
    for i in list(range(1,len(id_video) + 1)):
        ranking.append("#"+str(i))
    
    data = {'ranking': ranking,
            'id_video':id_video,
            'data_publicacao':data_publicacao,
            'titulo':titulo,
            'id_canal':id_canal,
            'n_views':n_views,
            'n_likes':n_likes,
            'n_comments':n_comments,
            'thumbnail':thumbnail_image, 
            'nome_canal':nome_canal, 
            'id_categoria':id_categoria, 
            'tags':tags}
    
    api = DataFrame(data = data)
    return api

##### FUNÇÃO QUE GERA UM DATA FRAME COM O RANKING DE TAGS NOS VÍDEOS #####

def ranking_tags(dftags):
    import pandas as pd
    import numpy as np
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    import nltk
    nltk.download('stopwords')

    _stopwords = []
    for word in stopwords.words(['portuguese','english']):
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
    
    # DataFrame
    df_final = pd.DataFrame(ranking.items(), columns = ['tags', 'contagem'])
    
    return df_final.sort_values(by = 'contagem', ascending = False).reset_index(drop = True)

##### FUNÇÃO QUE GERA NUVEM DE PALAVRAS #####

def word_cloud_tags(dftags):
    import numpy as np
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    import nltk
    nltk.download('stopwords')
    
    _stopwords = []
    for word in stopwords.words(['portuguese','english']):
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

    wc = ' '.join(keywords)
    wordcloud = WordCloud(collocations=False, background_color='black').generate(wc)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

##### FUNÇÃO QUE PLOTA O GRÁFICO DE BARRAS #####

def bar_plot_categorias(df):
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    
    cat = df.groupby('category_name').size().sort_values(ascending = False).reset_index().rename(columns = {0:'count'})

    rc = {'figure.figsize':(10,6),
            'axes.facecolor':'#0e1117',
            'axes.edgecolor': '#0e1117',
            'axes.labelcolor': 'white',
            'figure.facecolor': '#0e1117',
            'patch.edgecolor': '#0e1117',
            'text.color': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'grid.color': 'grey',
            'font.size' : 12,
            'axes.labelsize': 12,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()

    ax = sns.barplot(y='category_name', x='count', data=cat, color = "#D90F0F")

    ax.set(xlabel = 'Contagem', ylabel = 'Categoria')

    plt.show()





