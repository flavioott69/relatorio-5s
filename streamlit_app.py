import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gerador Relatório 5S", page_icon="📋")

st.title("📋 Gerador de Relatório de Auditoria 5S")
st.write("Insira os dados da auditoria para gerar o relatório executivo padronizado.")

# Campo para a chave da API do Gemini (ou você pode fixar se preferir)
api_key = st.text_input("Cole sua Chave da API do Google AI Studio:", type="password")

setor = st.text_input("Setor Inspecionado (ex: Aves I):")
lider = st.text_input("Líder do Setor:")
pontos = st.number_input("Pontuação Geral:", min_value=0, max_value=100, value=95)

if st.button("Gerar Relatório"):
    if not api_key:
        st.warning("Por favor, insira sua chave da API do Gemini.")
    elif not setor:
        st.warning("Informe o setor inspecionado.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"Gere o relatório executivo de auditoria 5S para o setor {setor}, liderado por {lider}, com pontuação de {pontos} pontos, seguindo o padrão corporativo."
        
        with st.spinner("Gerando relatório..."):
            response = model.generate_content(prompt)
            st.markdown("### Resultado:")
            st.write(response.text)
