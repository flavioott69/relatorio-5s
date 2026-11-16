import streamlit as st
import google.generativeai as genai
from datetime import date

# Configuração da Página
st.set_page_config(
    page_title="Programa 5S TM engenharia",
    page_icon="📋",
    layout="wide"
)

# Estilo visual (Paleta Verde Claro / Industrial TM Engenharia)
st.markdown("""
<style>
    .faixa-verde {
        background-color: #065F46;
        color: #FFFFFF;
        padding: 16px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .senso-header {
        background-color: #E8F5E9;
        color: #065F46;
        padding: 12px;
        border-left: 5px solid #10B981;
        border-radius: 4px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .rodape-tm {
        margin-top: 40px;
        padding: 12px;
        background-color: #F1F5F9;
        color: #065F46;
        text-align: center;
        font-weight: bold;
        border-top: 2px solid #10B981;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Faixa Verde Superior
st.markdown('<div class="faixa-verde">TM Engenharia e serviços • Programa 5S</div>', unsafe_allow_html=True)

# Chave API
with st.expander("🔑 Configuração da API (Google AI Studio)", expanded=True):
    api_key = st.text_input("Cole sua Chave da API do Google AI Studio:", type="password")

# Cabeçalho da Vistoria (Sem Auditor, Sem Hora, Sem Código)
st.subheader("1. Dados da Vistoria")
col1, col2, col3 = st.columns(3)
with col1:
    empresa = st.text_input("Empresa / Cliente:")
with col2:
    setor = st.text_input("Setor / Área / Unidade:")
with col3:
    data_vistoria = st.date_input("Data da Vistoria:", value=date.today())

obs_gerais = st.text_area("Observações Gerais da Vistoria (Opcional):", height=70)

st.divider()

# Estrutura Oficial dos 5 Sensos e 29 Perguntas
sensos_dados = [
    {
        "titulo": "1ºS. Senso de UTILIZAÇÃO",
        "definicao": "Distinguir o necessário e descartar o desnecessário evitando excessos, desperdícios e má utilização.",
        "itens": [
            ("ITEM 1.1", "A área guarda somente objetos, peças e materiais necessários para a execução do trabalho?"),
            ("ITEM 1.2", "Existem materiais em excesso ou que já não tem mais uso?"),
            ("ITEM 1.3", "Foram encontrados materiais danificados?"),
            ("ITEM 1.4", "Existem vazamentos de água, ar, óleo ou alguma outra fonte de desperdício?")
        ]
    },
    {
        "titulo": "2ºS. Senso de ORGANIZAÇÃO",
        "definicao": "Agrupar, identificar os recursos e instalações, facilitando o acesso, utilização e prevenção de acidentes.",
        "itens": [
            ("ITEM 2.1", "Existem materiais espalhados na superfície de mesas, bancadas, no chão, corredores, etc.?"),
            ("ITEM 2.2", "Os materiais dentro de gavetas, armários, bancadas, estão em locais próprios e de fácil localização? Estes materiais estão organizados?"),
            ("ITEM 2.3", "Os materiais estão estocados livres de deterioração, umidade, quedas ou outros danos?"),
            ("ITEM 2.4", "Foi encontrado algum material impedindo vias de acesso ou o acesso aos equipamentos de emergência?"),
            ("ITEM 2.5", "Os extintores de combate a princípio de incêndio estão com o prazo de validade adequado? Foram inspecionados?")
        ]
    },
    {
        "titulo": "3ºS. Senso de LIMPEZA",
        "definicao": "Efetuar a limpeza e detectar problemas, visando eliminar ou minimizar as fontes de sujeira.",
        "itens": [
            ("ITEM 3.1", "Os pisos, paredes e teto estão limpos e isentos de dejetos, lixo, água ou outros líquidos?"),
            ("ITEM 3.2", "Os equipamentos, tubulações, armários, prateleiras, ferramentas, etc. estão limpos?"),
            ("ITEM 3.3", "As placas, faixas no piso e outras sinalizações estão limpas e em bom estado de conservação?"),
            ("ITEM 3.4", "Existem fontes geradora de sujeira? Existe risco de contaminação do produto ou dano a equipamentos?"),
            ("ITEM 3.5", "Os recipientes para coleta seletiva são bem distribuídos e conservados?"),
            ("ITEM 3.6", "Os banheiros e vestiários estão limpos?"),
            ("ITEM 3.7", "Recentemente o crescimento de mato alto em torno do ambiente de trabalho pode estar oferecendo algum risco à segurança ou impedindo a eficiência do trabalho?")
        ]
    },
    {
        "titulo": "4ºS. Senso de PADRONIZAÇÃO",
        "definicao": "Estabelecer procedimentos e ferramentas para manter os 3 primeiros sensos.",
        "itens": [
            ("ITEM 4.1", "Existe algum aspecto que possa estar oferecendo risco à segurança dos funcionários?"),
            ("ITEM 4.2", "A identificação dos quadros elétricos e tomadas sobre os riscos, estão de forma clara e objetiva?"),
            ("ITEM 4.3", "Os armários, gavetas, áreas de estocagem, etc., estão marcados com etiquetas ou sinalizações?"),
            ("ITEM 4.4", "As identificações de armários, gavetas, prateleiras descrevem claramente seu conteúdo?"),
            ("ITEM 4.5", "Os funcionários estão utilizando o EPI corretamente? Estão praticando comportamento inseguro?"),
            ("ITEM 4.6", "A área atende o pré requisito da NR 31 (Refeitório, barreira, banheiros e lavatórios de mão)?"),
            ("ITEM 4.7", "O local possui todas as placas de sinalização necessárias?")
        ]
    },
    {
        "titulo": "5ºS. Senso de DISCIPLINA",
        "definicao": "Ter e manter a habilidade de fazer a coisa certa naturalmente (autodisciplina).",
        "itens": [
            ("ITEM 5.1", "As tarefas relacionadas ao 5S são executadas regularmente? O senso de disciplina é mantido por todos?"),
            ("ITEM 5.2", "As pessoas tem conhecimento do resultado do 5S da área? Elas são envolvidas nos planos de ação?"),
            ("ITEM 5.3", "As ações da última auditoria 5S foram implementadas? Existem ações em atraso?"),
            ("ITEM 5.4", "As não conformidades se repetem?"),
            ("ITEM 5.5", "O descarte de materiais na coleta seletiva é realizado corretamente?"),
            ("ITEM 5.6", "Situações que demonstram desperdício de energia elétrica (Na ausência de pessoas nas salas/escritórios as lâmpadas, computadores e ar condicionado estão desligadas)?")
        ]
    }
]

st.subheader("2. Checklist Operacional dos 5 Sensos")

respostas = []
total_aplicaveis = 0
total_conformes = 0

# Renderização das abas dos 5 Sensos
abas = st.tabs(["1ºS Utilização", "2ºS Organização", "3ºS Limpeza", "4ºS Padronização", "5ºS Disciplina"])

for idx_senso, senso in enumerate(sensos_dados):
    with abas[idx_senso]:
        st.markdown(f"""
        <div class="senso-header">
            <strong>{senso['titulo']}</strong><br>
            <em>{senso['definicao']}</em>
        </div>
        """, unsafe_allow_html=True)

        for codigo, pergunta in senso["itens"]:
            with st.container(border=True):
                st.markdown(f"**{codigo}** — {pergunta}")
                status = st.radio(
                    f"Avaliação {codigo}",
                    ["C - Conforme", "NC - Não Conforme", "NA - Não se Aplica"],
                    horizontal=True,
                    key=f"status_{codigo}",
                    label_visibility="collapsed"
                )

                if status == "C - Conforme":
                    total_aplicaveis += 1
                    total_conformes += 1
                elif status == "NC - Não Conforme":
                    total_aplicaveis += 1
                    st.error("🚨 Não Conformidade Identificada — Preencha o Plano de Ação:")
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        descricao_fato = st.text_input("Descrição do Fato / Desvio:", key=f"fato_{codigo}")
                        acao_corretiva = st.text_input("Ação Corretiva Proposta:", key=f"acao_{codigo}")
                    with c2:
                        responsavel = st.text_input("Responsável pela Execução:", key=f"resp_{codigo}")
                        prioridade = st.selectbox("Prioridade:", ["Alta", "Média", "Baixa"], key=f"prio_{codigo}")

                    fotos = st.file_uploader(
                        f"Evidências Fotográficas ({codigo})",
                        type=["jpg", "jpeg", "png"],
                        accept_multiple_files=True,
                        key=f"foto_{codigo}"
                    )

                    respostas.append({
                        "senso": senso["titulo"],
                        "codigo": codigo,
                        "pergunta": pergunta,
                        "fato": descricao_fato,
                        "acao": acao_corretiva,
                        "responsavel": responsavel,
                        "prioridade": prioridade,
                        "fotos": fotos
                    })

# Cálculo de Desempenho
st.divider()
nota_geral = round((total_conformes / total_aplicaveis) * 100, 1) if total_aplicaveis > 0 else 100.0

if nota_geral >= 90:
    classificacao = "Excelente Desempenho"
elif nota_geral >= 75:
    classificacao = "Bom Desempenho"
elif nota_geral >= 60:
    classificacao = "Atenção Necessária"
else:
    classificacao = "Nível Crítico / Reprovado"

st.subheader("3. Resumo Executivo & Emissão de Relatório")
m1, m2, m3 = st.columns(3)
m1.metric("Índice Geral 5S", f"{nota_geral}%")
m2.metric("Classificação", classificacao)
m3.metric("Não Conformidades (NC)", len(respostas))

if st.button("📄 Gerar Relatório Técnico Completo", type="primary", use_container_width=True):
    if not empresa or not setor:
        st.warning("Por favor, preencha a Empresa/Cliente e o Setor/Unidade no topo da página.")
    else:
        st.markdown("---")
        st.markdown('<div class="faixa-verde">TM Engenharia e serviços • Relatório de Auditoria 5S</div>', unsafe_allow_html=True)

        st.markdown(f"""
        **Empresa / Cliente:** {empresa}  
        **Setor / Unidade:** {setor}  
        **Data da Vistoria:** {data_vistoria.strftime('%d/%m/%Y')}  
        **Índice Geral 5S:** **{nota_geral}%** ({classificacao})  
        **Observações Gerais:** {obs_gerais if obs_gerais else 'Nenhuma observação adicional registrada.'}
        """)

        # Resumo gerado pela IA se a chave API for informada
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                texto_ncs = "\n".join([f"- {r['codigo']} ({r['senso']}): Fato: {r['fato']} | Ação: {r['acao']} | Resp: {r['responsavel']} | Prioridade: {r['prioridade']}" for r in respostas])
                prompt_ia = f"""
                Atue como especialista em Gestão da Qualidade e Programa 5S da TM Engenharia e serviços.
                Analise os resultados desta auditoria na empresa {empresa}, setor {setor}, com nota geral de {nota_geral}% ({classificacao}).
                Não conformidades registradas:
                {texto_ncs if texto_ncs else 'Nenhuma não conformidade encontrada.'}

                Escreva um breve parecer executivo técnico (máximo 2 parágrafos) destacando os pontos fortes, o impacto das não conformidades e orientações gerais para manutenção da autodisciplina da equipe. Não inclua cabeçalhos extras, datas, horas ou códigos de auditoria.
                """
                with st.spinner("Redigindo parecer técnico executivo..."):
                    parecer = model.generate_content(prompt_ia)
                    st.info(f"**Parecer Técnico Executivo:**\n\n{parecer.text}")
            except Exception as e:
                st.warning(f"Não foi possível gerar o parecer automático da IA: {e}")

        # Tabela e Fotos do Plano de Ação Simplificado (Sem Prazo)
        st.markdown("### Plano de Ação Corretiva")
        if len(respostas) == 0:
            st.success("Nenhuma Não Conformidade registrada. O setor atende integralmente aos requisitos avaliados.")
        else:
            for item in respostas:
                with st.container(border=True):
                    st.markdown(f"**{item['codigo']} — {item['senso']}** | Prioridade: **{item['prioridade']}**")
                    st.markdown(f"**Item Avaliado:** {item['pergunta']}")
                    st.markdown(f"**Fato / Desvio:** {item['fato'] if item['fato'] else 'Não detalhado'}")
                    st.markdown(f"**Ação Corretiva Proposta:** {item['acao'] if item['acao'] else 'Não detalhada'}")
                    st.markdown(f"**Responsável pela Execução:** {item['responsavel'] if item['responsavel'] else 'A definir'}")

                    if item["fotos"]:
                        cols_foto = st.columns(min(len(item["fotos"]), 4))
                        for idx_f, foto in enumerate(item["fotos"]):
                            with cols_foto[idx_f % 4]:
                                st.image(foto, caption=f"Evidência {item['codigo']}", use_container_width=True)

        st.markdown('<div class="rodape-tm">Programa 5S - TM Engenharia e serviços</div>', unsafe_allow_html=True)
        st.caption("Dica: Para salvar em PDF no celular ou computador, toque no menu do navegador (⋮) e selecione 'Imprimir' > 'Salvar como PDF'.")
