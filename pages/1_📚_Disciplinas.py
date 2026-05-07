"""
Página de Gestão de Disciplinas
Integra com o endpoint GET /subjects/search do backend Xano
para exibir disciplinas com filtros de busca e tarefas atrasadas.
"""

import streamlit as st
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Disciplinas", page_icon="📚")
st.title("Gestão de Disciplinas")

# ============================================================================
# CONFIGURAÇÃO DE API
# ============================================================================

# TODO: Substituir pela URL real do seu backend Xano
XANO_BASE_URL = "https://eu-0.xano.io/api:KQnBJ_Bb"
SUBJECTS_SEARCH_ENDPOINT = f"{XANO_BASE_URL}/subjects/search"


# ============================================================================
# FUNÇÕES DE INTEGRAÇÃO COM API
# ============================================================================

def get_auth_token() -> Optional[str]:
    """
    Recupera o token de autenticação da sessão Streamlit.
    
    Returns:
        Token de autenticação ou None se não disponível
    """
    # O token deveria estar disponível após login bem-sucedido
    # Armazenar em st.session_state.auth_token durante o fluxo de login
    return st.session_state.get("auth_token", None)


def search_subjects(
    name: Optional[str] = None,
    has_overdue: bool = False,
) -> tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Busca disciplinas no backend Xano com filtros opcionais.
    
    Args:
        name: Filtro por nome (busca case-insensitive)
        has_overdue: Se True, retorna apenas disciplinas com tarefas atrasadas
    
    Returns:
        Tupla (lista_de_disciplinas, mensagem_de_erro)
        Se erro, lista_de_disciplinas será vazia e mensagem_de_erro conterá detalhes
    """
    try:
        # Preparar query parameters
        params = {}
        if name and name.strip():
            params["name"] = name.strip()
        if has_overdue:
            params["has_overdue"] = True
        
        # Preparar headers com autenticação
        headers = {"Content-Type": "application/json"}
        auth_token = get_auth_token()
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        # Fazer requisição GET
        response = requests.get(
            SUBJECTS_SEARCH_ENDPOINT,
            params=params,
            headers=headers,
            timeout=10,
        )
        
        # Tratar diferentes status codes
        if response.status_code == 401:
            return [], "❌ Erro de autenticação. Faça login novamente."
        elif response.status_code == 403:
            return [], "❌ Acesso negado. Você não tem permissão para acessar essas disciplinas."
        elif response.status_code == 400:
            error_detail = response.json().get("error_message", "Parâmetros inválidos")
            return [], f"❌ Erro na requisição: {error_detail}"
        elif response.status_code == 500:
            return [], "❌ Erro no servidor. Tente novamente mais tarde."
        elif response.status_code != 200:
            return [], f"❌ Erro na requisição (HTTP {response.status_code})"
        
        # Tentar parsear JSON
        subjects = response.json()
        if not isinstance(subjects, list):
            return [], "❌ Formato de resposta inválido do servidor"
        
        return subjects, None
    
    except requests.exceptions.Timeout:
        return [], "❌ Timeout na conexão com o servidor. Tente novamente."
    except requests.exceptions.ConnectionError:
        return [], "❌ Erro de conexão com o backend. Verifique sua internet."
    except requests.exceptions.RequestException as e:
        return [], f"❌ Erro na requisição: {str(e)}"
    except ValueError:
        return [], "❌ Erro ao processar resposta do servidor (JSON inválido)"
    except Exception as e:
        return [], f"❌ Erro inesperado: {str(e)}"


def format_date(date_string: Optional[str]) -> str:
    """
    Formata uma data ISO para formato legível.
    
    Args:
        date_string: Data em formato ISO ou None
    
    Returns:
        Data formatada ou "N/A"
    """
    if not date_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return date_string


def display_subjects_table(subjects: List[Dict[str, Any]]) -> None:
    """
    Exibe uma tabela com as disciplinas e expandores para tarefas atrasadas.
    
    Args:
        subjects: Lista de disciplinas com dados enriquecidos
    """
    if not subjects:
        st.warning("📭 Nenhuma disciplina encontrada com os critérios de busca.")
        return
    
    st.success(f"✅ {len(subjects)} disciplina(s) encontrada(s)")
    
    # Exibir cada disciplina em um container
    for subject in subjects:
        subject_id = subject.get("id", "")
        subject_name = subject.get("name", "Sem nome")
        subject_code = subject.get("code", "")
        subject_status = subject.get("status", "ativo")
        subject_description = subject.get("description", "")
        overdue_count = subject.get("overdue_count", 0)
        overdue_tasks = subject.get("overdue_tasks", [])
        
        # Container para cada disciplina
        with st.container(border=True):
            # Header com informações principais
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### {subject_name}")
                if subject_description:
                    st.caption(subject_description)
            
            with col2:
                if subject_code:
                    st.markdown(f"**Código:** {subject_code}")
            
            with col3:
                # Badge de status e tarefas atrasadas
                status_color = "🟢" if subject_status == "ativo" else "🔴"
                st.markdown(f"{status_color} {subject_status.capitalize()}")
                
                if overdue_count > 0:
                    st.markdown(f"⏰ **{overdue_count} atrasada(s)**")
            
            # Expandor com tarefas atrasadas (se houver)
            if overdue_count > 0 and overdue_tasks:
                with st.expander(f"📋 Ver {overdue_count} tarefa(s) atrasada(s)"):
                    # Criar tabela com tarefas atrasadas
                    tasks_data = []
                    for task in overdue_tasks:
                        task_status_icon = {
                            "completed": "✅",
                            "pending": "⏳",
                            "in_progress": "🔄",
                        }.get(task.get("status", ""), "❓")
                        
                        tasks_data.append({
                            "Status": task_status_icon,
                            "Título": task.get("title", "Sem título"),
                            "Data de Vencimento": format_date(task.get("due_date")),
                        })
                    
                    st.dataframe(
                        tasks_data,
                        use_container_width=True,
                        hide_index=True,
                    )


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

# Abas para separar Busca/Listagem de Cadastro
tab_lista, tab_novo = st.tabs(["🔍 Buscar & Listar", "➕ Nova Disciplina"])

# ============================================================================
# ABA: BUSCAR & LISTAR
# ============================================================================

with tab_lista:
    st.subheader("Buscar Disciplinas")
    
    # Componentes de busca
    col_search, col_overdue, col_button = st.columns([2, 1.5, 1])
    
    with col_search:
        search_name = st.text_input(
            "🔎 Buscar por nome...",
            placeholder="Digite o nome da disciplina",
            help="Busca case-insensitive em tempo real",
        )
    
    with col_overdue:
        has_overdue = st.checkbox(
            "⏰ Apenas com atrasos",
            help="Mostrar apenas disciplinas com tarefas vencidas",
        )
    
    with col_button:
        st.write("")  # Espaçador para alinhar o botão
        search_button = st.button(
            "🔍 Pesquisar",
            use_container_width=True,
            type="primary",
        )
    
    # Divider
    st.divider()
    
    # Executar busca quando clicar no botão, digitar algo ou mudar checkbox
    if search_button or search_name or has_overdue:
        with st.spinner("🔄 Buscando disciplinas..."):
            subjects, error_message = search_subjects(
                name=search_name,
                has_overdue=has_overdue,
            )
        
        if error_message:
            st.error(error_message)
        else:
            display_subjects_table(subjects)
    else:
        # Estado inicial: mostrar mensagem informativa
        st.info(
            "👉 Use o campo de busca acima para encontrar suas disciplinas. "
            "Você pode filtrar por nome e/ou mostrar apenas aquelas com tarefas atrasadas."
        )

# ============================================================================
# ABA: NOVA DISCIPLINA
# ============================================================================

with tab_novo:
    st.subheader("Cadastrar Nova Disciplina")
    
    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina", placeholder="Ex: Matemática Avançada")
        codigo = st.text_input("Código", placeholder="Ex: MAT001")
        professor = st.text_input("Nome do Professor", placeholder="Ex: Prof. João Silva")
        descricao = st.text_area("Descrição", placeholder="Descrição opcional da disciplina")
        dia_semana = st.selectbox(
            "Dia da Aula",
            ["Seg", "Ter", "Qua", "Qui", "Sex", "Sábado"],
        )
        
        submitted = st.form_submit_button("💾 Salvar")
        
        if submitted:
            if not nome or not codigo:
                st.error("❌ Nome e Código são obrigatórios")
            else:
                st.success(f"✅ Disciplina '{nome}' ({codigo}) cadastrada! (Simulação)")
                st.info("💡 Para integração completa, implemente o endpoint POST /subjects")