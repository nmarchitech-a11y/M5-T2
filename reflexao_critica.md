# Reflexão Crítica — IFC Building Analyzer com CrewAI

## Decisões de Design

Este projeto implementa uma **arquitetura sequencial de três agentes** usando CrewAI para análise de modelos IFC de edificações residenciais. A escolha do CrewAI foi motivada pela sua abstração de alto nível — definir agentes com `role`, `goal` e `backstory` é mais intuitivo que construir grafos de estado manualmente com LangGraph, e o `Process.sequential` garante que cada agente recebe o output dos anteriores como contexto. Esta abordagem reflete a cadeia de trabalho real em projetos AEC: um analista extrai dados, um documentador produz relatórios, e um revisor valida o resultado.

O design das tools segue **decomposição funcional por domínio**: em vez de uma única tool monolítica de leitura IFC, criamos 6 tools especializadas usando `BaseTool` do CrewAI — 4 de leitura/extração (`ler_modelo_ifc`, `extrair_quantitativos`, `extrair_espacos_areas`, `extrair_materiais`) e 2 de geração de output (`gerar_relatorio_docx`, `gerar_checklist_xlsx`). Esta separação espelha o workflow real de profissionais BIM e permite que cada agente use apenas as ferramentas relevantes ao seu papel. A decisão de gerar tanto `.docx` quanto `.xlsx` reflete a prática profissional: relatórios narrativos para comunicação com stakeholders e checklists tabulados para rastreabilidade de conformidade.

O `backstory` de cada agente foi calibrado para o contexto AEC brasileiro, incluindo referências a normas ABNT e práticas de mercado. Isso orienta o raciocínio do LLM para produzir observações técnicas relevantes em vez de análises genéricas.

## Limitações Técnicas

**1. Ausência de Raciocínio Geométrico/Espacial:** O sistema extrai propriedades textuais e numéricas (nomes, quantitativos, materiais) mas não realiza análise geométrica. Não detecta conflitos espaciais (ex: viga interceptando tubulação), não verifica distâncias livres de circulação, nem valida arcos de abertura de portas. O kernel geométrico do IfcOpenShell (OpenCASCADE) requer operações explícitas de tessellação e interseção de sólidos — computacionalmente caras e não encapsuladas nas tools atuais. Exemplo concreto: o sistema não consegue verificar se o corrimão da escada (`IfcRailing`) colide fisicamente com a parede interna adjacente, mesmo tendo ambos os elementos no modelo.

**2. Dependência de PropertySets Padrão IFC4:** O sistema assume arquivos IFC com property sets padrão (`Pset_WallCommon`, `Qto_WallBaseQuantities`). Exportações reais do Revit frequentemente colocam dimensões em property sets customizados como `Revit_Type_Parameters` em vez do padrão `Qto_WallBaseQuantities`. O sistema retornaria dados incompletos silenciosamente para tais arquivos — sem alertar o utilizador. Um mecanismo de fallback que busca propriedades em todos os psets disponíveis mitigaria este problema.

**3. Risco de Alucinação na Análise do LLM:** Embora os dados de entrada sejam determinísticos (IfcOpenShell), o Agente Relator pode gerar observações imprecisas sobre normas técnicas ou custos que o LLM não domina. O Agente Revisor mitiga parcialmente este risco ao re-verificar dados contra o modelo original, mas não inclui validação automatizada cruzando cada afirmação do relatório contra os valores brutos extraídos.

## Extensões Possíveis

- **Detecção de Interferências:** Adicionar agente usando `ifcopenshell.geom` para tesselar elementos e detectar colisões entre sistemas estruturais e MEP.
- **Verificação NBR 9050:** Agente que verifica automaticamente larguras de portas ≥ 0.80m, corredores ≥ 1.20m e presença de rampas — o modelo atual já identifica portas de 0.70m como não-conformidade.
- **Comparação de Versões:** Pipeline que aceita dois `.ifc` e gera relatório de diferenças por `GlobalId`, identificando elementos adicionados, removidos ou modificados entre revisões de projeto.
- **Modo Q&A Interativo:** Substituir o pipeline sequencial por uma crew conversacional que permite perguntas de acompanhamento sobre o modelo.
