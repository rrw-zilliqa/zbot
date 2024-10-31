# zbot

This is a simple telegram bot which will operate a wallet for you and can perform some tasks via OpenAI function calling.

To use it:

```
export OPENAPI_API_KEY=<your api key>
export TELEGRAM_BOT_TOKEN=<telegram bot token>
export ETHEREUM_RPC_URL=https://api.zq2-prototestnet.zilliqa.com
export SEED="Wallet generation seed. Keep this secret!"
export ZILLIQA_FAUCET_URL=https://faucet.zq2-prototestnet.zilliqa.com
export ZILLIQA_OTTERSCAN_URL=https://explorer.zq2-prototestnet.zilliqa.com/
```

And then run `./main.py`; `/help` is moderately informative.

Things you can (currently) ask:

```
/ask run the faucet for me
/ask what's my balance?
/ask please send 0.1 zil to <address>
```

You can get an OpenAPI key from openAPI once you've funded your account.
You can get a telegram bot token from @botfather.


Enjoy!
<richard@zilliqa.com>
