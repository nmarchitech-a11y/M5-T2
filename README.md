# 🏗️ IFC Building Analyzer — Multi-Agentes com CrewAI

Sistema multi-agente que lê um modelo `.ifc` de edifício residencial, extrai quantitativos, áreas, materiais e elementos estruturais, e gera um relatório técnico `.docx` e um checklist de conformidade `.xlsx`.

## 📋 Visão Geral

| Item | Descrição |
|------|-----------|
| **Framework** | CrewAI (Agent → Task → Crew → Process.sequential) |
| **LLM** | Claude Sonnet 4.5 (Anthropic) |
| **IFC Library** | IfcOpenShell 0.8.x |
| **Schema** | IFC4 |
| **Outputs** | `.docx` relatório técnico + `.xlsx` checklist de conformidade |

### Arquitetura

```
.IFC → Agent 1 (Analista BIM) → Agent 2 (Relator Técnico) → Agent 3 (Revisor) → .docx + .xlsx
```

- **Agent 1 — Analista BIM/IFC:** Extrai sistematicamente todos os dados do modelo usando 4 tools (ler_modelo_ifc, extrair_quantitativos, extrair_espacos_areas, extrair_materiais)
- **Agent 2 — Relator Técnico AEC:** Sintetiza os dados em relatório `.docx` profissional e checklist `.xlsx` usando 2 tools (gerar_relatorio_docx, gerar_checklist_xlsx)
- **Agent 3 — Revisor de Conformidade:** Verifica dados contra o modelo original e emite parecer final

## 📁 Estrutura do Repositório

```
├── README.md                          ← Este arquivo
├── ifc_building_analyzer.ipynb        ← Notebook principal (executar este)
├── casa_residencial.ifc               ← Modelo IFC de entrada
├── create_sample_ifc.py               ← Script que gerou o .ifc
├── reflexao_critica.md                ← Reflexão crítica (300-500 palavras)
└── output/
    ├── relatorio_analise_ifc.docx     ← Relatório gerado pela crew
    └── checklist_ifc.xlsx             ← Checklist gerado pela crew
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- Anthropic API key ([obter aqui](https://console.anthropic.com/))

### 1. Clonar e instalar

```bash
git clone https://github.com/SEU_USUARIO/ifc-building-analyzer.git
cd ifc-building-analyzer

pip install crewai crewai-tools langchain-anthropic langchain
pip install python-docx openpyxl ifcopenshell
```

### 2. Configurar API Key

```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"
```

Ou via Google Colab Secrets (ícone 🔑 no painel esquerdo).

### 3. Executar o Notebook

```bash
jupyter notebook ifc_building_analyzer.ipynb
```

Execute todas as células sequencialmente. A crew irá:
1. Carregar `casa_residencial.ifc`
2. Agent 1 extrai todos os dados via IfcOpenShell
3. Agent 2 gera relatório `.docx` e checklist `.xlsx`
4. Agent 3 verifica conformidade e emite parecer

Tempo estimado: 3–8 minutos.

### 4. Verificar Outputs

Na pasta `output/`:
- `relatorio_analise_ifc_*.docx` — Relatório com resumo executivo, quantitativos, análise de espaços, materiais, estrutura e recomendações
- `checklist_ifc_*.xlsx` — Checklist com 20+ itens verificados (Conforme / Não Conforme / Parcial)

## 🔧 Tools Implementadas

| Tool (BaseTool) | Agente | Função |
|-----------------|--------|--------|
| `LerModeloIFCTool` | Analista + Revisor | Resumo hierárquico do modelo IFC |
| `ExtrairQuantitativosTool` | Analista + Revisor | Quantitativos detalhados de todos os elementos |
| `ExtrairEspacosTool` | Analista | Ambientes com áreas brutas/líquidas e volumes |
| `ExtrairMateriaisTool` | Analista | Materiais e seus usos por tipo de elemento |
| `GerarRelatorioDocxTool` | Relator | Gera relatório .docx formatado |
| `GerarChecklistXlsxTool` | Relator | Gera checklist .xlsx com cores por status |

## 📊 Modelo IFC — Casa Residencial

O `casa_residencial.ifc` é um edifício residencial de 2 pavimentos com:

| Elemento | Quantidade |
|----------|-----------|
| Paredes | 15 (externas + internas) |
| Portas | 9 (entrada + internas) |
| Janelas | 9 (vidro temperado 6mm) |
| Pilares | 12 (concreto C30, 30×30cm) |
| Vigas | 9 (concreto C30, 20×30cm) |
| Lajes | 3 (piso térreo, piso superior, cobertura) |
| Escada | 1 (17 espelhos, 16 pisos) |
| Ambientes | 11 (sala, cozinha, quartos, banheiros, etc.) |
| Materiais | 7 (concreto, tijolo, aço, vidro, madeira, cerâmica, lã mineral) |

## 📝 Dependências

```
crewai>=1.0.0
crewai-tools>=1.0.0
langchain-anthropic>=1.0.0
langchain>=1.0.0
python-docx>=1.0.0
openpyxl>=3.1.0
ifcopenshell>=0.8.0
```

## 👤 Autor

Natalia Manolio

## 📄 Licença

Projeto educacional para o Master Internacional em IA para Arquitetura e Construção (Zigurat).
