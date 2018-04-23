import os
import csv

def txt2csv(inputfile,outputfile):  
  datacsv = open(outputfile,'w')  
  csvwriter = csv.writer(datacsv,dialect=("excel"))  
  mainfileH = open(inputfile,'rb')  
  for line in mainfileH.readlines():     
      rowline = []
      line = line.decode("utf-8-sig").replace(' ', ' ').lstrip(" ").rstrip(' ')
      line = line.replace('\r\n','')
      char_index = False
      for content in line.split("      "):
          rowline.append(content)
      print (rowline) 
      #line = line.replace()
      #print(line)    
      csvwriter.writerow(rowline)  
  datacsv.close()  
  mainfileH.close()
#
def main():
    inputfile = "./data/InAs.txt"
    outputfile = "./data/InAs.csv"
    txt2csv(inputfile, outputfile)

if __name__ == '__main__':
    main()