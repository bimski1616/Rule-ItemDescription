import streamlit as st
import pandas as pd
import re
import io

# ==========================================
# 1. CLEANING & LOGIC FUNCTIONS
# ==========================================

def clean_text(x):
    if pd.isna(x):
        return x
    x = str(x)
    x = x.lower()
    x = re.sub(r'[\n\r\t\xa0]', ' ', x)
    x = re.sub(r'[\\/]', ' ', x)
    x = re.sub(r'[^a-z0-9\s]', ' ', x)
    x = re.sub(r'\s+', ' ', x).strip()
    return x

def clean_text_2(x):
    if pd.isna(x):
        return x
    x = str(x)
    x = x.lower()
    x = re.sub(r'[\n\r\t\xa0]', ' ', x)
    x = re.sub(r'\s+', ' ', x).strip()
    return x

# --- L1 to L5 Rules (Standard) ---

def get_categorization_L1(item_desc_clean):
    text = str(item_desc_clean).lower()
    if "netgear re-tagging works on tower" in text: return 'Operation & Maintenance (MSS)'
    if "splicing and tracing core in existing closure" in text: return 'Operation & Maintenance (MSS)'
    if " ms " in text or text.startswith("ms ") or text.endswith(" ms"): return 'Operation & Maintenance (MSS)'
    if "rigger" in text: return 'Optimization & Network Management (RNO)'
    if "for new build" in text: return 'Installation-Test-Commissioning (TIN)'
    if any(k in text for k in ['inbuilding', 'lampsite', 'ibs', 'das', 'small cell', 'repeater', 'prru', 'rhub', 'indoor antenna']): return 'Inbuilding Coverage Services (IBC)'
    if any(k in text for k in ['optimization', 'optimize', 'drive test', 'walk test', 'network performance', 'kpi', 'benchmark', 'npo', 'parameter', 'tuning', 'measurement', 'ssv', 'rno', 'rf adjustment', 'data collection', 'oss data', 'analysis', 'npi']): return 'Optimization & Network Management (RNO)'
    if any(k in text for k in ['survey', 'tssr', 'site audit', 'design', 'planning', 'los', 'site hunt', 'sid', 'drawing', 'desgin', 'boq', 'tagging', 'gps coordinate']): return 'Survey (ENG)'
    if any(k in text for k in ['maintenance', 'helpdesk', 'managed service', 'operation', 'repair', 'spare part', 'fault', 'fuel', 'genset', 'cleaning', 'rent', 'lease', 'bill', 'support', 'corrective', 'preventive', 'ms fee', 'monitoring', 'assurance', 'keeper', 'freon', 'refrigerant', 'rewinding', 'taskforce', 'site visit', 'good part', 'handling adhoc', 'purifikasi', 'bushing', 'contactor', 'oli', 'capacity allowance', 'seal', 'pressure suit']): return 'Operation & Maintenance (MSS)'
    return 'Installation-Test-Commissioning (TIN)'

def get_categorization_L2(item_desc_clean_L2):
    text = str(item_desc_clean_L2).lower()
    if any(k in text for k in ["supply & install", "supply and install", "supply&install", "provide & install", "provide and install", "supply & fix", "supply and fix", "including wiring", "include wiring"]): return "Material & Services"
    service_keywords = ["installation", " install", "install ", "dismantle", "service", "survey", "optimize", "optimization", "maintenance", "manpower", "team", "visit", "test", "commissioning", "integration", "configuration", "audit", "design", "training", "consultancy", "logistic", "transport", "mobilization", "incentive", "return", "handling", "tagging", "splicing", "trench", "pulling", "roding", "construct", "drilling", "rewinding", "unwelding", "drawing", "documentation", "assurance", "monitoring", "analysis", "reporting", "tuning", "clearance", "keeper", "helpdesk", "managed service", "support", "verification", "collection", "induction", "registration", "rectification", "relocation", "replacement", "replace", "swap", "expansion", "upgrade", "implementation", "migration", "re-tagging", "trouble shooting", "cleaning", "rent", "lease", "bill", "purifikasi", "moving", "codeploy", "co-deploy", "works", "work", "fusion", "los survey", "parameter", "adjustment", "rigger", "custimization", "customization", "supervision", "atp", "bastian", "bast", "acceptance", "compensation", "pick up", "fee", "allowance", "permit", "po for", "document", "welding", "taskforce", "checking", "check", "oss", "walk test", "wt&oss", "pre-modernization", "modernization", "laying", "termination", "rearrangement", "pm package"]
    if any(k in text for k in service_keywords): return "Services Only"
    if text.startswith("new:") or text.startswith("new-") or text.startswith("new "): return "Services Only"
    return "Material Supply"

def get_categorization_L3(item_desc_clean):
    text = str(item_desc_clean).lower()
    if "incentive" in text or "points" in text: return "Incentive"
    if "logistic" in text or "return fault" in text or "good part" in text: return "Logistic"
    if any(k in text for k in ["pulling", "trench", "cable", "otb"]): return "Outside Plant (OSP)"
    if any(k in text for k in ["power", "rectifier", "battery", "genset", "generator", "ups", "inverter", "kwh", "mcb", "transformer", "ac power", "dc power", "lv ", "hv ", "breaker", "busbar"]): return "Power System"
    if any(k in text for k in ["ran", "radio", "bts", "nodeb", "enodeb", "gnodeb", "sran", "base station", "rru", "aau", "bbu", "rfu", "trx", "sector", "cell ", "cell-", "multi-sector", "antenna", "feeder", "jumper", "cpri", "tma", "combiner", "diplexer", "triplexer", "filter", "4g", "5g", "lte", "gul", "gsm", "umts", "nr ", "nsa", " sa ", "drive test", "walk test", "dt ", "ssv", "sso", "npi", "rno", "rf adjustment", "parameter", "optimization", "tuning", "network performance", "kpi", "rigger", "inbuilding", "ibs", "das", "lampsite", "small cell", "repeater", "prru", "rhub", "mocn", "roaming", "neighbor", "blind spot", "coverage", "distribution aerial", "feeder aerial", "service operation center", "remote radio unit"]): return "Radio Access Network (RAN)"
    if any(k in text for k in ["microwave", " mw ", " mw-", "-mw", "odu", "idu", "transmission", "trm", "backhaul", "per hop", "optical", "fiber", "fibre", " fo ", "ftth", "fbb", "osp", "isp", "olt", "ont", "gpon", "wdm", "mstp", "sdh", "dwdm", "otn", "ptn", "datacomm", "router", "switch", "ip ne", "ip_ne", "peering", "splicing", "roding", "duct", "aerial", "underground", "odf", "patch cord", "fat ", "fdt ", "closure", "lan ", "cat 6", "cat6", "metro", "ethernet", "access,olt", "access,blade", "access,rack", "wdm/mstp"]): return "Transmission (TRM)"
    if any(k in text for k in ["core network", " msc", " hlr", " hss", " epc", " mme", " sgsn", " ggsn", " ims", " volte", "cs core", "ps core", "packet core", "udm", "ausf", "amf", "smf", "upf", "pcrf", "dra", "stp", "sbc", "mgw", "softswitch", "media gateway", "signaling", "user plane", "control plane", "charging system", "ocs", "pcc", "cs helpdesk", "core site"]): return "Core Network (CORE)"
    if any(k in text for k in ["cme", "ac ", "dc ", "air conditioner", "conditioning", "pac ", "split ac", "cooling", "cabinet", "shelter", "enclosure", "rack", "cage", "pole", "tower", "monopole", "guyed", "civil", "grounding", "lightning", "arrester", "protection", "fuel", "tank", "sensor", "mechanical", "electrical", "concrete", "foundation", "fence", "tray", "ladder", "bracket", "mounting", "clamp", "bolt", "nut", "anchor", "pipe", "conduit", "trunking", "seal", "cement", "sand", "gravel", "macadam", "renovation", "refurbishment", "cleaning", "site keeper", "security", "freon", "oil", "lubricant", "pump", "valve", "compressor", "bushing", "contactor", "mecanical", "pressure suit", "reinstatement", "welding", "drilling", "hole", "anti theft", "atd", "lug", "scun", "connector"]): return "Supporting Facility (CME)"
    return "General Support"

def get_categorization_L4(item_desc_clean_L2):
    text = str(item_desc_clean_L2).lower()
    if "man-month" in text or "man month" in text or "*month" in text or " month" in text: return "Man-month"
    if "team" in text: return "Team"
    if "/site" in text or "per site" in text: return "Site"
    if "/hop" in text or "per hop" in text or " hop" in text: return "Hop"
    if "/each" in text or "pcs" in text or "per point" in text: return "Each"
    return "Each"

def get_categorization_L5(item_desc_clean):
    text = str(item_desc_clean).lower()
    if "rectification and expansion" in text: return "Swap/Replacement"
    if any(k in text for k in ['per point', 'allowance', 'incentive', 'return fault', 'return good part', 'good part', 'compensation', 'logistic from', 'self pick up', 'handling', 'rigger', 'visit', 'document', 'coordinate', 'gps', 'aos', 'project service', 'access registration', 'induction', 'team induction', 'restricted mining', 'special event', 'assurance', 'npi', 'taskforce']): return "Support"
    if any(k in text for k in ['optimization', 'performance', 'tuning', 'audit', 'ssv', 'sso', 'dt', 'drive test', 'npx', 'network performance', 'kpi', 'monitor', 'collection', 'verification', 'adjustment', 'acceptance', 'benchmark', 'parameters and neighboring cell', 'analysis and report', 'quality management', 'neighboring cell scripts', 'without car', 'walk test', 'iro_ethernet configuration', 'iro_fbb common', 'iro_mw idu', 'tsel_gul_rf_rigger', 'xl_gul_merge_rf_rigger', 'xl_gul_rf_rigger', 'ioh_gul_rf_rigger', 'otdr', 'fiber quality', 'board testing', 'antenna checking', 'light indicator', 'idu', 'odu', 'bbu', 'rru']): return "Optimization & Performance Management"
    if any(k in text for k in ['maintenance', 'trouble shooting', 'troubleshooting', 'repair', 'corrective', 'preventive', 'spare part', 'spare', 'rectification', 'fixing', 'warranty', 'helpdesk', 'support', 'ticket', 'complain', 'service operation center', 'soc', 'alarm clearance', 'tagging', 'reinstatement', 'site keeper', 'managed service', 'shopping list package', 'shopping list', 'refrigerant', 'refrigerant freon', 'refrigerant r22', 'refrigerant r407c', 'pressure suit', 'purifikasi', 'rewinding', 'rewelding', 'split ac', 'trench & backfill', 'xl ms lumpsum shopping list', 'cell down', 'p1', 'unwelding']): return "Maintenance Services"
    if any(k in text for k in ['swap', 'replace', 'replacement', 'migration', 'modernization', 'relocation', 're-arrangement', 'rearrange', 're-configuration']): return "Swap/Replacement"
    if any(k in text for k in ['dismantle', 'dismantlement', 'removal', 'remove', 'de-installation', 'return']): return "Dismantling"
    if any(k in text for k in ['expansion', 'upgrade', 'capacity', 'add-on', 'augment', 'growth', 'extension', 'license']): return "Additional/Upgrade"
    if any(k in text for k in ['new', 'installation', 'install', 'commissioning', 'integration', 'survey', 'deployment', 'rollout', 'implement', 'implementation', 'setup', 'construct', 'civil work', 'supply', 'material', 'pipe', 'cable', 'pole', 'bracket', 'connector', 'adapter', 'feeder', 'clamp', 'cabinet', 'rack', 'power', 'battery', 'concrete', 'conduit', 'splicing', 'fusion', 'device', 'drawing', 'dummy load', 'contactor', 'jumper', 'kabel', 'mcb', 'rod', 'bushing', 'seal', 'ties', 'module', 'lamp', 'trafo', 'mechanical', 'oli', 'otb', 'patch cord', 'pipa', 'pvc', 'tape', 'rhub box', 'codeploy', 'insert']): return "New Deployment"
    return "Others"

# --- NEW: REFINED CATEGORIZATION RULE (Milestone Mapping) ---

def categorize_item_refined(row):
    """
    Advanced categorization rule for Telecom BOQ items.
    """
    # 1. PRE-PROCESSING
    desc = str(row.get('Item Description', '')).lower()
    l1 = str(row.get('Level 1 Service Type', '')).lower()
    l2 = str(row.get('Level 2 Category', '')).lower()
    l3 = str(row.get('Level 3 Category', '')).lower()

    # --- PHASE 1: EXACT & HIGH PRIORITY MATCHES ---
    if 'netgear' in desc: return 'netgear_l1'
    if 'sir' in desc: return 'm-09_sir_approved'
    if 'rfi' in desc: return 'm-03_rfi'

    if 'dismantle' in desc or 'dismantlement' in desc or 'decommission' in desc:
        return 'm-08_dismantle'

    logistics_keywords = ['transport', 'logistic', 'delivery', 'cargo', 'truck', 
                          'pick up', 'trip', 'distance', 'mobilization']
    if any(k in desc for k in logistics_keywords):
        return 'sa-logistic(te)'

    doc_keywords = ['pac', 'bast', 'documentation', 'acceptance', 'handover', 
                    'aos-', 'project service', 'admin', 'management fee']
    if any(k in desc for k in doc_keywords):
        return 'm-12_pac_approved'

    # --- PHASE 2: HARD CATEGORY CHECKS ---
    if 'material' in l2:
        return 'm-04_mos'

    if 'rno' in l1 or 'optimization' in l1:
        return 'm-07_on_air'

    # --- PHASE 3: KEYWORD REFINEMENT ---
    if any(k in desc for k in ['survey', 'drawing', 'boq', 'design', 'as plan', 'as built']):
        return 'm-01_site_survey'
    if 'visit' in desc: 
        return 'sa-site_visit(te)'

    if 'atp' in desc:
        if 'cme' in desc or 'cme' in l3: return 'm-03a_atp_cme'
        if 'pln' in desc: return 'm-03b_atp_pln'
        return 'm-10_atp_approved'
    if any(k in desc for k in ['qc', 'quality', 'assessment', 'audit']):
        return 'm-05a_sv_qc'

    if any(k in desc for k in ['trouble', 'maintenance', 'helpdesk', 'repair', 'corrective']):
        return 'm-06a_troubleshooting'

    on_air_keywords = ['optimization', 'performance', 'dt ', 'drive test', 'oss', 
                       'tuning', 'analysis', 'complain', 'verification', 'npx']
    if any(k in desc for k in on_air_keywords):
        return 'm-07_on_air'
    if 'integration' in desc:
        return 'm-06_integrated'

    mos_keywords = ['pipe', 'cable', 'pole', 'panel', 'rectifier', 'battery', 'conduit', 
                    'connector', 'jumper', 'splitter', 'attenuator', 'accessories', 
                    'clamp', 'bolt', 'nut', 'module', 'unit', 'rack', 'cabinet', 'concrete']
    if any(k in desc for k in mos_keywords):
        return 'm-04_mos'

    if any(k in desc for k in ['construct', 'drilling', 'hole', 'wall', 'civil', 'foundation']):
        return 'm-03a_atp_cme'

    install_keywords = ['installation', 'install', 'mounting', 'fiber', 'fusion', 
                        'splicing', 'cabling', 'laying', 'codeploy', 'mw 0.9', 'mw 1.2']
    if any(k in desc for k in install_keywords):
        return 'm-05_installation-completed'
    
    if 'installation' in l1 or 'ibc' in l1:
        return 'm-05_installation-completed'

    # --- PHASE 4: MANPOWER & INCENTIVES ---
    if any(k in desc for k in ['supervisor', 'spv', 'rigger', 'manpower', 'team']):
        return 'sa-site_spv'

    if any(k in desc for k in ['incentive', 'allowance', 'bonus']):
        return 'sa-productivity_incentive'

    return 'sa-productivity_incentive'

# ==========================================
# 2. MAIN PROCESSING WRAPPER
# ==========================================

@st.cache_data
def process_dataframe(df, col_name):
    # Create copies to avoid SettingWithCopy warnings
    processed = df.copy()
    
    # 1. Clean Text for L1, L3, L5
    processed['item_desc_clean'] = processed[col_name].apply(clean_text)
    
    # 2. Clean Text for L2, L4
    processed['item_desc_clean_L2'] = processed[col_name].apply(clean_text_2)
    
    # 3. Apply Basic Rules
    processed['Level 1 Service Type'] = processed['item_desc_clean'].apply(get_categorization_L1)
    processed['Level 2 Category'] = processed['item_desc_clean_L2'].apply(get_categorization_L2)
    processed['Level 3 Category'] = processed['item_desc_clean'].apply(get_categorization_L3)
    processed['Level 4 Unit'] = processed['item_desc_clean_L2'].apply(get_categorization_L4)
    processed['Level 5 Deployment Type'] = processed['item_desc_clean'].apply(get_categorization_L5)
    
    # 4. Apply NEW Refined Milestone Rule
    # Ensure the column 'Item Description' exists for the function to read, 
    # regardless of what the user selected in the dropdown.
    processed['Item Description'] = processed[col_name]
    
    # Apply row-by-row (axis=1) because the function checks L1/L2/L3 as well
    processed['Milestone'] = processed.apply(categorize_item_refined, axis=1)

    return processed

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Result')
    return output.getvalue()

# ==========================================
# 3. STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Item Categorizer (L1-Refined)", layout="wide")

st.title("📂 Item Description Auto-Categorizer")
st.markdown("""
This tool automates the categorization of item descriptions into:
* **Levels 1-5** (Service Type, Category, Equipment, Unit, Deployment)
* **Milestone** (Specific Activity Code mapping)
""")

# --- Sidebar ---
st.sidebar.header("Configuration")
uploaded_file = st.sidebar.file_uploader("Upload your file", type=['csv', 'xlsx'])

# --- Main Area ---
if uploaded_file is not None:
    try:
        # Load Data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"File loaded successfully! ({len(df)} rows)")
        
        # Column Selection
        st.subheader("1. Select Column")
        cols = df.columns.tolist()
        
        # Try to auto-select "Item Description" if it exists
        default_idx = cols.index("Item Description") if "Item Description" in cols else 0
        target_col = st.selectbox("Select the column containing Item Descriptions:", cols, index=default_idx)
        
        # Process Button
        if st.button("Run Categorization"):
            with st.spinner('Processing rules L1 through Milestone...'):
                result_df = process_dataframe(df, target_col)
                
            st.subheader("2. Preview Results")
            st.dataframe(result_df.head(50))
            
            # Statistics
            st.subheader("3. Quick Stats")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Level 1 Service Type**")
                st.write(result_df['Level 1 Service Type'].value_counts())
            with col2:
                st.write("**Level 2 Category**")
                st.write(result_df['Level 2 Category'].value_counts())
            with col3:
                st.write("**Level 3 Category**")
                st.write(result_df['Level 3 Category'].value_counts())
            with col4:
                st.write("**Level 4 Unit**")
                st.write(result_df['Level 4 Unit'].value_counts())
            with col5:
                st.write("**Level 5 Deployment Type**")
                st.write(result_df['Level 5 Deployment Type'].value_counts())
            with col6:
                st.write("**Milestone**")
                st.write(result_df['Milestone'].value_counts())

            # Download Section
            st.subheader("4. Download Data")
            
            col_d1, col_d2 = st.columns(2)
            
            # CSV Download
            csv_data = convert_df_to_csv(result_df)
            col_d1.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name='Categorized_Items_Refined.csv',
                mime='text/csv',
            )
            
            # Excel Download
            excel_data = convert_df_to_excel(result_df)
            col_d2.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name='Categorized_Items_Refined.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            
    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("👈 Please upload a CSV or Excel file from the sidebar to begin.")
