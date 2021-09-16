from datetime import datetime
from decimal import Decimal
import locale
import os
from pydantic import utils

import tinvest
from tinvest.schemas import Currency

from tinkoffapi import TinkoffApi
from settings import TOKEN, BROKER_ACCOUNT_ID, BROKER_ACCOUNT_STARTED_AT
from utils import add_to_csv, get_now
import bot
from random_emoji import random_emoji


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
api = TinkoffApi(api_token=TOKEN, broker_account_id=BROKER_ACCOUNT_ID)
usd_course = api.get_usd_course()
message_template = (f"{random_emoji()[0]} Отчет за {get_now().date()}:\n"
                    f"- Текущий курс доллара: {usd_course} руб\n"
                    "- Пополнения: {sum_pay_in} руб\n"
                    "- Текущая рублёвая стоимость портфеля: {portfolio_sum} руб\n"
                    "- Рублёвая прибыль: {profit_in_rub} руб ({profit_in_percent}%)")


def get_portfolio_sum() -> int:
    """Возвращает текущую стоимость портфеля в рублях без учета
    просто лежащих на аккаунте рублей в деньгах"""
    positions = api.get_portfolio_positions()

    portfolio_sum = Decimal('0')
    for position in positions:
        current_ticker_cost = (Decimal(str(position.balance))
                               * Decimal(str(position.average_position_price.value))
                               + Decimal(str(position.expected_yield.value)))
        if position.average_position_price.currency.name == "usd":
            current_ticker_cost *= usd_course
        portfolio_sum += current_ticker_cost
    return int(portfolio_sum)


def get_sum_pay_in() -> int:
    """Возвращает сумму всех пополнений в рублях"""
    operations = api.get_all_operations(BROKER_ACCOUNT_STARTED_AT)

    sum_pay_in = Decimal('0')
    for operation in operations:
        if operation.operation_type.value == "PayIn" or operation.operation_type.value == "PayOut":
            if operation.currency == Currency.usd:
                sum_pay_in += Decimal(str(operation.payment)
                                      ) * api.get_usd_course()
            else:
                sum_pay_in += Decimal(str(operation.payment))
    return int(sum_pay_in)


if __name__ == "__main__":
    portfolio_sum = get_portfolio_sum()
    sum_pay_in = get_sum_pay_in()
    profit_in_rub = portfolio_sum - sum_pay_in
    profit_in_percent = 100 * round(profit_in_rub / sum_pay_in, 4)
    add_to_csv(sum_pay_in, portfolio_sum, profit_in_rub, profit_in_percent, float(api.get_usd_course()))

    bot.send_message(
        message_template.format(
            sum_pay_in=sum_pay_in, 
            portfolio_sum=portfolio_sum, 
            profit_in_rub=profit_in_rub,
            profit_in_percent=profit_in_percent)
        )
            
    # print(f"Пополнения: {sum_pay_in:n} руб\n"
    #       f"Текущая рублёвая стоимость портфеля: {portfolio_sum:n} руб\n"
    #       f"Рублёвая прибыль: {profit_in_rub:n} руб ({profit_in_percent:n}%)")
