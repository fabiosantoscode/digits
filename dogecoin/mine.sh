#!/bin/bash

curl 'https://poloniex.com/public?command=returnChartData&currencyPair=BTC_DOGE&start=1455101400&end=9999999999&period=1800' | jq 'map(.close)' > data.json

