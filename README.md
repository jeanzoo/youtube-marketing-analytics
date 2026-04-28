# 📊 YouTube Analytics: Pipeline ETL para Inteligência de Mercado

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

## 📌 Contexto do Projeto (O Problema de Negócio)
No mercado de influência, empresas frequentemente perdem orçamento contratando criadores baseados apenas no número absoluto de inscritos (uma métrica de vaidade). O verdadeiro valor de conversão está no **engajamento ativo** da comunidade e na **velocidade de viralização** do conteúdo.

Este projeto é um pipeline de Engenharia de Dados (ETL) construído para resolver essa dor. Ele extrai dados diretamente da **YouTube Data API v3**, limpa, transforma e gera métricas de negócio (KPIs) para ajudar analistas a mapearem os influenciadores de maior impacto e retenção no gigantesco mercado de Gaming (Videogames) no Brasil.

---

## 🧠 Como a Solução Foi Arquitetada (Decisões de Engenharia)

Antes de escrever o código, estruturei o pipeline para responder a três desafios clássicos de Engenharia de Dados:

1. **Como extrair apenas os dados relevantes sem estourar a cota da API?**
2. **Como garantir *Data Quality* e transformar JSONs complexos em métricas de negócio?**
3. **Como garantir que o pipeline seja escalável para qualquer outro nicho?**

Abaixo, as decisões arquiteturais tomadas para cada etapa:

### 1️⃣ Extração Inteligente (Pushdown Optimization)
Em vez de usar a força bruta para baixar toda a base e filtrar no Pandas (desperdiçando tempo de processamento e cota da API), forcei o servidor do Google a me entregar apenas dados qualificados aplicando filtros rígidos na requisição (*Hard Filters*):
- **Localização e idioma:** Parâmetros `BR` e `pt` para isolar o ecossistema brasileiro.
- **Categoria Oficial:** Uso do `videoCategoryId='20'` (Gaming) para anular ruídos e falsos-positivos na busca.
- **Ordenação Lógica:** Requisição baseada em `viewCount`, garantindo que o pipeline processe apenas dados com relevância estatística.

> 💡 **Decisão de Arquitetura:** Aplicar filtros na origem (API) é infinitamente mais barato e eficiente do que limpar sujeira no destino.

### 2️⃣ Transformação e Regras de Negócio
Dados crus da API (likes, comments, views) têm baixo valor analítico. A camada de transformação (construída em Pandas) aplica programação defensiva contra inconsistências da API (como vídeos com likes ocultos) e cria novas *features*:
- **Taxa de Engajamento (%):** Relação entre interações e visualizações totais.
- **Trend Velocity (Views/h):** Normalização do crescimento baseado na idade do vídeo (visualizações divididas por horas no ar).

> 💡 **Decisão de Arquitetura:** O pipeline não deve apenas mover dados (Copy/Paste), ele deve enriquecê-los e entregar valor agregado para a tomada de decisão.

### 3️⃣ Carga e Entrega (Data Delivery)
A saída do pipeline é um artefato estruturado (`.csv`), perfeitamente limpo, tipado e ordenado pela métrica de aceleração.

> 💡 **Decisão de Arquitetura:** O output do dado deve estar pronto para consumo downstream imediato (seja para ingestão em um Data Warehouse, SQL ou consumo direto no Power BI).

### 4️⃣ Escalabilidade e Parametrização
O pipeline foi projetado de forma agnóstica. Ele não é um "script de videogame", é um motor de extração. Para plugar a análise em um novo mercado (ex: Finanças, Moda, Educação), o analista precisa alterar apenas três variáveis de ambiente: *Palavra-chave, ID da Categoria e Região*.

---

## ⚙️ Arquitetura do Pipeline

<div align="center">
  <img src="arquitetura_etl.svg" alt="Diagrama da Arquitetura ETL" width="800">
</div>

---

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório:
```bash
git clone [https://github.com/jeanzoo/youtube-marketing-analytics.git](https://github.com/jeanzoo/youtube-marketing-analytics.git)
cd youtube-marketing-analytics