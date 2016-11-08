#!/bin/bash

basename=`ls -tr dashboard-xhr*`

rm rep_total
rm dem_total

for f in $basename 
do
  echo "File $f"

  # substitute escaped newlines, ", and tabs with the real deal
  sed -e "s/\\\n/\n/g" $f | sed -e "s/\\\\\"/\"/g" | sed -e "s/\\\t//g" > v1

  # put the total delegates in separate files
  grep -e "<div class=\"republican\">" v1 | grep -e "[0-9]\+</span></div>" > rep
  grep -e "<div class=\"democrat\">" v1 | grep -e "[0-9]\+</span></div>" > dem

  # get the time of this file
  t=`ls --full-time $f | awk '{print $6,$7}'`

  # timestamp the total files
  echo -n "$t," >> rep_total
  echo -n "$t," >> dem_total

  # put the total value into the total file
  awk -F "<|>|=| |\"" '{ print $16 }' rep >> rep_total
  awk -F "<|>|=| |\"" '{ print $16 }' dem >> dem_total

  # get state data records from the list
  grep -e "[^>]<a href=\"http://elections.nytimes.com/2008/results/states/" -A 12 -B 1 v1 > v2

  # take out links, leave state name
  sed -e "s/^.*a href.* title=\"//; s/\" target.*//; s/^.*<.*>.*$//; s/--//; /^[A-Z]/ { / / { s/ /_/g; } };" v2 > v1

  # take out empty lines
  sed -ne '/^$/ !p;' v1 > v2

  # join lines, except for "first polls close ..."
  sed -ne '/^[A-Z]/ { N; N; s/\n//; /First Polls Close/ { s/\n//g p }; /First Polls Close/ !{ N; N; s/\n//g p; }; }' v2 > v1

  # set "first..." text to 0%
  awk '$2 ~ /First/ { if(NR > 14) {print $1, "0%", "0%", "0%"} } $2 !~ /First/ { if(NR > 14) {print $1, $2, $3, $4} }' v1 > v2

  while read line
  do
    state="states/"`echo $line | awk '{ print $1 }'`
    democrat=`echo $line | awk '{ print $2 } ' | sed -e "s/\([0-9]*\)%/\1/"`
    republican=`echo $line | awk '{ print $3 } ' | sed -e "s/\([0-9]*\)%/\1/"`
    reporting=`echo $line | awk '{ print $4 } ' | sed -e "s/\([0-9]*\)%/\1/"`

    echo -n "$t," >> $state
    echo -n "$democrat," >> $state
    echo -n "$republican," >> $state
    echo "$reporting" >> $state
  done < v2
done

rm rep dem 
#v1 v2
exit 0

