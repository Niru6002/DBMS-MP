import streamlit as st
import pandas as pd
from datetime import datetime, date
from db_operations import *

# Page configuration
st.set_page_config(
    page_title="Grant Management System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Apple-inspired theme
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem; 
        font-weight: 700; 
        color: #1d1d1f; 
        text-align: center; 
        padding: 2rem 0 1rem 0;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.75rem; 
        font-weight: 600; 
        color: #1d1d1f; 
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.3px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #0071e3;
    }
    .stats-container {
        background: linear-gradient(135deg, #f5f5f7 0%, #e8e8ed 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }
    div[data-testid="column"] > div > div > button {
        height: 120px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        border: 2px solid #d2d2d7 !important;
        background: white !important;
        color: #1d1d1f !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    div[data-testid="column"] > div > div > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
        border-color: #0071e3 !important;
        background: #f5f5f7 !important;
    }
    div[data-testid="column"] > div > div > button:active {
        transform: translateY(-2px) !important;
    }
    .nav-section {
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e8e8ed;
    }
    .nav-section h2 {
        color: #1d1d1f;
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .nav-section p {
        color: #6e6e73;
        font-size: 1rem;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_db():
    db = DatabaseConnection(host='localhost', user='root', password='root@123', database='grant_management')
    db.create_database()
    success, message = db.connect()
    if not success:
        st.error(f"Database connection failed: {message}")
        return None
    return db

def get_operations(db):
    return {
        'division': DivisionOperations(db),
        'region': RegionOperations(db),
        'topic': TopicOperations(db),
        'grantee': GranteeOperations(db),
        'grant': GrantOperations(db),
        'beneficiary': GrantBeneficiaryOperations(db),
        'milestone': MilestoneOperations(db),
        'grantee_univs': GranteeUnivsOperations(db),
        'grant_topic': GrantTopicOperations(db)
    }

def show_crud_operations(entity_name, ops, columns_config):
    """Generic CRUD interface"""
    st.markdown(f'<p class="sub-header">{columns_config["title"]}</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])
    
    # VIEW ALL
    with tab1:
        df = ops[entity_name].read_all()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f"No {entity_name} records found.")
    
    # CREATE
    with tab2:
        columns_config["create_form"](ops, entity_name)
    
    # UPDATE
    with tab3:
        columns_config["update_form"](ops, entity_name)
    
    # DELETE
    with tab4:
        columns_config["delete_form"](ops, entity_name)

# ==================== DIVISION ====================
def division_create_form(ops, entity_name):
    with st.form("create_division"):
        name = st.text_input("Division Name*")
        description = st.text_area("Description")
        if st.form_submit_button("Create"):
            if name:
                success, msg = ops[entity_name].create(name, description)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def division_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        div_id = st.selectbox("Select Division", df['division_id'].tolist(),
                             format_func=lambda x: f"ID: {x} - {df[df['division_id']==x]['name'].values[0]}")
        data = ops[entity_name].read_by_id(div_id)
        with st.form("update_division"):
            name = st.text_input("Name*", value=data.get('name', ''))
            desc = st.text_area("Description", value=data.get('description', ''))
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(div_id, name, desc)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def division_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        div_id = st.selectbox("Select to Delete", df['division_id'].tolist(),
                             format_func=lambda x: f"ID: {x} - {df[df['division_id']==x]['name'].values[0]}")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(div_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== REGION ====================
def region_create_form(ops, entity_name):
    with st.form("create_region"):
        name = st.text_input("Region Name*")
        if st.form_submit_button("Create"):
            if name:
                success, msg = ops[entity_name].create(name)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def region_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        reg_id = st.selectbox("Select Region", df['region_id'].tolist(),
                             format_func=lambda x: f"ID: {x} - {df[df['region_id']==x]['name'].values[0]}")
        data = ops[entity_name].read_by_id(reg_id)
        with st.form("update_region"):
            name = st.text_input("Name*", value=data.get('name', ''))
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(reg_id, name)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def region_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        reg_id = st.selectbox("Select to Delete", df['region_id'].tolist(),
                             format_func=lambda x: f"ID: {x} - {df[df['region_id']==x]['name'].values[0]}")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(reg_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== TOPIC ====================
def topic_create_form(ops, entity_name):
    with st.form("create_topic"):
        name = st.text_input("Topic Name*")
        category = st.text_input("Category")
        if st.form_submit_button("Create"):
            if name:
                success, msg = ops[entity_name].create(name, category)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def topic_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        topic_id = st.selectbox("Select Topic", df['topic_id'].tolist(),
                               format_func=lambda x: f"ID: {x} - {df[df['topic_id']==x]['name'].values[0]}")
        data = ops[entity_name].read_by_id(topic_id)
        with st.form("update_topic"):
            name = st.text_input("Name*", value=data.get('name', ''))
            category = st.text_input("Category", value=data.get('category', ''))
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(topic_id, name, category)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def topic_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        topic_id = st.selectbox("Select to Delete", df['topic_id'].tolist(),
                               format_func=lambda x: f"ID: {x} - {df[df['topic_id']==x]['name'].values[0]}")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(topic_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== GRANTEE ====================
def grantee_create_form(ops, entity_name):
    with st.form("create_grantee"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name*")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        with col2:
            addr = st.text_area("Address")
            g_type = st.selectbox("Type", ["University", "Institute", "Foundation", "NGO", "Corporation", "Other"])
        if st.form_submit_button("Create"):
            if name:
                success, msg = ops[entity_name].create(name, email, addr, phone, g_type)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def grantee_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        g_id = st.selectbox("Select Grantee", df['grantee_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['grantee_id']==x]['name'].values[0]}")
        data = ops[entity_name].read_by_id(g_id)
        with st.form("update_grantee"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name*", value=data.get('name', ''))
                email = st.text_input("Email", value=data.get('email', ''))
                phone = st.text_input("Phone", value=data.get('phone', ''))
            with col2:
                addr = st.text_area("Address", value=data.get('addr', ''))
                types = ["University", "Institute", "Foundation", "NGO", "Corporation", "Other"]
                idx = types.index(data.get('grantee_type', 'Other')) if data.get('grantee_type') in types else 0
                g_type = st.selectbox("Type", types, index=idx)
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(g_id, name, email, addr, phone, g_type)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def grantee_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        g_id = st.selectbox("Select to Delete", df['grantee_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['grantee_id']==x]['name'].values[0]}")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(g_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== GRANT ====================
def grant_create_form(ops, entity_name):
    regions_df = ops['region'].read_all()
    divisions_df = ops['division'].read_all()
    
    with st.form("create_grant"):
        purpose = st.text_area("Purpose*")
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date*")
            date_awarded = st.date_input("Date Awarded*")
        with col2:
            close_date = st.date_input("Close Date*")
            duration = st.number_input("Duration (months)*", min_value=1, value=12)
        with col3:
            amount = st.number_input("Amount*", min_value=0.0, format="%.2f")
        
        region_id = st.selectbox("Region", regions_df['region_id'].tolist() if not regions_df.empty else [])
        division_id = st.selectbox("Division", divisions_df['division_id'].tolist() if not divisions_df.empty else [])
        
        if st.form_submit_button("Create"):
            if purpose:
                success, msg = ops[entity_name].create(purpose, date_awarded, duration, close_date,
                                                      start_date, amount, region_id, division_id)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def grant_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        g_id = st.selectbox("Select Grant", df['grant_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['grant_id']==x]['purpose'].values[0][:30]}...")
        data = ops[entity_name].read_by_id(g_id)
        regions_df = ops['region'].read_all()
        divisions_df = ops['division'].read_all()
        
        with st.form("update_grant"):
            purpose = st.text_area("Purpose*", value=data.get('purpose', ''))
            col1, col2, col3 = st.columns(3)
            with col1:
                start_date = st.date_input("Start Date*", value=data.get('start_date', date.today()))
                date_awarded = st.date_input("Date Awarded*", value=data.get('date_awarded', date.today()))
            with col2:
                close_date = st.date_input("Close Date*", value=data.get('close_date', date.today()))
                duration = st.number_input("Duration", min_value=1, value=data.get('duration', 12))
            with col3:
                amount = st.number_input("Amount", min_value=0.0, value=float(data.get('amount', 0)), format="%.2f")
            
            region_id = st.selectbox("Region", regions_df['region_id'].tolist() if not regions_df.empty else [])
            division_id = st.selectbox("Division", divisions_df['division_id'].tolist() if not divisions_df.empty else [])
            
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(g_id, purpose, date_awarded, duration, close_date,
                                                      start_date, amount, region_id, division_id)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def grant_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        g_id = st.selectbox("Select to Delete", df['grant_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['grant_id']==x]['purpose'].values[0][:30]}...")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(g_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== MILESTONE ====================
def milestone_create_form(ops, entity_name):
    grants_df = ops['grant'].read_all()
    with st.form("create_milestone"):
        if not grants_df.empty:
            grant_id = st.selectbox("Grant*", grants_df['grant_id'].tolist(),
                                   format_func=lambda x: f"ID: {x} - {grants_df[grants_df['grant_id']==x]['purpose'].values[0][:30]}...")
        else:
            st.warning("Create a grant first")
            grant_id = None
        
        milestone_desc = st.text_area("Description*")
        col1, col2 = st.columns(2)
        with col1:
            due_date = st.date_input("Due Date*")
        with col2:
            completion = st.slider("Completion %", 0, 100, 0)
        
        if st.form_submit_button("Create"):
            if grant_id and milestone_desc:
                success, msg = ops[entity_name].create(grant_id, milestone_desc, due_date, completion)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def milestone_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        m_id = st.selectbox("Select Milestone", df['milestone_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['milestone_id']==x]['milestone_desc'].values[0][:30]}...")
        data = ops[entity_name].read_by_id(m_id)
        grants_df = ops['grant'].read_all()
        
        with st.form("update_milestone"):
            if not grants_df.empty:
                grant_id = st.selectbox("Grant*", grants_df['grant_id'].tolist())
            else:
                grant_id = data.get('grant_id')
            
            milestone_desc = st.text_area("Description*", value=data.get('milestone_desc', ''))
            col1, col2 = st.columns(2)
            with col1:
                due_date = st.date_input("Due Date*", value=data.get('due_date', date.today()))
            with col2:
                completion = st.slider("Completion %", 0, 100, data.get('completion', 0))
            
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(m_id, grant_id, milestone_desc, due_date, completion)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def milestone_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        m_id = st.selectbox("Select to Delete", df['milestone_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['milestone_id']==x]['milestone_desc'].values[0][:30]}...")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(m_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== BENEFICIARY ====================
def beneficiary_create_form(ops, entity_name):
    grantees_df = ops['grantee'].read_all()
    with st.form("create_beneficiary"):
        if not grantees_df.empty:
            grantee_id = st.selectbox("Grantee*", grantees_df['grantee_id'].tolist(),
                                     format_func=lambda x: f"ID: {x} - {grantees_df[grantees_df['grantee_id']==x]['name'].values[0]}")
        else:
            st.warning("Create a grantee first")
            grantee_id = None
        
        institution = st.text_input("Institution*")
        description = st.text_area("Description")
        county = st.text_input("County of Institute")
        
        if st.form_submit_button("Create"):
            if grantee_id and institution:
                success, msg = ops[entity_name].create(grantee_id, institution, description, county)
                st.success("Created!" if success else msg)
                if success: st.rerun()

def beneficiary_update_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        b_id = st.selectbox("Select Beneficiary", df['beneficiary_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['beneficiary_id']==x]['institution'].values[0]}")
        data = ops[entity_name].read_by_id(b_id)
        grantees_df = ops['grantee'].read_all()
        
        with st.form("update_beneficiary"):
            if not grantees_df.empty:
                grantee_id = st.selectbox("Grantee*", grantees_df['grantee_id'].tolist())
            else:
                grantee_id = data.get('grantee_id')
            
            institution = st.text_input("Institution*", value=data.get('institution', ''))
            description = st.text_area("Description", value=data.get('description', ''))
            county = st.text_input("County", value=data.get('county_of_institute', ''))
            
            if st.form_submit_button("Update"):
                success, msg = ops[entity_name].update(b_id, grantee_id, institution, description, county)
                st.success("Updated!" if success else msg)
                if success: st.rerun()

def beneficiary_delete_form(ops, entity_name):
    df = ops[entity_name].read_all()
    if not df.empty:
        b_id = st.selectbox("Select to Delete", df['beneficiary_id'].tolist(),
                           format_func=lambda x: f"ID: {x} - {df[df['beneficiary_id']==x]['institution'].values[0]}")
        if st.button("Delete", type="primary"):
            success, msg = ops[entity_name].delete(b_id)
            st.success("Deleted!" if success else msg)
            if success: st.rerun()

# ==================== MAIN APPLICATION ====================
def main():
    # Initialize database
    db = init_db()
    if not db:
        st.error("Failed to connect to database. Please check your MySQL server.")
        return
    
    ops = get_operations(db)
    
    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Database Setup (in sidebar for admin)
    with st.sidebar.expander("Database Setup"):
        if st.button("Initialize Schema"):
            success, msg = db.initialize_schema('schema.sql')
            if success:
                st.success(msg)
            else:
                st.error(msg)
    
    # Entity configurations
    configs = {
        'division': {'title': 'Division Management', 
                    'create_form': division_create_form, 'update_form': division_update_form, 'delete_form': division_delete_form},
        'region': {'title': 'Region Management',
                  'create_form': region_create_form, 'update_form': region_update_form, 'delete_form': region_delete_form},
        'topic': {'title': 'Topic Management',
                 'create_form': topic_create_form, 'update_form': topic_update_form, 'delete_form': topic_delete_form},
        'grantee': {'title': 'Grantee Management',
                   'create_form': grantee_create_form, 'update_form': grantee_update_form, 'delete_form': grantee_delete_form},
        'grant': {'title': 'Grant Management',
                 'create_form': grant_create_form, 'update_form': grant_update_form, 'delete_form': grant_delete_form},
        'beneficiary': {'title': 'Beneficiary Management',
                       'create_form': beneficiary_create_form, 'update_form': beneficiary_update_form, 'delete_form': beneficiary_delete_form},
        'milestone': {'title': 'Milestone Management',
                     'create_form': milestone_create_form, 'update_form': milestone_update_form, 'delete_form': milestone_delete_form},
    }
    
    # Route to appropriate page
    page = st.session_state.current_page
    
    if page == "Home":
        st.markdown('<h1 class="main-header">Grant Management System</h1>', unsafe_allow_html=True)
        
        # Statistics Dashboard
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-bottom: 1rem;">Dashboard Overview</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Grants", len(ops['grant'].read_all()))
        with col2:
            st.metric("Total Grantees", len(ops['grantee'].read_all()))
        with col3:
            st.metric("Total Milestones", len(ops['milestone'].read_all()))
        with col4:
            st.metric("Total Topics", len(ops['topic'].read_all()))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation Section
        st.markdown('''
        <div class="nav-section">
            <h2>Management Sections</h2>
            <p>Select a section below to manage your grant system data</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.write("")  # Spacing
        
        # Grid Navigation Buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Division", use_container_width=True, key="nav_division"):
                st.session_state.current_page = "division"
                st.rerun()
        with col2:
            if st.button("Region", use_container_width=True, key="nav_region"):
                st.session_state.current_page = "region"
                st.rerun()
        with col3:
            if st.button("Topic", use_container_width=True, key="nav_topic"):
                st.session_state.current_page = "topic"
                st.rerun()
        with col4:
            if st.button("Grantee", use_container_width=True, key="nav_grantee"):
                st.session_state.current_page = "grantee"
                st.rerun()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Grant", use_container_width=True, key="nav_grant"):
                st.session_state.current_page = "grant"
                st.rerun()
        with col2:
            if st.button("Beneficiary", use_container_width=True, key="nav_beneficiary"):
                st.session_state.current_page = "beneficiary"
                st.rerun()
        with col3:
            if st.button("Milestone", use_container_width=True, key="nav_milestone"):
                st.session_state.current_page = "milestone"
                st.rerun()
        with col4:
            if st.button("Relationships", use_container_width=True, key="nav_relationships"):
                st.session_state.current_page = "relationships"
                st.rerun()
        
    elif page in ["division", "region", "topic", "grantee", "grant", "beneficiary", "milestone"]:
        # Show CRUD operations for selected entity
        st.markdown(f'<h1 class="main-header">{configs[page]["title"]}</h1>', unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to Home", use_container_width=False):
            st.session_state.current_page = "Home"
            st.rerun()
        
        show_crud_operations(page, ops, configs[page])
    elif page == "relationships":
        st.markdown('<h1 class="main-header">Relationship Management</h1>', unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to Home", use_container_width=False):
            st.session_state.current_page = "Home"
            st.rerun()
        
        # Relationship tabs
        rel_tab1, rel_tab2 = st.tabs(["Grantee-Grant Links", "Grant-Topic Links"])
        
        with rel_tab1:
            st.markdown('<p class="sub-header">Grantee-Grant Relationships</p>', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["View All", "Create Link"])
            
            with tab1:
                df = ops['grantee_univs'].read_all()
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No relationships found.")
        
        with tab2:
            grantees = ops['grantee'].read_all()
            grants = ops['grant'].read_all()
            
            with st.form("link_grantee_grant"):
                if not grantees.empty and not grants.empty:
                    grantee_id = st.selectbox("Grantee*", grantees['grantee_id'].tolist(),
                                             format_func=lambda x: f"{grantees[grantees['grantee_id']==x]['name'].values[0]}")
                    grant_id = st.selectbox("Grant*", grants['grant_id'].tolist(),
                                           format_func=lambda x: f"ID: {x} - {grants[grants['grant_id']==x]['purpose'].values[0][:30]}")
                    assoc_body = st.text_input("Associated Body")
                    
                    if st.form_submit_button("Create Link"):
                        success, msg = ops['grantee_univs'].create(grantee_id, grant_id, assoc_body)
                        st.success("Link created!" if success else msg)
                        if success: st.rerun()
                else:
                    st.warning("Please create grantees and grants first")
        
        with rel_tab2:
            st.markdown('<p class="sub-header">Grant-Topic Relationships</p>', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["View All", "Create Link"])
            
            with tab1:
                df = ops['grant_topic'].read_all()
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No relationships found.")
            
            with tab2:
                grants = ops['grant'].read_all()
                topics = ops['topic'].read_all()
                
                with st.form("link_grant_topic"):
                    if not grants.empty and not topics.empty:
                        grant_id = st.selectbox("Grant*", grants['grant_id'].tolist(),
                                               format_func=lambda x: f"ID: {x} - {grants[grants['grant_id']==x]['purpose'].values[0][:30]}")
                        topic_id = st.selectbox("Topic*", topics['topic_id'].tolist(),
                                               format_func=lambda x: f"{topics[topics['topic_id']==x]['name'].values[0]}")
                        
                        if st.form_submit_button("Create Link"):
                            success, msg = ops['grant_topic'].create(grant_id, topic_id)
                            st.success("Link created!" if success else msg)
                            if success: st.rerun()
                    else:
                        st.warning("Please create grants and topics first")

if __name__ == "__main__":
    main()
