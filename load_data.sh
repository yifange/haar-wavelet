#!/bin/bash

usage() { echo "Usage: $0 -f <csv_file> -a <array_name>" 1>&2; exit 1;}
csv_file="" 
array_name=""
raw_array_name=""
while getopts "f:a:" opt; do
  case $opt in
    f)
      csv_file=$OPTARG
      ;;
    a) 
      array_name=$OPTARG
      ;;
    \?)
      echo "Invalid option: $OPTARG" >&2
      usage
      ;;
     *)
      usage
      ;;
  esac
done

if [ -z "$csv_file" ] || [ -z "$array_name"]
then
   usage
fi

raw_array_name=${array_name}_raw
echo $csv_file
echo $raw_array_name

iquery -aq "create array $raw_array_name
<i:int64,
j:int64,
val:double>
[n=0:*,10,0]"

iquery -aq "create array $array_name
<val:double>
[i=0:*,10,0,
j=0:*,10,0]"

rm -f /tmp/load.scidb
csv2scidb -i $csv_file -p "NNN" > /tmp/load.scidb &
sleep 2;

iquery -q "LOAD $raw_array_name FROM '/tmp/load.scidb'"
iquery -aq "redimension_store($raw_array_name,$array_name)"


