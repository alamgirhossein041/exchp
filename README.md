Prerequisite

```bash
yum install python3-pip
pip3 install binance-futures-connector
pip3 install python-telegram-bot

# use the English quotation
# Exchange API Token
export API_KEY=""
export SECRET_KEY=""

# Telegram API Token
export BOT_TOKEN=""
# with @ symbol
export CHANNEL_ID=""

# watch list
export TOKEN_LIST=""
```

Run
```bash
# use crontab
crontab -e

# vim edit
# every 30 minutes
# export and execute
*/30  * * * *
```
