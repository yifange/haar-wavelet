#!/bin/bash
#TODO change bluk size and overlap

usage() { echo "Usage: $0 -f <csv_file> -a <array_name> -r <row_dimension> -c <col_dimension>" 1>&2; exit 1;}
csv_file="" 
array_name=""
raw_array_name=""
row_dim=1
col_dim=1

while getopts "f:a:r:c:" opt; do
  case $opt in
    f)
      csv_file=$OPTARG
      ;;
    a) 
      array_name=$OPTARG
      ;;
    r)
      row_dim=$OPTARG
      ;;
    c)
      col_dim=$OPTARG
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

echo "row_dim:$row_dim"
echo "col_dim:$col_dim"

raw_array_name=${array_name}_raw
echo $csv_file
echo $raw_array_name

echo "------------"
echo "drop array" 
echo "------------"
iquery -q "DROP ARRAY $raw_array_name" > /dev/null 2>&1
iquery -q "DROP ARRAY $array_name" > /dev/null 2>&1

echo "------------"
echo "crate array"
echo "------------"
iquery -aq "create array $raw_array_name
<i:int64,
j:int64,
val:double>
[n=0:$[row_dim*col_dim],1000000,0]"

iquery -aq "create array $array_name
<val:double>
[i=0:$row_dim,1000,0,
j=0:$col_dim,1000,0]"

echo "------------"
echo "call csv2scidb"
echo "------------"
rm -f /tmp/load.scidb
csv2scidb -i $csv_file -p "NNN" > /tmp/load.scidb &
sleep 2;

echo "------------"
echo "Load raw array"
echo "------------"
iquery -nq "LOAD $raw_array_name FROM '/tmp/load.scidb'" 

echo "------------"
echo "redimension_store"
echo "------------"
iquery -naq "redimension_store($raw_array_name,$array_name)" 


