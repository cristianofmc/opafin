import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import os
import re
import argparse

def apply_visual_settings():
    sns.set(style="whitegrid")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Expense category analysis.')
    parser.add_argument('--csv', required=True, help='Path to the input CSV file.')
    return parser.parse_args()

def load_csv(csv_path):
    return pd.read_csv(csv_path, parse_dates=['DATE'])

def clean_amount_column(df):
    df['AMOUNT'] = df['AMOUNT'].replace(r'[$,]', '', regex=True).astype(float)
    return df

def expand_installments(df):
    installment_pattern = re.compile(r'(\d+)/(\d+)')
    expanded_rows = []
    for _, row in df.iterrows():
        installments = row['INSTALLMENTS']
        if isinstance(installments, str) and installment_pattern.match(installments):
            current, total = map(int, installment_pattern.match(installments).groups())
            for i in range(current, total + 1):
                new_date = row['DATE'] + pd.DateOffset(months=i - current)
                new_row = row.copy()
                new_row['DATE'] = new_date
                expanded_rows.append(new_row)
        else:
            expanded_rows.append(row)
    return pd.DataFrame(expanded_rows)

def handle_duplicate_categories(df):
    categories = []
    for _, row in df.iterrows():
        if pd.notna(row['CATEGORY']):
            categories.append((row['CATEGORY'], row['AMOUNT'], row['DATE']))
        if pd.notna(row['CATEGORY2']):
            categories.append((row['CATEGORY2'], row['AMOUNT'], row['DATE']))
    return pd.DataFrame(categories, columns=['CATEGORY', 'AMOUNT', 'DATE'])

def get_custom_period(date):
    if date.day >= 25:
        start = date.replace(day=25)
    else:
        start = (date - timedelta(days=date.day)).replace(day=25)
    end = start + pd.DateOffset(months=1)
    return f"{start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')}"

def enrich_date_columns(df):
    df['MONTH'] = df['DATE'].dt.to_period('M')
    df['YEAR'] = df['DATE'].dt.year
    df['CUSTOM_PERIOD'] = df['DATE'].apply(get_custom_period)
    return df

def create_output_dir():
    os.makedirs("charts", exist_ok=True)

def plot_bar(data, title, filename):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='AMOUNT', y='CATEGORY', data=data.sort_values('AMOUNT', ascending=False))
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', label_type='edge')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"charts/{filename}_bar.png")
    plt.close()

def plot_pie(data, title, filename):
    fig = px.pie(data, names='CATEGORY', values='AMOUNT', title=title)
    fig.write_image(f"charts/{filename}_pie.png")

def generate_reports(group_by, label, df):
    grouped = df.groupby([group_by, 'CATEGORY'])['AMOUNT'].sum().reset_index()
    for period in grouped[group_by].unique():
        period_data = grouped[grouped[group_by] == period]
        title = f"Expenses by Category - {label} {period}"
        filename = f"{label}_{period}"
        plot_bar(period_data, title, filename)
        plot_pie(period_data, title, filename)

def generate_total_report(df):
    total = df.groupby('CATEGORY')['AMOUNT'].sum().reset_index()
    plot_bar(total, "Total Expenses by Category", "Total")
    plot_pie(total, "Total Expenses by Category", "Total")

def main():
    apply_visual_settings()
    args = parse_arguments()
    df = load_csv(args.csv)
    df = clean_amount_column(df)
    df = expand_installments(df)
    df = handle_duplicate_categories(df)
    df = enrich_date_columns(df)
    create_output_dir()
    generate_reports('CUSTOM_PERIOD', 'Period', df)
    generate_reports('MONTH', 'Monthly', df)
    generate_reports('YEAR', 'Yearly', df)
    generate_total_report(df)

    print("Reports generated in ./charts")

if __name__ == "__main__":
    main()
