#!/usr/bin/env bash -e

EXEC="docker run --rm -e SMARTHR_TENANT=$SMARTHR_TENANT -e SMARTHR_TOKEN=$SMARTHR_TOKEN ghcr.io/yasuyuky/smarthr-imedic"

for f in tsv csv; do
    mkdir -p output/$f
    $EXEC $f last last >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").last-last.txt
    $EXEC $f full full >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").full-full.txt
    $EXEC $f last full >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").last-full.txt
    $EXEC $f last email >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").last-email.txt
done
