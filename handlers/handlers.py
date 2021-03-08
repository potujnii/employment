from loader import bot, dp, db, logger, logsDirect
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import requests
import json
import logging
from aiogram.types import InputFile
import re
from datetime import datetime, date, time, timedelta
from loguru import logger
from functions import functions
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer('Welcome!I\'m a bot who knows everything about currency\nMy commands:\n1./list\n2./exchange\n3./history')


@dp.message_handler(commands=["list"])
@logger.catch
async def dwa(message: types.Message):
    messageToSend = 'Базовая валюта: USD\n'
    # check how much time has passed
    if functions.timeDifferenceMoreThanTen():
        response = requests.get('https://api.exchangeratesapi.io/latest?base=USD').json()
        currency_value = response.get('rates').items()
        messageToSend += 'лог: с последнего запроса прошло больше 10 минут. данные свежие\n'
    else:
        currency_value = db.get_currency_value_list()
        messageToSend += 'лог: с последнего запроса прошло менее 10 минут. данные НЕсвежие\n'

    # from tuple to str, and appen msg for send
    for cortej in currency_value:
        currency, value = cortej
        messageToSend += f"{currency} - {float('{:.2f}'.format(value))}\n"
    await message.answer(messageToSend)

    # add log
    logger.info("Отправка сообщения. Сообщение: {}".format(message.text))

@dp.message_handler(commands=["exchange"])
async def get_currency_and_value(message: types.Message):
    # if expression in correct
    if re.fullmatch(r'^\/exchange \d{1,15} [A-Za-z]{3} to [A-Za-z]{3}$', message.text) or re.fullmatch(r'^\/exchange \$\d{1,15} to [A-Za-z]{3}$', message.text) \
            or re.fullmatch(r'^\/exchange \d{1,15}\$ to [A-Za-z]{3}$', message.text):
        # get base, symbols, value
        exchangeData = message.text
        exchangeData = exchangeData[10:].split('to')
        if '$' in message.text:
            base = 'USD'
        else:
            base = re.findall('[A-Za-z]{3}', exchangeData[0])[0].upper()

        valueToExchange = re.findall('\d{1,5}', exchangeData[0])[0]
        symbols = re.findall('[A-Za-z]{3}', exchangeData[1])[0].upper()


        # make request
        response = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={symbols}&base={base}')
        if response.status_code == 400:
            # if error
            await message.answer(response.json().get('error'))
        else:
            rate = response.json().get('rates').get(symbols)
            result = float(rate) * float(valueToExchange) # convert value
            result = float('{:.2f}'.format(result)) # 2 points
            await message.answer(f'\n{valueToExchange} {base}\n=\n{result} {symbols}')
    else:
        await message.answer('Wrong input.\nCorrect examples: \n/exchange $10 to PLN\nor\n/exchange 10 RUB to USD')


@dp.message_handler(commands=["history"])
async def get_currency_and_valu1e(message: types.Message):
    # if expression is correct
    if re.fullmatch('\/history\s[A-Za-z]{3}\/[A-Za-z]{3}\sfor\s\d{1,3}\sdays', message.text) \
            or re.fullmatch('\/history\s[A-Za-z]{3}\/[A-Za-z]{3}\sfor\s\d{1,3}\sday', message.text):
        msg = message.text
        msg = msg.split('for')
        # split and find base, symbols, day
        base = re.findall(r'\b[A-Za-z]{3}\b', msg[0], re.ASCII)[0].upper()
        symbols = re.findall(r'\b[A-Za-z]{3}\b', msg[0], re.ASCII)[1].upper()
        day = int(re.findall(r'\d{1,15}', msg[1], re.ASCII)[0])

        end_at = datetime.today().date()
        if day == 1:
            day = 2
        start_at = end_at - timedelta(day)
        # request and get response
        response = requests.get(f'https://api.exchangeratesapi.io/history?start_at={start_at}&end_at={end_at}&base={base}&symbols={symbols}')
        # print(f'https://api.exchangeratesapi.io/history?start_at={start_at}&end_at={end_at}&base={base}&symbols={symbols}')
        # if response is error
        if response.status_code == 400:
            await message.answer(response.json().get('error'))
        else:
            currency_value = response.json().get('rates')
            values = []
            data = {symbols: values}
            # get values from response
            print(currency_value.values())

            for item in currency_value.values():
                values.append(item.get(symbols))
                print(item)
            # make graph
            df = pd.DataFrame(data)
            x = np.arange(len(values))
            plt.axis([0, min(values), 0, max(values)*2])
            plt.plot(x, df)
            plt.legend(data, loc=2)
            # save img and send it to user
            img = 'graph/graph.png'
            plt.savefig(img)
            imgToSend = InputFile(img, filename=img)
            await bot.send_photo(message.from_user.id, imgToSend)


    else:
        await message.answer('Wrong input.\nCorrect examples:\n/history USD/CAD for 7 days\nor\n/history USD/CAD for 1 day')

