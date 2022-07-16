import requests
from datetime import datetime
import telebot
from auth_data import token


def get_info():
    """Возвращает все пары"""
    response = requests.get(url="https://yobit.net/api/3/info")

    with open("info.txt", "w") as file:
        file.write(response.text)

    return response.text


def get_ticker(coin1="btc", coin2="usd"):
    """Возвращает данные о выбранных парах"""
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1")
    with open("ticker.txt", "w") as file:
        file.write(response.text)

    return response.text


def get_depth(coin1="btc", coin2="usd", limit=150):
    """Возврашает информацию о выставленных ордерах (продажу/покупку)"""
    response = requests.get(url=f"https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("depth.txt", "w") as file:
        file.write(response.text)

    bids = response.json()[f"{coin1}_usd"]["bids"]

    total_bids_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bids_amount += price * coin_amount

    return f"Total bids: {total_bids_amount} $"


def get_trades(coin1="btc", coin2="usd", limit=150):
    """Возваращает совершенные сделки по покупке/продаже"""
    response = requests.get(url=f"https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("trades.txt", "w") as file:
        file.write(response.text)

    total_trade_ask = 0
    total_trade_bid = 0

    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == "ask":
            total_trade_ask += item["price"] * item["amount"]
        else:
            total_trade_bid += item["price"] * item["amount"]

    info = f"[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin1} BUY: {round(total_trade_bid, 2)}$"

    return info


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend! Write the 'price' to find out the cost of BTC!")

    @bot.message_handler(content_types=["text"])
    def send_text(message, coin='eth'):
        if message.text.lower() == "price":
            try:
                req = requests.get(url=f"https://yobit.net/api/3/ticker/{coin}_usd")
                response = req.json()
                sell_price = response[f"{coin}_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%d.%m.%Y %H:%M')}\nSell {coin} price: {sell_price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn...Something was wrong..."
                )
        else:
            bot.send_message(message.chat.id, "invalid command")

    bot.polling()


def main():
    pass
    # print(get_info())
    # print(get_ticker())
    # print(get_ticker(coin1='eth'))
    # print(get_depth(limit=2000))
    # print(get_trades())
    # print(get_trades(coin1='eth'))


if __name__ == '__main__':
    # main()
    telegram_bot(token)