#!/bin/bash
#set -e
usage() { echo "Usage: $0 
		-a <array_to_be_transformed> 
		-f <out_put_file> will be out if not given
		-t <threshold>"
	1>&2; exit 1;}

array_name=""
out_file="out.csv"
dev=1
threshold=0;

while getopts "a:f:t:" opt; do
  case $opt in
    a) 
      array_name=$OPTARG
      ;;
    f)
      out_file=$OPTARG
      ;;
    t)
      threshold=$OPTARG
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

echo "thrshold: $threshold"

if [ -z "$array_name" ];
then
   usage
fi


#    sperate array called ${array_name}_compreesed
echo "
-------------------------
Threshold
-------------------------"
START=$(date +%s)

iquery -nq "UPDATE $array_name
	       SET multiply=0 
            WHERE multiply > 0 AND multiply < $threshold
               OR multiply < 0 AND multiply > $(expr 0 - $threshold)"

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Threshold took $DIFF seconds"



# 4. Outpu the compressed array out to (i,j,val) if val is not 0
echo "
-------------------------
Output (i,j,val)
-------------------------"
iquery  -o csv+ -r $out_file -aq "filter ($array_name,multiply!=0)"

read -p "Press any key..."
