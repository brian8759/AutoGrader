#!/usr/bin/python

import sys, os, csv, re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f',
                    help="Student Info file",
                    dest="file",
                    required=True)

parser.add_argument('--dir',
                    dest="dir",
                    help="Directory from which outputs of the sweep are read.",
                    required=True)

parser.add_argument('-i',
                    help="Interfaces to plot (regex)",
                    default=".*",
                    dest="pat_iface")


args = parser.parse_args()
pat_iface = re.compile(args.pat_iface)

#there are five folders in dir, they are n1, n2, n3, n4, n5, we only check n2,3,4,5
acceptable_range = {'2' : (3, 7), '3' : (0.5, 6), '4' : (0.2, 6), '5' : (0.2, 6)}

def read_list(fname, delim=','):
    lines = open(fname).xreadlines()
    ret = []
    for l in lines:
        ls = l.strip().split(delim)
        ls = map(lambda e: '0' if e.strip() == '' or e.strip() == 'ms' or e.strip() == 's' else e, ls)
        ret.append(ls)
    return ret

def verifyTopo(**kwargs):
    currentDir = os.getcwd()
    errorCount = 0
    for i in range(2, 6):
        fileName = 'n'+str(i)
        filePath = os.path.join(currentDir, args.dir, fileName, 'bwm.txt')
        data = read_list(filePath)
        rate = {}
        column = 3

        for row in data:
            try:
                ifname = row[1]
            except:
                break
            if ifname not in ['eth0', 'lo', 'total']:
                if not rate.has_key(ifname):
                    rate[ifname] = []
                try:
                    rate[ifname].append(float(row[column]) * 8.0 / (1 << 20))
                except:
                    break
        
        
        for k in sorted(rate.keys()):
            if pat_iface.match(k):
                print k
                result = check(rate[k])
                if result:
                    print 'Successful check', filePath
                    continue
                else:
                    errorCount += 1
                    print 'Error', filePath
    if errorCount != 0:
        commentFile = open(kwargs["comment"], 'a+')
        commentFile.write('topo setup is not right\n')
        commentFile.close()
    
    gradeFile = open(kwargs["grade"], 'a+')
    gradeFile.write(str(errorCount))
    gradeFile.write('\n')
    gradeFile.close()

def verifyBWM(**kwargs):
    errorCount = 0
    #in submission dir, there are several bwm.txt files
    for i in range(2, 6):
        fileName = 'bwm'+str(i)+'.txt'
        filePath = os.path.join(kwargs["submission"], fileName)
        
        r = acceptable_range[str(i)]
        data = read_list(filePath)
        rate = {}
        column = 3

        for row in data:
            try:
                ifname = row[1]
            except:
                break
            if ifname not in ['eth0', 'lo', 'total']:
                if not rate.has_key(ifname):
                    rate[ifname] = []
                try:
                    rate[ifname].append(float(row[column]) * 8.0 / (1 << 20))
                except:
                    break

        for k in sorted(rate.keys()):
            if pat_iface.match(k):
                print k
                result = checkBwmRange(rate[k], r)
                if result:
                    print 'Successful check', filePath
                    continue
                else:
                    errorCount += 1
                    print 'error', filePath

    if errorCount != 0:
        commentFile = open(kwargs["comment"],'a+')
        commentFile.write('BWM output is not acceptable\n')
        commentFile.close()
        
    gradeFile =open(kwargs["grade"],'a+')
    gradeFile.write(str(errorCount))
    gradeFile.write('\n')
    gradeFile.close()

def verifyQuiz(**kwargs):
    
    answer = [['B'], ['C', 'D'], ['A'], ['D'], ['D'], ['B']]
    quizPath = os.path.join(kwargs["submission"], "quiz.txt")
    if not os.path.isfile(quizPath):
        # no quiz.txt
        return

    quizFile = open(quizPath, 'r')
    
    lines = quizFile.xreadlines()
    count = 0
    i = 0
    errorCount = 0

    for line in lines:
        tokens = line.strip().split()
        # tokens[1] is the corresponding answer for example tokens[1] = 'B'
        # check if tokens[1] is correct answer
        if tokens[1] in answer[i]:
            count += 1
        else:
            errorCount += 1
        i += 1

    bonus = 0.5 * count
    print 'bonus', bonus

    if errorCount != 0:
        commentFile = open(kwargs["comment"],'a+')
        for item in answer:
            commentFile.write("%s\n" % item)

        commentFile.close()
        
    gradeFile = open(kwargs["grade"],'a+')
    gradeFile.write(str(errorCount*0.5))
    gradeFile.write('\n')
    gradeFile.close()



def check(bwmRate):
    checkRate = bwmRate[2:]
    for r in checkRate:
        if r != 0:
            continue
        else:
            return False

    return True


def checkBwmRange(bwmRate, rateRange):
    #we check the bwmRate, if bwmRate is within the range, then return true
    # we pass the first two elements in bwmRate
    checkRate = bwmRate[2:]
    for r in checkRate:
        if r <= rateRange[1] and r >= rateRange[0]:
            continue
        else:
            #print r
            return False
    
    return True


def getFilePath():
    currentDir = os.getcwd()
    stuInfoPath = os.path.join(currentDir, args.file)
    stuInfoFile = open(stuInfoPath, 'r')
    submissionDir = stuInfoFile.readline()
    submissionDir = submissionDir.rstrip('\n')
    gradePath = stuInfoFile.readline()
    gradePath = gradePath.rstrip('\n')
    commentPath = stuInfoFile.readline()
    commentPath = commentPath.rstrip('\n')
    
    filePathDict = {"submission" : submissionDir, "grade" : gradePath, "comment" : commentPath}
    return filePathDict

def main():
    filePathDict = getFilePath()
    verifyTopo(filePathDict)
    verifyBWM(filePathDict)
    verifyQuiz(filePathDict)
    
if __name__ == '__main__':
    main()
