import telegram
import datetime
import os

from binance.cm_futures import CMFutures
from binance.um_futures import UMFutures


def get_sh_time() -> str:
    sh_tz = datetime.timezone(datetime.timedelta(hours=8), name="Asia/Shanghai")
    return (
        datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .astimezone(sh_tz)
        .strftime("%Y-%m-%d %H:%M:%S")
        + "\n"
    )


def get_total_balance(um_futures_client: UMFutures) -> str:
    total_balance = 0.0
    for ele in um_futures_client.balance():
        total_balance += float(ele.get("crossWalletBalance"))
    return "totalAccountValue={}\n\n".format(round(total_balance, 3))


def get_change_percent(title: str, num: float) -> str:
    title_prefix = title + "="
    title_postfix = "%"
    bold_char = "*"
    if num < 0.0:
        title_prefix += bold_char
        title_postfix = bold_char + title_postfix
    return "{}{}{}".format(title_prefix, round(num, 3), title_postfix)


def get_token_info(cm_futures_client: CMFutures, token_list: str) -> str:
    symbol_to_pair_percent = dict()
    for ele in cm_futures_client.ticker_24hr_price_change():
        symbol_to_pair_percent.update(
            {
                ele.get("symbol"): (
                    ele.get("pair"),
                    ele.get("priceChangePercent"),
                    ele.get("lastPrice"),
                )
            }
        )
    res = ""
    for token in token_list:
        symbol = token + "USD_PERP"
        if symbol in symbol_to_pair_percent:
            pair_percent = symbol_to_pair_percent.get(symbol)
            bold_pair_str = "*" + pair_percent[0] + "*"
            change24h_str = get_change_percent("change24h", float(pair_percent[1]))
            tmp = "{}\nlast={}\n{}\n\n".format(
                bold_pair_str, pair_percent[2], change24h_str
            )
            res += tmp

    return res.strip()


def get_exchange_info() -> str:
    api_key = os.environ["API_KEY"]
    secret_key = os.environ["SECRET_KEY"]
    token_list = os.environ["TOKEN_LIST"].split(",")

    um_futures_client = UMFutures(key=api_key, secret=secret_key)
    total_balance = get_total_balance(um_futures_client)

    cm_futures_client = CMFutures(key=api_key, secret=secret_key)
    token_info = get_token_info(cm_futures_client, token_list)

    return total_balance + token_info


if __name__ == "__main__":
    bot = telegram.Bot(token=os.environ["BOT_TOKEN"])
    bot.send_message(
        chat_id=os.environ["CHANNEL_ID"],
        text=get_sh_time() + "\n" + get_exchange_info(),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )
