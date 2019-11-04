#!/bin/bash

net_cfg=app/src/main/res/xml/network_security_config.xml
cat $net_cfg | awk '{printf $0}' > tmp.xml

cat tmp.xml \
| sed -E 's#<base-config[^>]+/>|<base-config\>.*</base-config\>>##g' \
| sed -E 's#</network-security-config>#<base-config cleartextTrafficPermitted="true"> <trust-anchors> <certificates src="system" /> <certificates src="user" /> </trust-anchors> </base-config> </network-security-config>#g' \
> $net_cfg

rm tmp.xml
