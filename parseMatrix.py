#!/usr/bin/python
import csv, argparse
import math
from argparse import ArgumentParser
# NOTE does not check if dim is bigger than colum num and row number 
def main():
  parser = argparse.ArgumentParser(description='Parse csv file into CSV file of (row, col, val) each line.\
						Corp the maxtrix to 2^n by 2^n matrix if needed')
  parser.add_argument('-n', dest='n', required=True, type=float,
		     help = '2^n dimension of input csv.The haar-wavelet can only process 2^n by 2^n martix')
  parser.add_argument('--inf', dest='infile', required=True, 
                      help='input N by N csv file')
  parser.add_argument('--outf', dest='outfile', required=True, 
                      help='output file')
  args = parser.parse_args()

  dim = int(math.pow(2,args.n)) #dimension should be 2^n

  with open(args.infile, 'rb') as inf, open(args.outfile, 'wb') as outf:
    reader = csv.reader(inf, delimiter=' ')
    writer = csv.writer(outf)
   
    row_num = 0
    while (row_num < dim):
      row =  reader.next()
      col_num = 0
      while (col_num < dim):
        writer.writerow([row_num, col_num, row[col_num]])
        col_num += 1
      row_num +=1

if  __name__ =='__main__':
    main()
