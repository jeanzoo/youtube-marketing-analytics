import os
from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone

# 1. Configuração e Segurança
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Inicializa o motor do YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 2. A Demanda de Negócio da Agência
nicho_pesquisa = "Jogos Indie"
max_resultados = 30 

print(f"Iniciando varredura no YouTube para o nicho: '{nicho_pesquisa}' (Filtro: Brasil)...")

try:
    # ETAPA A: Buscar os IDs dos vídeos mais recentes sobre o tema NO BRASIL
    request_busca = youtube.search().list(
        q=nicho_pesquisa,
        part='id',
        type='video',
        order='date', # Filtra pelos envios mais recentes
        maxResults=max_resultados,
        regionCode='BR',       # Filtro geográfico: Apenas Brasil
        relevanceLanguage='pt' # Filtro de idioma: Português
    )
    resultado_busca = request_busca.execute()

    # Extrai apenas a lista de IDs
    ids_videos = [item['id']['videoId'] for item in resultado_busca['items'] if 'videoId' in item['id']]

    if not ids_videos:
        print(" Nenhum vídeo encontrado para este nicho no Brasil no momento.")
    else:
        # ETAPA B: Puxar a "Capivara" completa com as estatísticas desses vídeos
        request_stats = youtube.videos().list(
            part='statistics,snippet',
            id=','.join(ids_videos)
        )
        resultado_stats = request_stats.execute()

        # 3. Transformação (Criação de Métricas de Negócio)
        dados_extraidos = []
        agora = datetime.now(timezone.utc)

        for video in resultado_stats['items']:
            titulo = video['snippet']['title']
            canal = video['snippet']['channelTitle']
            data_pub_str = video['snippet']['publishedAt'] # Ex: 2026-04-27T10:00:00Z
            
            # Converte a data do YouTube para calcular as horas no ar
            data_pub = datetime.fromisoformat(data_pub_str.replace('Z', '+00:00'))
            horas_no_ar = max((agora - data_pub).total_seconds() / 3600, 1) # Mínimo 1 hora para evitar erro de divisão
            
            # Puxando os dados usando programação defensiva
            stats = video.get('statistics', {})
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))

            # MÉTRICAS EXCLUSIVAS (O que o recrutador quer ver)
            # Taxa de Engajamento: (Likes + Comentários) / Views
            engajamento = ((likes + comments) / views * 100) if views > 0 else 0
            
            # Trend Velocity: Quantas views por hora esse vídeo está ganhando?
            velocidade = views / horas_no_ar

            dados_extraidos.append({
                'Canal': canal,
                'Título': titulo,
                'Visualizações': views,
                'Taxa_Engajamento_%': round(engajamento, 2),
                'Trend_Velocity_(Views/h)': round(velocidade, 2)
            })
            
        # 4. Carga (Load) para o arquivo final
        df_yt = pd.DataFrame(dados_extraidos)

        if not df_yt.empty:
            # Ordena a tabela pela velocidade da trend (o que está mais "quente" agora)
            df_yt = df_yt.sort_values(by='Trend_Velocity_(Views/h)', ascending=False)
            df_yt.to_csv('relatorio_agencia_youtube.csv', index=False, encoding='utf-8')
            print(f"\n🚀 Sucesso! Analisados {len(df_yt)} vídeos focados no Brasil.")
            print("Arquivo 'relatorio_agencia_youtube.csv' gerado na pasta do projeto.")
        else:
            print("\n Nenhum dado válido foi retornado da API.")

except Exception as e:
    print(f"\n Erro durante o processo ETL: {e}")