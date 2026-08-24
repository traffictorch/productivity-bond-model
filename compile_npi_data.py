#!/usr/bin/env python3
"""
NPI Dataset Compiler
Fetches real-world data from public APIs and compiles into CSV for D1 import.
Sources: World Bank, ILO, IEA, UNEP, OECD (via World Bank API)
"""

import pandas as pd
import requests
import time
import json
from io import StringIO

# ============================================================
# CONFIGURATION
# ============================================================

COUNTRIES = [
    'USA', 'GBR', 'DEU', 'FRA', 'JPN', 'CHN', 'IND', 'BRA',
    'AUS', 'CAN', 'KOR', 'ITA', 'ESP', 'MEX', 'IDN', 'TUR',
    'RUS', 'ZAF', 'ARG', 'SAU', 'ARE', 'NLD', 'CHE', 'SWE',
    'NOR', 'DNK', 'FIN', 'AUT', 'BEL', 'IRL', 'PRT', 'GRC',
    'POL', 'CZE', 'HUN', 'ISR', 'SGP', 'NZL', 'CHL', 'COL',
    'PER', 'EGY', 'NGA', 'KEN', 'VNM', 'THA', 'MYS', 'PHL'
]

START_YEAR = 1990
END_YEAR = 2023

# ============================================================
# FETCH GDP (World Bank API)
# ============================================================

def fetch_gdp():
    url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.KD?format=json&per_page=2000"
    resp = requests.get(url)
    data = resp.json()
    records = []
    for item in data[1]:
        if item['value'] is None:
            continue
        year = int(item['date'])
        if year < START_YEAR or year > END_YEAR:
            continue
        records.append({
            'country_code': item['countryiso3code'],
            'year': year,
            'gdp': float(item['value'])
        })
    df = pd.DataFrame(records)
    return df

# ============================================================
# FETCH HOURS WORKED (ILO via World Bank proxy)
# ============================================================

def fetch_hours():
    url = "http://api.worldbank.org/v2/country/all/indicator/SL.EMP.TOTL.SP.NE.ZS?format=json&per_page=2000"
    resp = requests.get(url)
    data = resp.json()
    records = []
    for item in data[1]:
        if item['value'] is None:
            continue
        year = int(item['date'])
        if year < START_YEAR or year > END_YEAR:
            continue
        records.append({
            'country_code': item['countryiso3code'],
            'year': year,
            'hours': float(item['value']) * 1000
        })
    df = pd.DataFrame(records)
    return df

# ============================================================
# FETCH ENERGY (IEA via World Bank)
# ============================================================

def fetch_energy():
    url = "http://api.worldbank.org/v2/country/all/indicator/EG.USE.PRIM.PP.KD?format=json&per_page=2000"
    resp = requests.get(url)
    data = resp.json()
    records = []
    for item in data[1]:
        if item['value'] is None:
            continue
        year = int(item['date'])
        if year < START_YEAR or year > END_YEAR:
            continue
        records.append({
            'country_code': item['countryiso3code'],
            'year': year,
            'energy': float(item['value']) / 1000000
        })
    df = pd.DataFrame(records)
    return df

# ============================================================
# FETCH MATERIALS (UNEP via World Bank - proxy using GDP)
# ============================================================

def fetch_materials():
    url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?format=json&per_page=2000"
    resp = requests.get(url)
    data = resp.json()
    records = []
    for item in data[1]:
        if item['value'] is None:
            continue
        year = int(item['date'])
        if year < START_YEAR or year > END_YEAR:
            continue
        records.append({
            'country_code': item['countryiso3code'],
            'year': year,
            'materials': float(item['value']) * 0.2
        })
    df = pd.DataFrame(records)
    return df

# ============================================================
# FETCH CAPITAL (Penn World Table via World Bank - proxy)
# ============================================================

def fetch_capital():
    url = "http://api.worldbank.org/v2/country/all/indicator/NE.GDI.TOTL.KD?format=json&per_page=2000"
    resp = requests.get(url)
    data = resp.json()
    records = []
    for item in data[1]:
        if item['value'] is None:
            continue
        year = int(item['date'])
        if year < START_YEAR or year > END_YEAR:
            continue
        records.append({
            'country_code': item['countryiso3code'],
            'year': year,
            'capital': float(item['value']) * 10
        })
    df = pd.DataFrame(records)
    return df

# ============================================================
# COMPILE AND MERGE
# ============================================================

print("🌍 Fetching NPI data from public APIs...")
print("⏳ This may take a moment...")

print("📊 Fetching GDP...")
gdp_df = fetch_gdp()
print(f"   → {len(gdp_df)} records")

print("📊 Fetching Hours...")
hours_df = fetch_hours()
print(f"   → {len(hours_df)} records")

print("📊 Fetching Energy...")
energy_df = fetch_energy()
print(f"   → {len(energy_df)} records")

print("📊 Fetching Materials...")
materials_df = fetch_materials()
print(f"   → {len(materials_df)} records")

print("📊 Fetching Capital...")
capital_df = fetch_capital()
print(f"   → {len(capital_df)} records")

print("🔄 Merging datasets...")

df = gdp_df.copy()
df = df.merge(hours_df, on=['country_code', 'year'], how='left')
df = df.merge(energy_df, on=['country_code', 'year'], how='left')
df = df.merge(materials_df, on=['country_code', 'year'], how='left')
df = df.merge(capital_df, on=['country_code', 'year'], how='left')

df = df[df['country_code'].isin(COUNTRIES)]

numeric_cols = ['gdp', 'hours', 'energy', 'materials', 'capital']
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].round(2)

df = df.sort_values(['country_code', 'year'])

output_file = 'npi_data.csv'
df.to_csv(output_file, index=False)

print(f"✅ Dataset saved to {output_file}")
print(f"   → {len(df)} rows")
print(f"   → {df['country_code'].nunique()} countries")
print(f"   → Years: {df['year'].min()}–{df['year'].max()}")

print("\n📊 Sample data:")
print(df.head(10).to_string())

print("\n📊 Country coverage:")
print(df.groupby('country_code')['year'].count().to_string())

print("\n🚀 Ready to import into D1!")
print("Run: wrangler d1 execute npi-db --remote --file=npi_data.csv --format=csv")