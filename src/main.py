import fileProc
import os
import re

def main():
    matrix = fileProc.getMatrix("../file/test_10.sam")
    para_name_wonum, para_name_wnum, para_wonum_index, para_wnum_index = fileProc.getParaName("../file/test_10.fac")
    log = open("../log/log.txt", "w")
    for i in range(len(matrix)):
    #for i in range(3):
        print(str(i+1)+"/"+str(len(matrix)))
        found_all = fileProc.fileGen(matrix,para_name_wonum, para_name_wnum, para_wonum_index, para_wnum_index,log,i)
    log.close()
    if(found_all == 1):
        print("found and replaced all paras")
    else:
        print("some paras not found, plz check logfile for detail")


if __name__ == '__main__':
    main()


