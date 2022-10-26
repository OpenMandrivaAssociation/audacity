#!/bin/sh
curl -L https://audacityteam.org/ 2>/dev/null |grep 'Latest version' |sed -e 's,.*Latest version,,g;s,.*: ,,;s,<.*,,'
