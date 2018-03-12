#!/bin/bash

seconds_in_24_hrs=86400

curl 'https://poloniex.com/public?command=returnChartData&currencyPair=BTC_DOGE&start=0&end=9999999999&period='${seconds_in_24_hrs} | jq 'map(.close)' > data.json

