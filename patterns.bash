#!/usr/bin/env bash -e

EXEC="docker run --rm -e SMARTHR_TENANT=$SMARTHR_TENANT -e SMARTHR_TOKEN=$SMARTHR_TOKEN ghcr.io/yasuyuky/smarthr-imedic"
OUTPUTS=()

for f in tsv csv; do
    mkdir -p output/$f
    for pattern in "last last" "full full" "last full" "last email"; do
        set -- $pattern
        output=output/$f/${SMARTHR_TENANT}$(date +"%Y%m%d").$1-$2.txt
        $EXEC $f "$1" "$2" >"$output"
        OUTPUTS+=("$output")
    done
done

printf 'Created files:\n'
printf '  %s\n' "${OUTPUTS[@]}"
