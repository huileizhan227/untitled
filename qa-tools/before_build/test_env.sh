#!/bin/bash

common_config="app/src/main/java/com/africa/news/common/config/CommonConfig.java"

#sed -i -E 's/ *String +PRE_DOMAIN *= *"www"/ String PRE_DOMAIN = "test" /g' $common_config

sed -i -E 's/ +boolean +IS_TEST *= *false/ boolean IS_TEST = true/g' $common_config

grep -E 'boolean +IS_TEST' $common_config
