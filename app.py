import streamlit as st
import pandas as pd
import re
import io

# ==========================================
# 1. LOGIC FUNCTIONS (Extracted from Notebook)
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

def get_categorization_L1(item_desc_clean):
    text = str(item_desc_clean).lower()
    
    # 1. Specific User Overrides
    if "netgear re-tagging works on tower" in text: return 'Operation & Maintenance (MSS)'
    if "splicing and tracing core in existing closure" in text: return 'Operation & Maintenance (MSS)'
    if " ms " in text or text.startswith("ms ") or text.endswith(" ms"): return 'Operation & Maintenance (MSS)'
    if "rigger" in text: return 'Optimization & Network Management (RNO)'
    if "for new build" in text: return 'Installation-Test-Commissioning (TIN)'

    # 2. Inbuilding Coverage Services (IBC)
    if any(k in text for k in ['inbuilding', 'lampsite', 'ibs', 'das', 'small cell', 
                            'repeater', 'prru', 'rhub', 'indoor antenna']):
        return 'Inbuilding Coverage Services (IBC)'
        
    # 3. Optimization & Network Management (RNO)
    if any(k in text for k in ['optimization', 'optimize', 'drive test', 'walk test', 
                            'network performance', 'kpi', 'benchmark', 'npo', 'parameter', 
                            'tuning', 'measurement', 'ssv', 'rno', 'rf adjustment', 
                            'data collection', 'oss data', 'analysis', 'npi']):
        return 'Optimization & Network Management (RNO)'
    
    # 4. Survey (ENG)
    if any(k in text for k in ['survey', 'tssr', 'site audit', 'design', 'planning', 
                            'los', 'site hunt', 'sid', 'drawing', 'desgin', 'boq', 'tagging', 
                            'gps coordinate']):
        return 'Survey (ENG)'
    
    # 5. Operation & Maintenance (MSS)
    if any(k in text for k in ['maintenance', 'helpdesk', 'managed service', 'operation', 
                            'repair', 'spare part', 'fault', 'fuel', 'genset', 'cleaning', 
                            'rent', 'lease', 'bill', 'support', 'corrective', 'preventive', 
                            'ms fee', 'monitoring', 'assurance', 'keeper', 'freon', 
                            'refrigerant', 'rewinding', 'taskforce', 'site visit', 
                            'good part', 'handling adhoc', 'purifikasi', 'bushing', 
                            'contactor', 'oli', 'capacity allowance', 'seal', 'pressure suit']):
        return 'Operation & Maintenance (MSS)'
    
    # 6. Default Fallback (TIN)
    return 'Installation-Test-Commissioning (TIN)'

def get_categorization_L2(item_desc_clean_L2):
    text = str(item_desc_clean_L2).lower()
    
    # Priority 1: Material & Services (Combo items)
    if any(k in text for k in ["supply & install", "supply and install", "supply&install",
                            "provide & install", "provide and install", "supply & fix", 
                            "supply and fix", "including wiring", "include wiring"]):
        return "Material & Services"
    
    # Priority 2: Services Only (Action verbs and service tasks)
    service_keywords = [
        "installation", " install", "install ", "dismantle", "service", "survey", 
        "optimize", "optimization", "maintenance", "manpower", "team", "visit", 
        "test", "commissioning", "integration", "configuration", "audit", "design", 
        "training", "consultancy", "logistic", "transport", "mobilization", "incentive", 
        "return", "handling", "tagging", "splicing", "trench", "pulling", "roding", 
        "construct", "drilling", "rewinding", "unwelding", "drawing", "documentation", 
        "assurance", "monitoring", "analysis", "reporting", "tuning", "clearance", 
        "keeper", "helpdesk", "managed service", "support", "verification", "collection", 
        "induction", "registration", "rectification", "relocation", "replacement", 
        "replace", "swap", "expansion", "upgrade", "implementation", "migration", 
        "re-tagging", "trouble shooting", "cleaning", "rent", "lease", "bill", 
        "purifikasi", "moving", "codeploy", "co-deploy", "works", "work",
        "fusion", "los survey", "parameter", "adjustment", "rigger", "custimization",
        "customization", "supervision", "atp", "bastian", "bast", "acceptance",
        "compensation", "pick up", "fee", "allowance", "permit", "po for",
        "document", "welding", "taskforce", "checking", "check", "oss", "walk test", 
        "wt&oss", "pre-modernization", "modernization", "laying", "termination", 
        "rearrangement", "pm package"
    ]
    if any(k in text for k in service_keywords):
        return "Services Only"
    if text.startswith("new:") or text.startswith("new-") or text.startswith("new "):
        return "Services Only"
        
    # Priority 3: Material Supply (Default)
    return "Material Supply"

def get_categorization_L3(item_desc_clean):
    text = str(item_desc_clean).lower()
    
    # 1. Incentive (Highest Priority)
    if "incentive" in text or "points" in text: return "Incentive"

    # 2. Logistic
    if "logistic" in text or "return fault" in text or "good part" in text: return "Logistic"

    # 3. Outside Plant (OSP)
    if any(k in text for k in ["pulling", "trench", "cable", "otb"]): return "Outside Plant (OSP)"

    # 4. Power System
    if any(k in text for k in ["power", "rectifier", "battery", "genset", "generator", 
                            "ups", "inverter", "kwh", "mcb", "transformer", 
                            "ac power", "dc power", "lv ", "hv ", "breaker", "busbar"]):
        return "Power System"

    # 5. Radio Access Network (RAN)
    if any(k in text for k in ["ran", "radio", "bts", "nodeb", "enodeb", "gnodeb", 
                            "sran", "base station", "rru", "aau", "bbu", "rfu", "trx", 
                            "sector", "cell ", "cell-", "multi-sector", "antenna", 
                            "feeder", "jumper", "cpri", "tma", "combiner", "diplexer", 
                            "triplexer", "filter", "4g", "5g", "lte", "gul", "gsm", 
                            "umts", "nr ", "nsa", " sa ", "drive test", "walk test", 
                            "dt ", "ssv", "sso", "npi", "rno", "rf adjustment", 
                            "parameter", "optimization", "tuning", "network performance", 
                            "kpi", "rigger", "inbuilding", "ibs", "das", "lampsite", 
                            "small cell", "repeater", "prru", "rhub", "mocn", "roaming", 
                            "neighbor", "blind spot", "coverage", "distribution aerial", 
                            "feeder aerial", "service operation center", "remote radio unit"]):
        return "Radio Access Network (RAN)"

    # 6. Transmission (TRM)
    if any(k in text for k in ["microwave", " mw ", " mw-", "-mw", "odu", "idu", 
                            "transmission", "trm", "backhaul", "per hop", "optical", 
                            "fiber", "fibre", " fo ", "ftth", "fbb", "osp", "isp", 
                            "olt", "ont", "gpon", "wdm", "mstp", "sdh", "dwdm", 
                            "otn", "ptn", "datacomm", "router", "switch", "ip ne", 
                            "ip_ne", "peering", "splicing", "roding", "duct", "aerial", 
                            "underground", "odf", "patch cord", "fat ", "fdt ", "closure",
                            "lan ", "cat 6", "cat6", "metro", "ethernet", "access,olt",
                            "access,blade", "access,rack", "wdm/mstp"]):
        return "Transmission (TRM)"

    # 7. Core Network (CORE)
    if any(k in text for k in ["core network", " msc", " hlr", " hss", " epc", " mme", 
                            " sgsn", " ggsn", " ims", " volte", "cs core", "ps core", 
                            "packet core", "udm", "ausf", "amf", "smf", "upf", "pcrf", 
                            "dra", "stp", "sbc", "mgw", "softswitch", "media gateway", 
                            "signaling", "user plane", "control plane", "charging system", 
                            "ocs", "pcc", "cs helpdesk", "core site"]):
        return "Core Network (CORE)"

    # 8. Supporting Facility (CME)
    if any(k in text for k in ["cme", "ac ", "dc ", "air conditioner", "conditioning", 
                            "pac ", "split ac", "cooling", "cabinet", "shelter", 
                            "enclosure", "rack", "cage", "pole", "tower", "monopole", 
                            "guyed", "civil", "grounding", "lightning", "arrester", 
                            "protection", "fuel", "tank", "sensor", "mechanical", 
                            "electrical", "concrete", "foundation", "fence", "tray", 
                            "ladder", "bracket", "mounting", "clamp", "bolt", "nut", 
                            "anchor", "pipe", "conduit", "trunking", "seal", "cement", 
                            "sand", "gravel", "macadam", "renovation", "refurbishment", 
                            "cleaning", "site keeper", "security", "freon", "oil", 
                            "lubricant", "pump", "valve", "compressor", "bushing", 
                            "contactor", "mecanical", "pressure suit", "reinstatement", 
                            "welding", "drilling", "hole", "anti theft", "atd", "lug", 
                            "scun", "connector"]):
        return "Supporting Facility (CME)"
        
    # 9. General Support (Default)
    return "General Support"

def get_categorization_L4(item_desc_clean_L2):
    text = str(item_desc_clean_L2).lower()
    if "man-month" in text or "man month" in text or "*month" in text or " month" in text:
        return "Man-month"
    if "team" in text:
        return "Team"
    if "/site" in text or "per site" in text:
        return "Site"
    if "/hop" in text or "per hop" in text or " hop" in text:
        return "Hop"
    if "/each" in text or "pcs" in text or "per point" in text:
        return "Each"
    return "Each" # Default

def get_categorization_L5(item_desc_clean):
    text = str(item_desc_clean).lower()

    # 1. HARD EXCEPTION (Highest Priority)
    if "rectification and expansion" in text:
        return "Swap/Replacement"

    # 2. SUPPORT
    support_keywords = [
        'per point', 'allowance', 'incentive',
        'return fault', 'return good part', 'good part',
        'compensation', 'logistic from', 'self pick up', 'handling',
        'rigger', 'visit', 'document', 'coordinate', 'gps',
        'aos', 'project service', 
        'access registration', 'induction', 'team induction', 
        'restricted mining', 'special event', 'assurance', 
        'npi', 'taskforce'
    ]
    if any(k in text for k in support_keywords):
        return "Support"

    # 3. OPTIMIZATION & PERFORMANCE MANAGEMENT
    optimization_keywords = [
        'optimization', 'performance', 'tuning', 'audit', 'ssv', 'sso',
        'dt', 'drive test', 'npx', 'network performance', 'kpi', 'monitor',
        'collection', 'verification', 'adjustment', 'acceptance', 'benchmark',
        'parameters and neighboring cell', 'analysis and report',
        'quality management', 'neighboring cell scripts', 'without car',
        'walk test',
        'iro_ethernet configuration', 'iro_fbb common', 'iro_mw idu',
        'tsel_gul_rf_rigger', 'xl_gul_merge_rf_rigger',
        'xl_gul_rf_rigger', 'ioh_gul_rf_rigger', 'otdr', 'fiber quality', 
        'board testing', 'antenna checking', 'light indicator', 'idu', 'odu', 'bbu', 'rru',
    ]
    if any(k in text for k in optimization_keywords):
        return "Optimization & Performance Management"

    # 4. MAINTENANCE SERVICES
    maintenance_keywords = [
        'maintenance', 'trouble shooting', 'troubleshooting', 'repair',
        'corrective', 'preventive', 'spare part', 'spare', 'rectification',
        'fixing', 'warranty', 'helpdesk', 'support', 'ticket', 'complain',
        'service operation center', 'soc', 'alarm clearance', 'tagging',
        'reinstatement', 'site keeper', 'managed service',
        'shopping list package', 'shopping list',
        'refrigerant', 'refrigerant freon', 'refrigerant r22', 'refrigerant r407c',
        'pressure suit', 'purifikasi', 'rewinding', 'rewelding',
        'split ac', 'trench & backfill', 'xl ms lumpsum shopping list', 
        'cell down', 'p1', 'unwelding'
    ]
    if any(k in text for k in maintenance_keywords):
        return "Maintenance Services"

    # 5. SWAP / REPLACEMENT (GENERAL)
    swap_keywords = [
        'swap', 'replace', 'replacement', 'migration', 'modernization',
        'relocation', 're-arrangement', 'rearrange', 're-configuration'
    ]
    if any(k in text for k in swap_keywords):
        return "Swap/Replacement"

    # 6. DISMANTLING
    dismantle_keywords = [
        'dismantle', 'dismantlement', 'removal', 'remove',
        'de-installation', 'return'
    ]
    if any(k in text for k in dismantle_keywords):
        return "Dismantling"

    # 7. ADDITIONAL / UPGRADE
    upgrade_keywords = [
        'expansion', 'upgrade', 'capacity', 'add-on',
        'augment', 'growth', 'extension', 'license'
    ]
    if any(k in text for k in upgrade_keywords):
        return "Additional/Upgrade"

    # 8. NEW DEPLOYMENT
    deployment_keywords = [
        'new', 'installation', 'install', 'commissioning', 'integration',
        'survey', 'deployment', 'rollout', 'implement', 'implementation',
        'setup', 'construct', 'civil work', 'supply', 'material',
        'pipe', 'cable', 'pole', 'bracket', 'connector', 'adapter',
        'feeder', 'clamp', 'cabinet', 'rack', 'power', 'battery',
        'concrete', 'conduit', 'splicing', 'fusion', 'device',
        'drawing', 'dummy load', 'contactor',
        'jumper', 'kabel', 'mcb', 'rod', 'bushing', 'seal',
        'ties', 'module', 'lamp', 'trafo', 'mechanical',
        'oli', 'otb', 'patch cord', 'pipa', 'pvc',
        'tape', 'rhub box', 'codeploy', 'insert'
    ]
    if any(k in text for k in deployment_keywords):
        return "New Deployment"

    # 9. FALLBACK
    return "Others"

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
    
    # 3. Apply Logic
    processed['Level 1 Service Type'] = processed['item_desc_clean'].apply(get_categorization_L1)
    processed['Level 2 Category'] = processed['item_desc_clean_L2'].apply(get_categorization_L2)
    processed['Level 3 Category'] = processed['item_desc_clean'].apply(get_categorization_L3)
    processed['Level 4 Unit'] = processed['item_desc_clean_L2'].apply(get_categorization_L4)
    processed['Level 5 Deployment Type'] = processed['item_desc_clean'].apply(get_categorization_L5)
    
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

st.set_page_config(page_title="Item Categorizer (L1-L5)", layout="wide")

st.title("📂 Item Description Auto-Categorizer")
st.markdown("""
This tool automates the categorization of item descriptions into **5 Levels** (Service Type, Category, Equipment, Unit, Deployment).
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
            with st.spinner('Processing rules L1 through L5...'):
                result_df = process_dataframe(df, target_col)
                
            st.subheader("2. Preview Results")
            st.dataframe(result_df.head(50))
            
            # Statistics
            st.subheader("3. Quick Stats")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Level 1 Distribution**")
                st.write(result_df['Level 1 Service Type'].value_counts())
            with col2:
                st.write("**Level 3 Distribution**")
                st.write(result_df['Level 3 Category'].value_counts())
            with col3:
                st.write("**Level 5 Distribution**")
                st.write(result_df['Level 5 Deployment Type'].value_counts())

            # Download Section
            st.subheader("4. Download Data")
            
            col_d1, col_d2 = st.columns(2)
            
            # CSV Download
            csv_data = convert_df_to_csv(result_df)
            col_d1.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name='Categorized_Items.csv',
                mime='text/csv',
            )
            
            # Excel Download
            excel_data = convert_df_to_excel(result_df)
            col_d2.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name='Categorized_Items.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            
    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("👈 Please upload a CSV or Excel file from the sidebar to begin.")
    st.markdown("### Expected Input Format")
    st.markdown("A file containing at least one column with item descriptions, e.g.:")
    st.dataframe(pd.DataFrame({
        "Item Description": [
            "1 HDPE pipe 20mm OD, 2mm WT",
            "1-3 AAU installation(not on tower)-/site",
            "TSEL service package 2025 JABO"
        ]
    }))