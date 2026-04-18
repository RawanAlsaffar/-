import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title='حوادث الأسطول | Q1 2026',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='expanded',
)

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / 'fleet_accidents_q1_2026_clean.csv'
MONTH_ORDER = ['يناير', 'فبراير', 'مارس']
DAY_ORDER = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
PERIOD_ORDER = ['فجر/ليل', 'صباح', 'ظهيرة/عصر', 'مساء']
SEQ = ['#F59E0B', '#38BDF8', '#A78BFA', '#34D399', '#FB7185', '#F97316', '#22C55E', '#60A5FA']
BG = '#0B1220'
CARD = '#111827'
CARD_2 = '#172033'
GRID = '#223047'
TEXT = '#E5EEF8'
MUTED = '#94A3B8'
BORDER = 'rgba(148,163,184,0.15)'
LOGO_CANDIDATES = [
    BASE / 'SRCAlogo_local_cmyk.jpg',
    Path(r'D:\fleet_q1_analysis_advanced_package_v2\home\ubuntu\fleet_q1_analysis\SRCAlogo_local_cmyk.jpg'),
]

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #09111f 0%, #0b1220 100%);
        color: #e5eef8;
    }
    .main .block-container {
        padding-top: 1.1rem;
        padding-bottom: 5rem;
        max-width: 98rem;
        direction: rtl;
    }
    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid rgba(148,163,184,0.12);
        border-left: none;
        left: 0;
    }
    [data-testid="stSidebarContent"], [data-testid="stSidebar"] * {
        color: #e5eef8;
        direction: rtl;
        text-align: right;
    }
    .top-brand {
        background: linear-gradient(135deg, rgba(17,24,39,0.96), rgba(15,23,42,0.94));
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 22px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 18px;
        justify-content: space-between;
        flex-direction: row-reverse;
    }
    .brand-title h1 {
        margin: 0;
        font-size: 1.95rem;
        color: #f8fafc;
    }
    .brand-title p {
        margin: 0.45rem 0 0 0;
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 1rem;
    }
    .brand-logo-box {
        min-width: 136px;
        text-align: left;
    }
    .brand-logo-fallback {
        background: rgba(56,189,248,0.08);
        border: 1px dashed rgba(148,163,184,0.22);
        border-radius: 14px;
        padding: 14px 16px;
        color: #9fb0c3;
        font-size: 0.88rem;
    }
    .hero {
        background: linear-gradient(135deg, rgba(245,158,11,0.18), rgba(56,189,248,0.14));
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 22px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }
    .hero h2 {
        margin: 0;
        font-size: 1.8rem;
        color: #f8fafc;
    }
    .hero p {
        margin: 0.45rem 0 0 0;
        color: #cbd5e1;
        line-height: 1.8;
    }
    .subtle {color: #93a4b8; font-size: 0.95rem;}
    .kpi-block {margin-bottom: 1rem;}
    .kpi-card {
        background: linear-gradient(180deg, rgba(17,24,39,0.95), rgba(15,23,42,0.96));
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 138px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    }
    .kpi-label {font-size: 0.94rem; color: #9fb0c3; margin-bottom: 0.45rem;}
    .kpi-value {font-size: 1.92rem; font-weight: 800; color: #f8fafc; line-height: 1.18;}
    .kpi-note {font-size: 0.88rem; color: #8dd3ff; margin-top: 0.65rem; line-height: 1.6;}
    .section-box {
        background: linear-gradient(180deg, rgba(17,24,39,0.92), rgba(17,24,39,0.82));
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 20px;
        padding: 18px 18px 8px 18px;
        margin-bottom: 14px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.12);
    }
    .section-title {
        font-size: 1.08rem;
        color: #f8fafc;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }
    .insight-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.92), rgba(15,23,42,0.96));
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 16px;
        padding: 16px 18px;
        min-height: 124px;
        margin-bottom: 0.8rem;
    }
    .insight-card .title {font-size: 0.9rem; color: #8dd3ff; margin-bottom: 0.45rem;}
    .insight-card .body {font-size: 0.98rem; color: #e5eef8; line-height: 1.8;}
    .small-chip {
        display: inline-block;
        padding: 0.24rem 0.55rem;
        background: rgba(56,189,248,0.12);
        border: 1px solid rgba(56,189,248,0.18);
        color: #bfe6ff;
        border-radius: 999px;
        margin-left: 0.35rem;
        margin-top: 0.4rem;
        font-size: 0.82rem;
    }
    .tab-intro {
        margin: 0.15rem 0 1rem 0;
        color: #9fb0c3;
        font-size: 0.95rem;
    }
    .footer-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(9,17,31,0.95);
        border-top: 1px solid rgba(148,163,184,0.14);
        color: #cbd5e1;
        text-align: center;
        padding: 0.7rem 1rem;
        z-index: 999;
        font-size: 0.92rem;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: #111827;
        color: #dbe7f3;
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,0.12);
        padding: 0.55rem 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(245,158,11,0.16), rgba(56,189,248,0.18));
        color: white;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 16px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    replacements = {
        'أثناء.التوجه.للبلاغ': 'أثناء التوجه للبلاغ',
        'أثناء.نقل.الحالة': 'أثناء نقل الحالة',
        'أثناءالمباشرة': 'أثناء المباشرة',
        'اثناء نقل الحاله': 'أثناء نقل الحالة',
        'بدون.بلاغ': 'بدون بلاغ',
        'لايوجد بلاغ': 'لا يوجد بلاغ',
        'لايوجد.بلاغ': 'لا يوجد بلاغ',
        'لاينطبق': 'لا ينطبق',
        'لايوجد': 'لا يوجد',
        'حادث.مركبة.إسعافية': 'حادث مركبة إسعافية',
        'مركبةاسعاف': 'مركبة إسعاف',
        'مركزاسعافي': 'مركز إسعافي',
        'المدينةالمنورة': 'المدينة المنورة',
        'مكةالمكرمة': 'مكة المكرمة',
    }
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace('\xa0', ' ', regex=False).str.strip()
            df[col] = df[col].replace({'nan': np.nan, 'NaT': np.nan, 'None': np.nan})
            df[col] = df[col].replace(replacements)
    text_cleanup_cols = ['المركبات/ مرحلة الرحلة الإسعافية', 'حالة المورد بعد الحدث', 'نوع المورد', 'نوع الحدث / الفشل', 'المنطقة', 'المدينة', 'نوع البلاغ']
    for col in text_cleanup_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace('.', ' ', regex=False)
                .str.replace(r'\s+', ' ', regex=True)
                .str.strip()
                .replace({'nan': np.nan, 'NaT': np.nan, 'None': np.nan})
            )
    if 'التاريخ' in df.columns:
        df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
    bool_map = {'true': True, 'false': False, True: True, False: False}
    for col in ['حادث_بإصابات', 'المورد_خارج_الخدمة', 'المورد_يعمل_بعد_الحدث', 'توثيق_داعم_متوفر', 'تم_تفعيل_قيادة_الحدث', 'تم_ربط_حزام_الأمان']:
        if col in df.columns:
            df[col] = df[col].map(bool_map).fillna(df[col])
    num_cols = [
        'إجمالي_الإصابات', 'عدد الإصابات الناتجة عن الحادث', 'نسبة الخطأ  على الإسعاف', 'نسبة الخطأ  على الطرف الآخر',
        'مدة الحدث حساب تلقائي_بالدقائق', 'زمن الإستجابة_بالدقائق', 'نسبة اكتمال ارصد', 'الموديل'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'إجمالي_الإصابات' not in df.columns and 'عدد الإصابات الناتجة عن الحادث' in df.columns:
        df['إجمالي_الإصابات'] = pd.to_numeric(df['عدد الإصابات الناتجة عن الحادث'], errors='coerce').fillna(0)
    if 'حادث_بإصابات' not in df.columns:
        df['حادث_بإصابات'] = df['إجمالي_الإصابات'].fillna(0) > 0
    if 'المورد_خارج_الخدمة' not in df.columns:
        df['المورد_خارج_الخدمة'] = df['حالة المورد بعد الحدث'].fillna('').astype(str).str.contains('لا يعمل')
    if 'المركبات/ مرحلة الرحلة الإسعافية' in df.columns:
        df['مرحلة_تحليلية'] = df['المركبات/ مرحلة الرحلة الإسعافية'].replace({
            'لا يوجد بلاغ': 'غير تشغيلي/غير محدد',
            'لايوجد بلاغ': 'غير تشغيلي/غير محدد',
            'لايوجد.بلاغ': 'غير تشغيلي/غير محدد',
            'بدون بلاغ': 'غير تشغيلي/غير محدد',
            'بدون.بلاغ': 'غير تشغيلي/غير محدد',
            'لا ينطبق': 'غير تشغيلي/غير محدد',
            'لاينطبق': 'غير تشغيلي/غير محدد',
        })
    if 'الشهر' in df.columns:
        df['الشهر'] = pd.Categorical(df['الشهر'], categories=MONTH_ORDER, ordered=True)
    if 'اسم_اليوم' in df.columns:
        df['اسم_اليوم'] = pd.Categorical(df['اسم_اليوم'], categories=DAY_ORDER, ordered=True)
    if 'فترة_اليوم' in df.columns:
        df['فترة_اليوم'] = pd.Categorical(df['فترة_اليوم'], categories=PERIOD_ORDER, ordered=True)
    return df


@st.cache_data
def get_logo_path() -> str | None:
    for candidate in LOGO_CANDIDATES:
        try:
            if Path(candidate).exists():
                return str(candidate)
        except Exception:
            continue
    return None


def fig_layout(fig, title, height=390, legend=True):
    fig.update_layout(
        title=title,
        title_x=0.02,
        height=height,
        paper_bgcolor=BG,
        plot_bgcolor=CARD,
        font=dict(family='Arial', color=TEXT, size=13),
        margin=dict(l=25, r=25, t=58, b=25),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, x=0,
            bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT)
        ) if legend else None,
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, showline=False),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, showline=False),
    )
    return fig


def card(label: str, value: str, note: str = ''):
    st.markdown(
        f"""
        <div class='kpi-block'>
            <div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{value}</div>
                <div class='kpi-note'>{note}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(title: str, body: str):
    st.markdown(
        f"""
        <div class='insight-card'>
            <div class='title'>{title}</div>
            <div class='body'>{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_caption(text: str):
    st.markdown(f"<div class='tab-intro'>{text}</div>", unsafe_allow_html=True)


def all_multiselect(label: str, options, default_all=True, key='x'):
    options = [o for o in options if pd.notna(o)]
    options = list(dict.fromkeys(options))
    all_token = 'الكل'
    default = [all_token] if default_all else []
    selected = st.sidebar.multiselect(label, [all_token] + options, default=default, key=key)
    if all_token in selected or not selected:
        return options
    return selected


def download_excel(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()


def fmt_num(x, digits=1, suffix=''):
    if pd.isna(x):
        return 'غير متاح'
    if digits == 0:
        return f"{int(round(float(x))):,}{suffix}"
    return f"{float(x):,.{digits}f}{suffix}"


def make_heatmap(data: pd.DataFrame):
    heat = data.dropna(subset=['اسم_اليوم', 'فترة_اليوم']).groupby(['اسم_اليوم', 'فترة_اليوم'], as_index=False).size()
    pivot = heat.pivot(index='اسم_اليوم', columns='فترة_اليوم', values='size').reindex(index=DAY_ORDER, columns=PERIOD_ORDER)
    fig = px.imshow(
        pivot,
        text_auto=True,
        color_continuous_scale=['#102033', '#163754', '#1d5f87', '#f59e0b'],
        aspect='auto',
        labels={'x': 'فترة اليوم', 'y': 'اليوم', 'color': 'الحوادث'},
    )
    return fig_layout(fig, 'اليوم × فترة اليوم', height=430, legend=False)


def make_empty_warning():
    st.warning('لا توجد بيانات مطابقة للفلاتر الحالية. جرّب توسيع النطاق أو اختيار "الكل" في أحد الفلاتر.')
    st.stop()


df = load_data(DATA_PATH)

def render_brand_header():
    logo_path = get_logo_path()
    if logo_path:
        logo_col, text_col = st.columns([1.1, 5], gap='large')
        with logo_col:
            st.image(logo_path, use_container_width=True)
        with text_col:
            st.markdown(
                """
                <div class='top-brand'>
                    <div class='brand-title'>
                        <h1>لوحة حوادث الأسطول</h1>
                        <p>ملخص حوادث الأسطول - الربع الأول 2026: نظرة شاملة على أماكن وأوقات الحوادث، ومدى تأثيرها على سير العمل</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class='top-brand'>
                <div class='brand-wrap'>
                    <div class='brand-title'>
                        <h1>لوحة حوادث الأسطول</h1>
                        <p>ملخص حوادث الأسطول - الربع الأول 2026: نظرة شاملة على أماكن وأوقات الحوادث، ومدى تأثيرها على سير العمل</p>
                    </div>
                    <div class='brand-logo-box'>
                        <div class='brand-logo-fallback'>
                            سيتم عرض شعار الهيئة تلقائياً عند توفر الملف داخل مجلد المشروع أو على المسار المحلي المحدد.
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.sidebar.markdown('## فلاتر ')
st.sidebar.caption('----------------------------------') 

regions = sorted(df['المنطقة'].dropna().unique())
selected_regions = all_multiselect('المنطقة', regions, key='regions')
filtered = df[df['المنطقة'].isin(selected_regions)].copy()

cities = sorted(filtered['المدينة'].dropna().unique())
selected_cities = all_multiselect('المدينة', cities, key='cities')
filtered = filtered[filtered['المدينة'].isin(selected_cities)].copy()

months = [m for m in MONTH_ORDER if m in filtered['الشهر'].astype(str).unique()]
selected_months = all_multiselect('الشهر', months, key='months')
filtered = filtered[filtered['الشهر'].astype(str).isin(selected_months)].copy()

stages = sorted(filtered['المركبات/ مرحلة الرحلة الإسعافية'].dropna().unique())
selected_stages = all_multiselect('مرحلة الرحلة', stages, key='stages')
filtered = filtered[filtered['المركبات/ مرحلة الرحلة الإسعافية'].isin(selected_stages)].copy()

status_options = sorted(filtered['حالة المورد بعد الحدث'].dropna().unique())
selected_status = all_multiselect('وضع المورد بعد الحادث', status_options, key='status')
filtered = filtered[filtered['حالة المورد بعد الحدث'].isin(selected_status)].copy()

injury_only = st.sidebar.toggle('فقط حوادث بإصابات', value=False)
if injury_only:
    filtered = filtered[filtered['حادث_بإصابات'].fillna(False).astype(bool)].copy()

out_service_only = st.sidebar.toggle('فقط خروج من الخدمة', value=False)
if out_service_only:
    filtered = filtered[filtered['المورد_خارج_الخدمة'].fillna(False).astype(bool)].copy()

st.sidebar.markdown('---')
st.sidebar.caption(f'السجلات الحالية: **{len(filtered)}** من أصل **{len(df)}**')

if filtered.empty:
    make_empty_warning()

incidents = len(filtered)
regions_n = filtered['المنطقة'].nunique()
cities_n = filtered['المدينة'].nunique()
injured_incidents = int(filtered['حادث_بإصابات'].fillna(False).astype(bool).sum())
out_of_service = int(filtered['المورد_خارج_الخدمة'].fillna(False).astype(bool).sum())
total_injuries = int(pd.to_numeric(filtered['إجمالي_الإصابات'], errors='coerce').fillna(0).sum())
avg_duration = pd.to_numeric(filtered['مدة الحدث حساب تلقائي_بالدقائق'], errors='coerce').mean()
avg_response = pd.to_numeric(filtered['زمن الإستجابة_بالدقائق'], errors='coerce').mean()
doc_rate = pd.to_numeric(filtered['نسبة اكتمال ارصد'], errors='coerce').mean() * 100 if 'نسبة اكتمال ارصد' in filtered.columns else np.nan

region_counts = filtered['المنطقة'].value_counts()
city_counts = filtered['المدينة'].value_counts()
stage_counts = filtered['المركبات/ مرحلة الرحلة الإسعافية'].value_counts()
analysis_stage_counts = filtered['مرحلة_تحليلية'].value_counts() if 'مرحلة_تحليلية' in filtered.columns else stage_counts
if len(analysis_stage_counts):
    operational_stage_counts = analysis_stage_counts[[('غير تشغيلي' not in str(idx)) for idx in analysis_stage_counts.index]]
else:
    operational_stage_counts = analysis_stage_counts
month_counts = filtered['الشهر'].astype(str).value_counts()
stage_top_display = operational_stage_counts.index[0] if len(operational_stage_counts) else (analysis_stage_counts.index[0] if len(analysis_stage_counts) else 'غير متاح')

render_brand_header()

hero_scope = ' | '.join([
    f"<span class='small-chip'>المناطق: {regions_n}</span>",
    f"<span class='small-chip'>المدن: {cities_n}</span>",
    f"<span class='small-chip'>السجلات المعروضة: {incidents}</span>",
])

st.markdown(
    f"""
    <div class='hero'>
        <h2>نظرة عامة</h2>
        <p>حسابات البيانات</p>
        <div style='margin-top:0.9rem'>{hero_scope}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

r1 = st.columns(5, gap='large')
with r1[0]:
    card('الحوادث', fmt_num(incidents, 0), f'أعلى منطقة: {region_counts.idxmax()}')
with r1[1]:
    card('الإصابات', fmt_num(total_injuries, 0), f'حوادث بإصابات: {injured_incidents}')
with r1[2]:
    card('الخروج من الخدمة', fmt_num(out_of_service, 0), 'أثر مباشر على الجاهزية')
with r1[3]:
    card('متوسط المدة', fmt_num(avg_duration, 1, ' د'), 'من بداية الحدث حتى الإغلاق')
with r1[4]:
    card('متوسط الاستجابة', fmt_num(avg_response, 1, ' د'), 'من البلاغ حتى الوصول')

r2 = st.columns(4, gap='large')
with r2[0]:
    card('المناطق', fmt_num(regions_n, 0), 'النطاق الجغرافي الحالي')
with r2[1]:
    card('المدن', fmt_num(cities_n, 0), 'الانتشار داخل النطاق')
with r2[2]:
    card('اكتمال الرصد', fmt_num(doc_rate, 1, '%'), 'يعكس اكتمال التوثيق')
with r2[3]:
    card('المرحلة الأعلى', stage_top_display, 'أعلى مرحلة تشغيلية من حيث الحوادث')

st.markdown('<div style="height:0.35rem"></div>', unsafe_allow_html=True)

st.download_button(
    'تنزيل البيانات المفلترة',
    data=download_excel(filtered),
    file_name='fleet_accidents_filtered_advanced.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)

ins_cols = st.columns(3, gap='large')
with ins_cols[0]:
    insight('أعلى تمركز جغرافي', f"تتصدر <b>{region_counts.idxmax()}</b> المشهد الحالي بعدد <b>{int(region_counts.max())}</b> حادثة، بينما تأتي <b>{city_counts.idxmax()}</b> كأعلى مدينة ضمن الفلاتر النشطة")
with ins_cols[1]:
    insight('النقطة التشغيلية الحساسة', f"المرحلة الأكثر تعرضاً هي <b>{stage_top_display}</b>، ما يشير إلى ضرورة رفع الضبط الوقائي خلال هذه المرحلة بالذات")
with ins_cols[2]:
    top_month = month_counts.index[0] if len(month_counts) else 'غير متاح'
    insight('الإيقاع الزمني', f"أعلى شهر ضمن النطاق الحالي هو <b>{top_month}</b>، مع متوسط مدة حدث يبلغ <b>{fmt_num(avg_duration, 1, ' دقيقة')}</b> ومتوسط استجابة <b>{fmt_num(avg_response, 1, ' دقيقة')}</b>.")

monthly = filtered.groupby(['الشهر_رقم', 'الشهر'], as_index=False).size().sort_values('الشهر_رقم')
region = filtered.groupby('المنطقة', as_index=False).size().sort_values('size', ascending=False)
city = filtered.groupby('المدينة', as_index=False).size().sort_values('size', ascending=False).head(10)
stage = filtered.groupby('مرحلة_تحليلية', as_index=False).size().sort_values('size', ascending=False) if 'مرحلة_تحليلية' in filtered.columns else filtered.groupby('المركبات/ مرحلة الرحلة الإسعافية', as_index=False).size().sort_values('size', ascending=False)
fault = filtered.groupby('جهة_الخطأ', as_index=False).size().sort_values('size', ascending=False)
status = filtered.groupby('حالة المورد بعد الحدث', as_index=False).size().sort_values('size', ascending=False)
duration_region = filtered.groupby('المنطقة', as_index=False)['مدة الحدث حساب تلقائي_بالدقائق'].mean().sort_values('مدة الحدث حساب تلقائي_بالدقائق', ascending=False)
response_region = filtered.dropna(subset=['زمن الإستجابة_بالدقائق']).groupby('المنطقة', as_index=False)['زمن الإستجابة_بالدقائق'].mean().sort_values('زمن الإستجابة_بالدقائق', ascending=False)
impact_region = filtered.groupby('المنطقة', as_index=False).agg(
    الحوادث=('معرف_الحدث', 'count'),
    الإصابات=('إجمالي_الإصابات', 'sum'),
    خروج_من_الخدمة=('المورد_خارج_الخدمة', 'sum')
)
impact_region['معدل_الإصابات'] = (impact_region['الإصابات'] / impact_region['الحوادث']).round(2)
impact_region['معدل_الخروج'] = (impact_region['خروج_من_الخدمة'] / impact_region['الحوادث']).round(2)

injuries_region = filtered.groupby('المنطقة', as_index=False)['إجمالي_الإصابات'].sum().sort_values('إجمالي_الإصابات', ascending=False)
case_types = filtered.groupby('نوع البلاغ', as_index=False).size().sort_values('size', ascending=False).head(8)
model_data = filtered.dropna(subset=['الموديل']).copy()
if not model_data.empty:
    model_data['الموديل'] = model_data['الموديل'].round(0).astype('Int64').astype(str)
    model_dist = model_data.groupby('الموديل', as_index=False).size().sort_values('size', ascending=False).head(12)
else:
    model_dist = pd.DataFrame({'الموديل': [], 'size': []})

doc_cols = ['تشييك المركبة اليومي', 'الفحص الدوري', 'ربط حزام الأمان', 'تقرير للحادث مرور / نجم', 'يوجد وثيقة  داعمة', 'تفعيل قيادة الحدث', 'خطة استمرارية الأعمال']
doc_records = []
for col in doc_cols:
    if col in filtered.columns:
        counts = filtered[col].fillna('غير معروف').value_counts()
        total = counts.sum()
        yes = counts.get('نعم', 0)
        no = counts.get('لا', 0)
        doc_records.append({'المؤشر': col, 'نعم': yes, 'لا': no, 'أخرى': total - yes - no, 'نسبة_نعم': round(yes / total * 100, 1) if total else 0})
doc_df = pd.DataFrame(doc_records)
doc_long = doc_df.melt(id_vars='المؤشر', value_vars=['نعم', 'لا', 'أخرى'], var_name='الحالة', value_name='العدد') if not doc_df.empty else pd.DataFrame(columns=['المؤشر', 'الحالة', 'العدد'])

monthly_data = filtered.groupby('الشهر').size().reset_index(name='العدد')
fig_month = px.line(monthly_data, x='الشهر', y='العدد', text='العدد', markers=True, color_discrete_sequence=[SEQ[1]])
fig_layout(fig_month, 'الاتجاه الشهري للحوادث', height=380)
fig_month.update_traces(textposition='top center', line_width=4, marker_size=10)

fig_region = px.bar(region, x='المنطقة', y='size', text='size', color='size', color_continuous_scale=['#164e63', '#0ea5e9', '#f59e0b'])
fig_layout(fig_region, 'توزيع الحوادث حسب المنطقة', height=360)

fig_city = px.bar(city.sort_values('size'), x='size', y='المدينة', orientation='h', text='size', color='size', color_continuous_scale=['#1d4ed8', '#38bdf8', '#a78bfa'])
fig_layout(fig_city, 'أعلى المدن من حيث عدد الحوادث', height=420)

stage_name_col = 'مرحلة_تحليلية' if 'مرحلة_تحليلية' in stage.columns else 'المركبات/ مرحلة الرحلة الإسعافية'
fig_stage = px.pie(stage, names=stage_name_col, values='size', hole=0.6, color_discrete_sequence=SEQ)
fig_layout(fig_stage, 'الحوادث حسب المرحلة التشغيلية', height=420)

fig_status = px.bar(status, x='حالة المورد بعد الحدث', y='size', text='size', color='حالة المورد بعد الحدث', color_discrete_sequence=['#34d399', '#fb7185', '#60a5fa'])
fig_layout(fig_status, 'وضع المورد بعد الحادث', height=360)

fig_fault = px.bar(fault, x='جهة_الخطأ', y='size', text='size', color='جهة_الخطأ', color_discrete_sequence=['#f59e0b', '#38bdf8', '#a78bfa', '#34d399'])
fig_layout(fig_fault, 'ملكية الخطأ في الحوادث', height=360)

fig_duration = px.bar(duration_region, x='المنطقة', y='مدة الحدث حساب تلقائي_بالدقائق', text='مدة الحدث حساب تلقائي_بالدقائق', color='مدة الحدث حساب تلقائي_بالدقائق', color_continuous_scale=['#2d1b69', '#7c3aed', '#f59e0b'])
fig_layout(fig_duration, 'متوسط مدة الحدث حسب المنطقة', height=380)

fig_response = px.bar(response_region, x='المنطقة', y='زمن الإستجابة_بالدقائق', text='زمن الإستجابة_بالدقائق', color='زمن الإستجابة_بالدقائق', color_continuous_scale=['#0f172a', '#38bdf8', '#f59e0b'])
fig_layout(fig_response, 'متوسط زمن الاستجابة حسب المنطقة', height=380)

fault_ambulance = filtered.groupby('المنطقة')['نسبة الخطأ  على الإسعاف'].mean().reset_index()
fig_fault_amb = px.bar(fault_ambulance, x='المنطقة', y='نسبة الخطأ  على الإسعاف', 
                      title='متوسط نسبة المسؤولية (على الإسعاف) حسب المنطقة',
                      text_auto='.2f', color_discrete_sequence=['#FB7185'])
fig_layout(fig_fault_amb, '')

fault_other = filtered.groupby('المنطقة')['نسبة الخطأ  على الطرف الآخر'].mean().reset_index()
fig_fault_oth = px.bar(fault_other, x='المنطقة', y='نسبة الخطأ  على الطرف الآخر', 
                      title='متوسط نسبة المسؤولية (على الطرف الآخر) حسب المنطقة',
                      text_auto='.2f', color_discrete_sequence=['#34D399'])
fig_layout(fig_fault_oth, '')

fig_impact = px.scatter(
    impact_region,
    x='معدل_الخروج', y='معدل_الإصابات', size='الحوادث', color='المنطقة',
    text='المنطقة', color_discrete_sequence=SEQ,
)
fig_layout(fig_impact, 'خريطة الأثر التشغيلي حسب المنطقة', height=420)
fig_impact.update_traces(textposition='top center')
fig_impact.update_xaxes(title='معدل الخروج من الخدمة')
fig_impact.update_yaxes(title='معدل الإصابات')


fig_heat = make_heatmap(filtered)

if not doc_long.empty:
    fig_doc = px.bar(doc_long, x='المؤشر', y='العدد', color='الحالة', barmode='stack', color_discrete_sequence=['#34d399', '#fb7185', '#60a5fa'])
else:
    fig_doc = go.Figure()
fig_layout(fig_doc, 'جودة التوثيق والامتثال', height=460)

fig_case = px.bar(case_types.sort_values('size'), x='size', y='نوع البلاغ', orientation='h', text='size', color='size', color_continuous_scale=['#164e63', '#38bdf8', '#f59e0b'])
fig_layout(fig_case, 'أكثر البلاغات ارتباطاً بالحوادث', height=420)

fig_injuries = px.bar(injuries_region, x='المنطقة', y='إجمالي_الإصابات', text='إجمالي_الإصابات', color='إجمالي_الإصابات', color_continuous_scale=['#7f1d1d', '#ef4444', '#f59e0b'])
fig_layout(fig_injuries, 'الإصابات حسب المنطقة', height=380)

if not model_dist.empty:
    fig_model = px.bar(model_dist.sort_values('size'), x='size', y='الموديل', orientation='h', text='size', color='size', color_continuous_scale=['#0f172a', '#3b82f6', '#f59e0b'])
else:
    fig_model = go.Figure()
fig_layout(fig_model, 'الحوادث حسب موديل المركبة', height=430)

for fig in [fig_month, fig_region, fig_city, fig_stage, fig_status, fig_fault, fig_duration, fig_response, fig_impact, fig_heat, fig_doc, fig_case, fig_injuries, fig_model]:
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)

charts_library = [
    ('الاتجاه الشهري للحوادث', fig_month),
    ('توزيع الحوادث حسب المنطقة', fig_region),
    ('أعلى المدن', fig_city),
    ('الحوادث حسب المرحلة التشغيلية', fig_stage),
    ('وضع المورد بعد الحادث', fig_status),
    ('الإصابات حسب المنطقة', fig_injuries),
    ('ملكية الخطأ في الحوادث', fig_fault),
    ('متوسط مدة الحدث حسب المنطقة', fig_duration),
    ('متوسط زمن الاستجابة حسب المنطقة', fig_response),
    ('اليوم × فترة اليوم', fig_heat),
    ('جودة التوثيق والامتثال', fig_doc),
    ('أكثر البلاغات ارتباطاً بالحوادث', fig_case),
    ('الحوادث حسب موديل المركبة', fig_model),
    ('خريطة الأثر التشغيلي حسب المنطقة', fig_impact),
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['نظرة عامة', 'المناطق والزمن ', 'كفاءة الأسطول والجاهزية', 'جودة التقارير والجاهزية', 'البيانات', 'مكتبة الرسوم'])

with tab1:
    section_caption('ملخص مرئي سريع للمشهد العام، يشمل الاتجاه الشهري، التركز الجغرافي، أعلى المدن، والمرحلة التشغيلية الأكثر تعرضاً.')
    a, b = st.columns([1.05, 0.95], gap='large')
    with a:
        st.plotly_chart(fig_month, width='stretch', key='overview_month')
    with b:
        st.plotly_chart(fig_region, width='stretch', key='overview_region')
    c, d = st.columns([1.05, 0.95], gap='large')
    with c:
        st.plotly_chart(fig_city, width='stretch', key='overview_city')
    with d:
        st.plotly_chart(fig_stage, width='stretch', key='overview_stage')

with tab2:
    section_caption('تحليل الأوقات والأماكن: نكشف هنا متى وأين تتركز الحوادث، عشان نحدد الفترات والمواقع اللي تحتاج انتباه أكثر')
    a, b = st.columns(2, gap='large')
    with a:
        st.plotly_chart(fig_heat, width='stretch', key='geo_heat')
    with b:
        st.plotly_chart(fig_fault, width='stretch', key='geo_fault')
    c, d = st.columns(2, gap='large')
    with c:
        st.plotly_chart(fig_injuries, width='stretch', key='geo_injuries')
    with d:
        st.plotly_chart(fig_case, width='stretch', key='geo_case_types')

with tab3:
    section_caption('نتابع كيف أثرت الحوادث على سرعة استجابة الفرق، وكم عطلت السيارات عن الخدمة، عشان نعرف المناطق اللي تأثرت جاهزيتها أكثر من غيرها')
    a, b = st.columns(2, gap='large')
    with a:
        st.plotly_chart(fig_duration, width='stretch', key='ops_duration')
    with b:
        st.plotly_chart(fig_response, width='stretch', key='ops_response')
    c, d = st.columns([1.05, 0.95], gap='large')
    with c:
        st.plotly_chart(fig_status, width='stretch', key='ops_status')
    with d:
        st.plotly_chart(fig_impact, width='stretch', key='ops_impact')
    st.plotly_chart(fig_model, width='stretch', key='ops_model')

with tab4:
    section_caption('مراجعة لمدى اكتمال بيانات الحوادث، مثل توفر التقارير الرسمية (نجم/المرور) والتأكد من توثيق إجراءات السلامة مثل ربط الحزام وفحص المركبة')
    st.plotly_chart(fig_doc, width='stretch', key='quality_doc')
    quality_cols = st.columns(3, gap='large')
    valid_report_rate = round((filtered['تقرير للحادث مرور / نجم'].fillna('').eq('متوفر تقرير المرور').mean() * 100), 1) if 'تقرير للحادث مرور / نجم' in filtered.columns else np.nan
    seatbelt_rate = round((filtered['ربط حزام الأمان'].fillna('').eq('نعم').mean() * 100), 1) if 'ربط حزام الأمان' in filtered.columns else np.nan
    evidence_rate = round((filtered['يوجد وثيقة  داعمة'].fillna('').eq('نعم').mean() * 100), 1) if 'يوجد وثيقة  داعمة' in filtered.columns else np.nan
    with quality_cols[0]:
        card('توفر تقرير رسمي', fmt_num(valid_report_rate, 1, '%'), 'مرور أو نجم')
    with quality_cols[1]:
        card('ربط حزام الأمان', fmt_num(seatbelt_rate, 1, '%'), 'ضمن النطاق الحالي')
    with quality_cols[2]:
        card('وثيقة داعمة', fmt_num(evidence_rate, 1, '%'), 'يعزز موثوقية التوثيق')
    if not doc_df.empty:
        st.dataframe(
            doc_df[['المؤشر', 'نسبة_نعم', 'نعم', 'لا', 'أخرى']].sort_values('نسبة_نعم', ascending=False),
            width='stretch', hide_index=True,
            column_config={
                'نسبة_نعم': st.column_config.ProgressColumn('نسبة نعم', min_value=0, max_value=100, format='%.1f%%')
            }
        )

with tab5:
    section_caption('استعراض السجلات المفلترة وإتاحة تنزيلها مباشرةً لمزيد من التحليل أو المراجعة التفصيلية')
    preview_cols = [
        'معرف_الحدث', 'المنطقة', 'المدينة', 'التاريخ', 'المركبات/ مرحلة الرحلة الإسعافية',
        'حالة المورد بعد الحدث', 'إجمالي_الإصابات', 'مدة الحدث حساب تلقائي_بالدقائق',
        'زمن الإستجابة_بالدقائق', 'جهة_الخطأ', 'نوع البلاغ'
    ]
    preview_cols = [c for c in preview_cols if c in filtered.columns]
    st.dataframe(filtered[preview_cols].sort_values('التاريخ', ascending=False), width='stretch', hide_index=True)

with tab6:
    section_caption('هنا تعرض جميع الرسوم ')
    for i in range(0, len(charts_library), 2):
        pair = charts_library[i:i+2]
        cols = st.columns(len(pair), gap='large')
        for col, (title, fig) in zip(cols, pair):
            with col:
                st.plotly_chart(fig, width='stretch', key=f'library_chart_{i}_{title}')

st.markdown(
    """
    <div class='footer-bar'>هيئة الهلال الأحمر السعودي</div>
    """,
    unsafe_allow_html=True,
)
