import os
import pytest
import pandas as pd
from datetime import datetime
from main import (
    apply_visual_settings,
    parse_arguments,
    load_csv,
    clean_amount_column,
    expand_installments,
    handle_duplicate_categories,
    get_custom_period,
    enrich_date_columns,
    create_output_dir,
    plot_bar,
    plot_pie,
    generate_reports,
    generate_total_report,
)

@pytest.fixture(autouse=True)
def ensure_charts_dir_exists():
    create_output_dir()

def test_clean_amount_column():
    df = pd.DataFrame({'AMOUNT': ['$1,000.50', '$2,000.00']})
    result = clean_amount_column(df)
    assert result['AMOUNT'].tolist() == [1000.50, 2000.00]

def test_expand_installments():
    df = pd.DataFrame({
        'DATE': [pd.Timestamp('2024-01-01')],
        'AMOUNT': [100],
        'CATEGORY': ['Test'],
        'INSTALLMENTS': ['1/3']
    })
    result = expand_installments(df)
    assert len(result) == 3
    assert result['DATE'].tolist() == [
        pd.Timestamp('2024-01-01'),
        pd.Timestamp('2024-02-01'),
        pd.Timestamp('2024-03-01')
    ]

def test_handle_duplicate_categories():
    df = pd.DataFrame({
        'CATEGORY': ['Food', None],
        'CATEGORY2': ['Drinks', 'Rent'],
        'AMOUNT': [100, 200],
        'DATE': [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-01')]
    })
    result = handle_duplicate_categories(df)
    assert len(result) == 3
    assert set(result['CATEGORY']) == {'Food', 'Drinks', 'Rent'}

def test_get_custom_period():
    date = datetime(2024, 4, 26)
    period = get_custom_period(date)
    assert period.startswith('2024-04-25')  # O período começa em 25

def test_enrich_date_columns():
    df = pd.DataFrame({
        'DATE': [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-01')]
    })
    result = enrich_date_columns(df)
    assert 'MONTH' in result.columns
    assert 'YEAR' in result.columns
    assert 'CUSTOM_PERIOD' in result.columns

def test_create_output_dir():
    create_output_dir()
    assert os.path.exists('charts')
    os.rmdir('charts')

def test_plot_bar():
    df = pd.DataFrame({
        'CATEGORY': ['Food', 'Drinks'],
        'AMOUNT': [100, 200]
    })
    try:
        plot_bar(df, "Test Bar Plot", "test_bar_plot")
        assert os.path.exists('charts/test_bar_plot_bar.png')
    finally:
        os.remove('charts/test_bar_plot_bar.png')

def test_plot_pie():
    df = pd.DataFrame({
        'CATEGORY': ['Food', 'Drinks'],
        'AMOUNT': [100, 200]
    })
    try:
        plot_pie(df, "Test Pie Plot", "test_pie_plot")
        assert os.path.exists('charts/test_pie_plot_pie.png')
    finally:
        os.remove('charts/test_pie_plot_pie.png')

def test_generate_reports():
    df = pd.DataFrame({
        'CATEGORY': ['Food', 'Drinks'],
        'AMOUNT': [100, 200],
        'DATE': [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-01')],
        'CUSTOM_PERIOD': ['2024-01-01 - 2024-02-01', '2024-01-01 - 2024-02-01']
    })
    try:
        generate_reports('CUSTOM_PERIOD', 'Period', df)
        assert os.path.exists('charts/Period_2024-01-01 - 2024-02-01_bar.png')
        os.remove('charts/Period_2024-01-01 - 2024-02-01_bar.png')
    finally:
        pass


def test_generate_total_report():
    df = pd.DataFrame({
        'CATEGORY': ['Food', 'Drinks'],
        'AMOUNT': [100, 200],
        'DATE': [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-01')]
    })
    try:
        generate_total_report(df)
        assert os.path.exists('charts/Total_bar.png')
        os.remove('charts/Total_bar.png')
    finally:
        pass
