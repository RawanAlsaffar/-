import pandas as pd
from pathlib import Path
p = Path('/home/ubuntu/fleet_q1_analysis/fleet_accidents_q1_2026_clean.csv')
df = pd.read_csv(p)
col = 'المركبات/ مرحلة الرحلة الإسعافية'
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
}
s = df[col].astype(str).str.replace('\xa0',' ', regex=False).str.strip().replace(replacements)
s = s.str.replace('.', ' ', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()
print(s.value_counts(dropna=False).to_string())
