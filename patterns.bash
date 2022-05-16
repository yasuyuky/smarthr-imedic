#!/usr/bin/env bash -e

for f in tsv csv; do
    mkdir -p output/$f
    python create_dict.py $f last last >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").last-last.txt
    python create_dict.py $f full full >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").full-full.txt
    python create_dict.py $f last full >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").last-full.txt
    python create_dict.py $f last email >output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").last-email.txt
done
