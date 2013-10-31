#!/bin/bash

usage() { echo "Usage: $0 
		-h <haar_matrix_name> 
		-a <array_to_be_transformed> 
		-r <result_array_name> 
		-f <out_put_file> will be out if not given" 
	1>&2; exit 1;}

haar_matrix_name=""
array_name=""
haar_matrix_tras_name=""
result_array_name="" # if not given, the it will be ${array_name}_trans
out_file="out.csv"
dev=1

while getopts "h:a:r:f" opt; do
  case $opt in
    h)
      haar_matrix_name=$OPTARG
      haar_matrix_tras_name=${haar_matrix_name}_t
      ;;
    a) 
      array_name=$OPTARG
      ;;
    r)
      result_array_name=$OPTARG
      ;;
    f)
      out_file=$OPTARG
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


if [ -z "$haar_matrix_name" ] || [ -z "$array_name" ];
then
   usage
fi

if [ -z "$result_array_name" ];
then
  result_array_name=${array_name}_trans
fi

# 1. transpose haar_maxtrix, tore as haar_matrix_t
echo "
-------------------------
Transpose haar matrix
-------------------------"
if [ $dev -eq 1 ]; then
  echo "Drop array $haar_matrix_tras_name if exist."
  iquery -nq "DROP ARRAY $haar_matrix_tras_name" > /dev/null 2>&1
fi
iquery -naq "store(transpose($haar_matrix_name), $haar_matrix_tras_name)" #trannspose


# 2. haar_2to11 * a2to11 * haar_2to11_t
echo "
-------------------------
Haar transformation
-------------------------"
if [ $dev -eq 1 ]; then
  echo "Drop array $result_array_name if exist."
  iquery -nq "DROP ARRAY $result_array_name" > /dev/null 2>&1
fi
iquery -naq "
	store(multiply(
		multiply($haar_matrix_name, $array_name),
		$haar_matrix_tras_name),
	      $result_array_name)" 


# 3. threshold, only store value > 0.000001, and store in
#    sperate array called ${array_name}_compreesed
echo "
-------------------------
Haar transformation
-------------------------"
if [ $dev -eq 1 ]; then
  echo "Drop array ${array_name}_compressed if exist."
  iquery -nq "DROP ARRAY ${array_nam}_compressed" > /dev/null 2>&1
fi

iquery -nq "SELECT multiply INTO ${array_name}_compressed 
           FROM $result_array_name  
           WHERE multiply>0.000001"

# 4. Outpu the compressed array out to (i,j,val) if val is not 0
iquery  -o csv+ -r $out_file -q "SELECT * FROM ${array_name}_compressed"
