#!/bin/bash
git pull --no-edit
wget -N http://ssb22.user.srcf.net/typography.js
git commit -am update && git push
