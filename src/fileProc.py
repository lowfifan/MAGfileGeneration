import re

def getMatrix(file):
    f = open(file)
    content = f.read().split("\n")
    file_gen_num = int(content[1])
    para_num = int(content[2])
    matrix = []
    for i in range(4, file_gen_num + 4):
        content_line = content[i].split("\t")
        matrix.append([])
        for j in range(0, para_num):
            matrix[i - 4].append(content_line[j])
    f.close()
    return matrix



def getParaName(file):
    f = open(file)
    content = f.read()
    para_all = re.findall(r'Uniform\n([a-zA-Z]*)[0-9]*\.*[0-9]*', content)
    para_name_wonum = re.findall(r'Uniform\n([a-zA-Z]*)\n', content)
    para_name_wonum.append("Q10")
    para_name_wnum_pre = re.findall(r'Uniform\n([a-zA-Z]*[0-9]+\.*[0-9]*)', content)
    para_name_wnum = []
    para_name_wnum.append([])
    para_name_wnum[0].append(re.search(r'[a-zA-Z]*', para_name_wnum_pre[0]).group(0))
    para_name_wnum[0].append(int(re.search(r'[a-zA-Z]*([0-9]*\.*[0-9]*)', para_name_wnum_pre[0]).group(1)))
    para_wnum_index = []
    para_wonum_index = []
    for i in range(1, len(para_name_wnum_pre)):
        letter = re.search(r'[a-zA-Z]*', para_name_wnum_pre[i])
        number = re.search(r'[a-zA-Z]*([0-9]*\.*[0-9]*)', para_name_wnum_pre[i])
        if (letter.group(0) == "Q" or letter.group(0) == "TSUM"):
            continue
        if (letter.group(0) == para_name_wnum[len(para_name_wnum) - 1][0]):
            para_name_wnum[len(para_name_wnum) - 1].append(int(number.group(1)))
        else:
            para_name_wnum.append([])
            para_name_wnum[len(para_name_wnum) - 1].append(letter.group(0))
            para_name_wnum[len(para_name_wnum) - 1].append(number.group(1))
    f.close()
    for j in range(len(para_name_wonum)):
        for i in range(len(para_all)):
            if (para_all[i] == "Q"):
                para_all[i] = "Q10"
            if (para_all[i] == para_name_wonum[j]):
                para_wonum_index.append(i)

    for j in range(len(para_name_wnum)):
        for i in range(len(para_all)):
            if (para_all[i] == para_name_wnum[j][0] and len(para_wnum_index) == j):
                para_wnum_index.append(i)
    return para_name_wonum, para_name_wnum, para_wonum_index, para_wnum_index


def fileGen(matrix,para_name_wonum, para_name_wnum,para_wonum_index,para_wnum_index,log,No):
    log.writelines("generating "+str(No+1)+"th files\n")
    f = open("../file/MAG201.CAB")
    writeFile = open("../file_gen/MAGA"+str(No+1)+".CAB", "w")
    matchfile = f.read()
    matchfile_paraName = re.findall(r'([A-Za-z0-9]+)\s*=\s*-?([0-9]+.?[0-9]*)', matchfile)
    newMatchfile = matchfile
    found_all = 1
    for i in range(len(para_name_wonum)):
        found = 0
        for j in range(len(matchfile_paraName)):
            if (para_name_wonum[i] == matchfile_paraName[j][0]):
                found = 1
                matchgroup = re.search(matchfile_paraName[j][0] + r'(\s*=\s*)-?[0-9]+.?[0-9]*', newMatchfile)
                newMatchfile = re.sub(matchfile_paraName[j][0] + r'\s*=\s*-?[0-9]+.?[0-9]*',
                                      matchfile_paraName[j][0] + matchgroup.group(1) + matrix[No][para_wonum_index[i]],
                                      newMatchfile)
                log.writelines("found " + matchgroup.group() + "  replace with   " + re.search(
                    matchfile_paraName[j][0] + r'\s*=\s*-?[0-9]+.?[0-9]*', newMatchfile).group() + "\n")
        if found == 0:
            found_all = 0
            log.writelines(para_name_wonum[i] + " not found" + "\n")

    for i in range(len(para_name_wnum)):
        found = 0
        for j in range(len(matchfile_paraName)):
            if (para_name_wnum[i][0] == matchfile_paraName[j][0]):
                found = 1
                if(para_name_wnum[i][0] == "FLTB" or para_name_wnum[i][0] == "FOTB"):
                    continue
                for k in range(len(para_name_wnum[i]) - 1):
                    numstr = str(float(para_name_wnum[i][k + 1]) / 100.0)
                    matchgroup = re.search(
                        matchfile_paraName[j][0] + r'(\s*=.*?)' + numstr + r'([0]*, *)([0-9]+.?[0-9]*)',
                        newMatchfile, re.DOTALL)
                    if (matchgroup == None):
                        log.writelines(matchfile_paraName[j][0]+ " "+ numstr+ " not found\n")
                    else:
                        newMatchfile = re.sub(
                            matchfile_paraName[j][0] + r'\s*=.*?' + numstr + r'[0]*, *[0-9]+.?[0-9]*',
                            matchfile_paraName[j][0] + matchgroup.group(1) + numstr + matchgroup.group(2) + matrix[No][para_wnum_index[i] + k],
                            newMatchfile, 0, re.DOTALL)
                        log.writelines("found " + matchfile_paraName[j][0] + "   " + numstr + matchgroup.group(2) + matchgroup.group(3) + "  replace with " + matchfile_paraName[j][0] + "   " + numstr + matchgroup.group(2) + matrix[No][para_wnum_index[i] + k] + "\n")
        if found == 0:
            found_all = 0
            print(para_name_wnum[i][0], " not found")
    writeFile.write(newMatchfile)
    f.close()
    log.writelines("\n")
    writeFile.close()
    return found_all

