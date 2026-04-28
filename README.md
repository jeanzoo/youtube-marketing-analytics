# 📊 YouTube Marketing Analytics: Pipeline ETL de Engajamento

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

## 📌 Contexto do Projeto (Business Case)
No mercado de marketing de influência, agências frequentemente perdem orçamento contratando criadores baseados apenas no número absoluto de inscritos (uma métrica de vaidade). O verdadeiro valor de conversão está no **engajamento ativo** da comunidade e na **velocidade de viralização** do conteúdo.

Este projeto é um pipeline de Engenharia de Dados (ETL) construído para resolver essa dor. Ele extrai dados diretamente da **YouTube Data API v3**, limpa, transforma e gera métricas de negócio para ajudar equipes de marketing a identificar os melhores influenciadores em nichos específicos no Brasil.

## ⚙️ Arquitetura do Pipeline

O fluxo de dados foi construído com foco em eficiência e redução de custo de requisições (Quota Optimization) da API.

<div align="center">
  <img src="arquitetura_etl.svg" alt="Diagrama da Arquitetura ETL" width="800">
</div>

## 🧠 Soluções de Engenharia Implementadas

1. **Filtragem na Origem (Pushdown Optimization):** Uso de `regionCode='BR'` e `relevanceLanguage='pt'` combinados com busca exata (Hard Filter) para evitar o tráfego de dados inúteis (ruído internacional e spam de tags).
2. **Programação Defensiva:** Implementação de `.get()` e blocos `try/except` para lidar com inconsistências no JSON da API (ex: vídeos que ocultam a contagem de *likes* não quebram o pipeline).
3. **Engenharia de Features:** Criação de métricas proprietárias através da manipulação de datas e estatísticas nativas:
   - **Taxa de Engajamento (%):** `(Likes + Comentários) / Visualizações`. Revela se a audiência interage ou apenas consome passivamente.
   - **Trend Velocity (Views/h):** Calcula a média de visualizações ganhas por hora desde a publicação. Identifica vídeos que estão viralizando *agora*.

## 🛠️ Tecnologias Utilizadas
* **Python ** (Lógica principal do pipeline)
* **Pandas** (Transformação de dados, formatação e ordenação)
* **Google API Client** (Comunicação com o Google Cloud)
* **Python-dotenv** (Governança e proteção de credenciais)

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório:
```bash
git clone [https://github.com/jeanzoo/youtube-marketing-analytics.git](https://github.com/jeanzoo/youtube-marketing-analytics.git)
cd youtube-marketing-analytics
