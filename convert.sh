#!/bin/bash

IN=/dev/stdin
OUT=/dev/stdout

function main () {
    BUFFER="$(cat 0<$IN)"
    
    echo "{" > $OUT
    echo "$BUFFER" | head -n 1 | sed -e "s/.*'\(.*\)'.*/\"timestamp\": \"\1\"/" >> $OUT
    
    CANDIDATE_LOOKUP=$(echo "$BUFFER" | head -n 2 | tail -n 1)
    declare -gA CANDIDATES
    
    _IFS=$IFS
    export IFS='|'
    for cand in $(echo "$CANDIDATE_LOOKUP")
    do
        CAND_ID=$(echo $cand | cut -d ';' -f 1)
        CAND_NAME=$(echo $cand | cut -d ';' -f 2,3,4,5 | tr ";" " ")
        CANDIDATES[$CAND_ID]="$CAND_NAME"
        # echo "$CAND_ID = ${CANDIDATES[$CAND_ID]}"
    done
    IFS=$_IFS
    
    echo ${!CANDIDATES[@]}
    echo $CANDIDATES
    
    echo "}" >> $OUT

    sed -f convert.sed 0<$IN >>$OUT
}

main "$@"
