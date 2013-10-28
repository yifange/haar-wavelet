#!/usr/bin/python
import csv, argparse
from argparse import ArgumentParser

def main():
  parser = argparse.ArgumentParser(description='Parse N by N csv file into CSV file of (row, col, val) each line.')
  parser.add_argument('--inf', dest='infile', required=True, help='input N by N csv file')
  parser.add_argument('--outf', dest='outfile', required=True, help='output file')
  args = parser.parse_args()

  with open(args.infile, 'rb') as inf, open(args.outfile, 'wb') as outf:
    reader = csv.reader(inf, delimiter=' ')
    writer = csv.writer(outf)
    row_num = 0
    for row in reader:
      col_num = 0
      for col in row:
	writer.writerow([row_num, col_num, col])
        col_num += 1
      row_num += 1
        
if  __name__ =='__main__':
    main()
