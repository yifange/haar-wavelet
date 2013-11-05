#!/bin/bash
#set -e
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
START=$(date +%s)

iquery -naq "store(transpose($haar_matrix_name), $haar_matrix_tras_name)" #trannspose

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Transpose haar_matrix  took $DIFF seconds"

# 2. haar_2to11 * a2to11 * haar_2to11_t
echo "
-------------------------
Haar transformation
-------------------------"
if [ $dev -eq 1 ]; then
  echo "Drop array $result_array_name if exist."
  iquery -nq "DROP ARRAY $result_array_name" > /dev/null 2>&1
fi
START=$(date +%s)

iquery -naq "
	store(multiply(
		multiply($haar_matrix_name, $array_name),
		$haar_matrix_tras_name),
	      $result_array_name)" 

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Haar transformation  took $DIFF seconds"

# 3. threshold, only store value > 0.000001, and store in
#    sperate array called ${array_name}_compreesed
<<COMMENT1
echo "
-------------------------
Threshold
-------------------------"
#if [ $dev -eq 1 ]; then
#  echo "Drop array ${array_name}_compressed if exist."
#  iquery -nq "DROP ARRAY ${array_nam}_compressed" > /dev/null 2>&1
#fi

#iquery -nq "SELECT multiply INTO ${array_name}_compressed 
#           FROM $result_array_name  
#           WHERE multiply>0.000001"
START=$(date +%s)

iquery -nq "UPDATE $result_array_name 
	       SET multiply=0 
            WHERE multiply >0 AND multiply < 0.00001
	       OR multiply <0 AND multiply > -0.00001"

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Threshold took $DIFF seconds"

COMMENT1


# 4. Outpu the compressed array out to (i,j,val) if val is not 0
echo "
-------------------------
Output (i,j,val)
-------------------------"
iquery  -o csv+ -r $out_file -aq "filter (${result_array_name},multiply!=0)"
