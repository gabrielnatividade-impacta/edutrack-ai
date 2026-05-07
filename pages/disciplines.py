import streamlit as st
import requests
import json
from datetime import datetime
from typing import Tuple, List, Optional

# Configuração da página
st.set_page_config(
    page_title="Disciplinas",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL base do backend Xano
XANO_BASE_URL = "https://eu-0.xano.io/api:KQnBJ_Bb"  # TODO: Substituir com URL real

# ============================================================================
# FUNÇÕES DE INTEGRAÇÃO COM O BACKEND
# ============================================================================

def get_auth_token() -> Optional[str]:
    """Recupera token de autenticação do session state"""
    if "auth_token" in st.session_state:
        return st.session_state.auth_token
    return None


def search_subjects(name: Optional[str] = None, has_overdue: bool = False) -> Tuple[Optional[List[dict]], Optional[str]]:
    """
    Busca disciplinas no backend com filtros opcionais.
    
    Args:
        name: Filtro de busca por nome (opcional)
        has_overdue: Se True, retorna apenas disciplinas com tarefas atrasadas
    
    Returns:
        Tupla (subjects, error_message)
    """
    try:
        # Preparar query parameters
        params = {}
        if name:
            params["name"] = name
        if has_overdue:
            params["has_overdue"] = "true"
        
        # Preparar headers com token de autenticação
        headers = {
            "Content-Type": "application/json"
        }
        
        token = get_auth_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        # Fazer requisição
        response = requests.get(
            f"{XANO_BASE_URL}/subjects/search",
            params=params,
            headers=headers,
            timeout=10
        )
        
        # Tratar diferentes status codes
        if response.status_code == 401:
            return None, "❌ Erro de autenticação. Por favor, faça login novamente."
        elif response.status_code == 403:
            return None, "❌ Acesso negado. Você não tem permissão para acessar estas disciplinas."
        elif response.status_code == 400:
            return None, "❌ Parâmetros inválidos. Verifique seus filtros."
        elif response.status_code == 500:
            return None, "❌ Erro no servidor. Tente novamente mais tarde."
        elif response.status_code == 200:
            subjects = response.json()
            return subjects, None
        else:
            return None, f"❌ Erro {response.status_code}: {response.reason}"
    
    except requests.exceptions.Timeout:
        return None, "⏱️ A requisição demorou muito. Tente novamente."
    except requests.exceptions.ConnectionError:
        return None, "📡 Erro de conexão. Verifique sua internet."
    except json.JSONDecodeError:
        return None, "❌ Resposta inválida do servidor."
    except Exception as e:
        return None, f"❌ Erro: {str(e)}"


def format_date(date_string: Optional[str]) -> str:
    """Formata data ISO para formato legível"""
    if not date_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return date_string


def display_subjects_table(subjects: List[dict]) -> None:
    """
    Renderiza tabela de disciplinas com expandores para tarefas atrasadas.
    
    Args:
        subjects: Lista de disciplinas retornada pela API
    """
    if not subjects:
        st.info("📭 Nenhuma disciplina encontrada com os filtros aplicados.")
        return
    
    # Renderizar cada disciplina em um container
    for subject in subjects:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{subject.get('name', 'N/A')}**")
                if subject.get('description'):
                    st.caption(subject['description'])
            
            with col2:
                st.write(f"📖 {subject.get('code', 'N/A')}")
            
            with col3:
                status = subject.get('status', 'unknown')
                status_emoji = "🟢" if status == "active" else "🔴"
                st.write(f"{status_emoji} {status.title()}")
            
            # Exibir tarefas atrasadas se houver
            overdue_count = subject.get('overdue_count', 0)
            if overdue_count > 0:
                with st.expander(f"⚠️ {overdue_count} tarefa(s) atrasada(s)", expanded=False):
                    overdue_tasks = subject.get('overdue_tasks', [])
                    
                    # Criar dados para tabela
                    task_data = []
                    for task in overdue_tasks:
                        task_data.append({
                            "Título": task.get('title', 'N/A'),
                            "Status": task.get('status', 'N/A').title(),
                            "Data de Vencimento": format_date(task.get('due_date'))
                        })
                    
                    # Exibir tabela formatada
                    if task_data:
                        st.dataframe(task_data, use_container_width=True, hide_index=True)
                    else:
                        st.write("Nenhuma tarefa atrasada encontrada.")


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

st.title("📚 Disciplinas")
st.markdown("---")

# Criar abas
tab1, tab2 = st.tabs(["🔍 Buscar & Listar", "➕ Nova Disciplina"])

with tab1:
    st.header("Buscar e Filtrar Disciplinas")
    
    # Criar layout com filtros
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_name = st.text_input(
            "🔍 Buscar por nome",
            placeholder="Digite o nome da disciplina...",
            key="search_name"
        )
    
    with col2:
        has_overdue = st.checkbox(
            "⚠️ Apenas com atrasos",
            value=False,
            help="Mostrar apenas disciplinas com tarefas vencidas"
        )
    
    with col3:
        st.write("")  # Espaço vazio para alinhamento
        search_button = st.button("🔍 Pesquisar", use_container_width=True)
    
    st.markdown("---")
    
    # Executar busca se solicitado
    if search_button or search_name or has_overdue:
        with st.spinner("Carregando disciplinas..."):
            subjects, error_message = search_subjects(name=search_name, has_overdue=has_overdue)
        
        if error_message:
            st.error(error_message)
        elif subjects is not None:
            st.success(f"✅ Encontradas {len(subjects)} disciplina(s)")
            display_subjects_table(subjects)

with tab2:
    st.header("Criar Nova Disciplina")
    st.info("🚧 Funcionalidade em desenvolvimento - formulário para cadastro será adicionado em breve.")
