#!/bin/bash
COUNTER=0
while true; do
        let COUNTER=COUNTER+1
        python3 manage.py flushexpiredtokens
        printf "Expired tokens flushed. Number of days running: $COUNTER\n"
        sleep 86400
done
