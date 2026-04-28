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
nicho_pesquisa = '"jogos" OR "gameplay" pt-br'
max_resultados = 30

print(f"Iniciando varredura no YouTube para o mercado de Gaming (Filtro: Top Brasil)...")

try:
    # ETAPA A: Buscar os IDs dos vídeos usando o Category ID nativo do YouTube
    request_busca = youtube.search().list(
        q=nicho_pesquisa,
        part='id',
        type='video',
        order='viewCount',     # Traz os gigantes primeiro
        maxResults=max_resultados,
        regionCode='BR',       # Filtro geográfico: Apenas Brasil
        relevanceLanguage='pt',# Filtro de idioma: Português
        videoCategoryId='20'   # <-- HARD FILTER: Categoria oficial de Gaming do YouTube
    )
    resultado_busca = request_busca.execute()

    # Extrai apenas a lista de IDs
    ids_videos = [item['id']['videoId'] for item in resultado_busca['items'] if 'videoId' in item['id']]

    if not ids_videos:
        print("Nenhum vídeo encontrado para este escopo no Brasil no momento.")
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
            data_pub_str = video['snippet']['publishedAt'] 
            
            # Converte a data do YouTube para calcular as horas no ar
            data_pub = datetime.fromisoformat(data_pub_str.replace('Z', '+00:00'))
            horas_no_ar = max((agora - data_pub).total_seconds() / 3600, 1) 
            
            # Puxando os dados usando programação defensiva
            stats = video.get('statistics', {})
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))

            # MÉTRICAS EXCLUSIVAS
            engajamento = ((likes + comments) / views * 100) if views > 0 else 0
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
            df_yt = df_yt.sort_values(by='Trend_Velocity_(Views/h)', ascending=False)
            df_yt.to_csv('relatorio_agencia_youtube.csv', index=False, encoding='utf-8')
            print(f"\n🚀 Sucesso! Analisados {len(df_yt)} vídeos da categoria Gaming no Brasil.")
        else:
            print("\n⚠️ Nenhum dado válido foi retornado da API.")

except Exception as e:
    print(f"\n❌ Erro durante o processo ETL: {e}")