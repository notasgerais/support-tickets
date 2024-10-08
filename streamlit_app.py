import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Mapa de Conteúdos")
st.write(
    """
    Aplicativo para criação de Mapa de Conteúdos das avaliações.
    """
)

disciplina = st.selectbox(
    "Selecione a Disciplina",
    ["Matemática", "Português", "Ciências", "Geografia", "História", "Inglês", "Espanhol", "Produção Textual", "Literatura" ]
)

turma = st.selectbox(
    "Selecione a Turma",
    ["6º Ano", "7º Ano", "8º Ano", "9º Ano", "1ª Série", "2ª Série", "3ª Série"]
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"Q{i}" for i in range(1, 1, 1)],
        "Conteúdo": np.random.choice(issue_descriptions, size=0),
        "Gabarito": np.random.choice(["Aberta", "A", "B", "C", "D", "E"], size=0),
        "Valor": 0.0,
        "Dificuldade": np.random.choice(["Fácil", "Média", "Difícil"], size=0),
        # "Date Submitted": [
        #     datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
        #     for _ in range(1)
        # ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Adicionar Questão")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    issue = st.text_area("Conteúdo da Questão")
    gabarito = st.selectbox("Gabarito", ["Aberta", "A", "B", "C", "D", "E"])
    valor = st.number_input("Insira o valor da questão", value=1.0, step=0.1)
    priority = st.selectbox("Dificuldade", ["Fácil", "Média", "Difícil"])
    submitted = st.form_submit_button("Adicionar")

if submitted:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    if len(st.session_state.df)==0:
        recent_ticket_number = 0
    else:  
        recent_ticket_number = len(st.session_state.df)
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"Q{recent_ticket_number+1}",
                "Conteúdo": issue,
                "Gabarito": gabarito,
                "Valor": valor,
                "Dificuldade": priority,
                # "Date Submitted": today,
            }
        ]
    )

    # Show a little success message.
    #st.write("Ticket submitted! Here are the ticket details:")
    #st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([ st.session_state.df,df_new], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Lista de Questões Adicionadas")
st.write(f"Número de Questões: `{len(st.session_state.df)}`")
st.write(f"Disciplina: `{disciplina}`")
st.write(f"Turma: `{turma}`")


st.info(
    "Você pode editar o conteúdo, o gabarito, o valor e a dificuldade das questões clicando duas vezes"
    " na célula correspondente!",
    icon="✍️",
)

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
edited_df = st.data_editor(
    st.session_state.df,
    #num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Gabarito",
            help="Ticket status",
            options=["A","B","C", "D", "E", "Aberta"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Dificuldade",
            help="Priority",
            options=["Fácil", "Média", "Difícil"],
            required=True,
        ),
    },
    # Disable editing the ID and Date Submitted columns.
    #disabled=["ID"],
)

st.write(f"Valor Total das Questões: `{edited_df.Valor.sum()}`")

#save = st.form_submit_button("Salvar Planilha")

csv = edited_df.to_csv(index=False).encode('utf-8')
#disciplina = "Matematica"
st.download_button(
   "Salvar Mapa de Conteúdos",
   csv,
   f'{disciplina}_{turma}.csv',
   "text/csv",
   key='download-csv'
)

# columns = edited_df.columns.values.tolist()

# deletar = st.button("Apagar Planilha")

# if deletar:
#     #edited_df
#     st.session_state.df = pd.DataFrame(None)
    

