from datetime import datetime
from pathlib import Path
from numpy import fabs

from pytz import timezone
import pandas as pd

from settings import CSV_NAME, CSV_DIR

def localize(d: datetime) -> datetime:
    return timezone('Europe/Moscow').localize(d)


def get_now() -> datetime:
    return localize(datetime.now())


def _get_stats_dataframe() -> pd.DataFrame:
    if Path(CSV_DIR / CSV_NAME).exists():
        return pd.read_csv(CSV_DIR / CSV_NAME)
    else:
        df = pd.DataFrame([], columns=['Date', 'Refills', 'Total price', 'Profit', 'Profit in perc', 'USD course'])
        _save_dataframe(df)
        return df

def _save_dataframe(df: pd.DataFrame):
    output_dir = Path(CSV_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_DIR / CSV_NAME, index=False)


def add_to_csv(sum_pay_in, portfolio_sum, profit_in_rub, profit_in_percent, usd_course):
    df = _get_stats_dataframe()
    df = df.append(
        {
            'Date': get_now().date(),
            'Refills': sum_pay_in,
            'Total price': portfolio_sum,
            'Profit': profit_in_rub,
            'Profit in perc': profit_in_percent,
            'USD course': usd_course
        },
        ignore_index=True
    )
    _save_dataframe(df)


