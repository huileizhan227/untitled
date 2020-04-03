#!/bin/bash
folder=$1
port=$2
pkg=$3
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/channel.yml -o ${folder}/channel -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/follow.yml -o ${folder}/follow -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/football.yml -o ${folder}/football -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/home.yml -o ${folder}/home -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/listen.yml -o ${folder}/listen -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/me.yml -o ${folder}/me -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/video.yml -o ${folder}/video -u $port --capability appPackage=$pkg
java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c ./case/vskit.yml -o ${folder}/vskit -u $port --capability appPackage=$pkg
