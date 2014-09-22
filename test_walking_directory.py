#!/usr/bin/python

import os, csv, shutil, subprocess

currentDir = os.getcwd()

for root, dirs, files in os.walk(currentDir):
    dirs.sort()
    for name in dirs:
        if name == "util":
            continue
        if "parkinglot-" in name:
            continue
        #for rootI, dirsI, filesI in os.walk(os.path.join(root, name)):
        # create a grade.txt file for each student
        gradePath = os.path.join(root, name, "grade.txt")
        commentPath = os.path.join(root, name, "comments.txt")
        submissionPath = os.path.join(root, name, "Submission attachment(s)")

        #create a studentInfo.txt in currentDir, write gradePath and commentPath into it
        studentInfoPath = os.path.join(currentDir, "studentInfo.txt")
        studentInfoFile = open(studentInfoPath, 'w+')
        studentInfoFile.write(submissionPath)
        studentInfoFile.write('\n')
        studentInfoFile.write(gradePath)
        studentInfoFile.write('\n')
        studentInfoFile.write(commentPath)
        studentInfoFile.write('\n')
        studentInfoFile.close()

        filePath = os.path.join(root, name, "Submission attachment(s)", "parkinglot.py")
        if not os.path.isfile(filePath):
            # empty folder
            gradeFile = open(gradePath, 'w+')
            gradeFile.write('5')
            gradeFile.write('\n')
            gradeFile.write('5')
            gradeFile.write('\n')
            gradeFile.write('3')
            gradeFile.write('\n')
            gradeFile.close()
            
            commentFile = open(commentPath, 'w+')
            commentFile.write("No submission!\n")
            commentFile.close()
            continue

        try: 
            shutil.copy2(filePath, currentDir)
            #print filePath
            print 'currently working on', name
            subprocess.call("sudo ./parkinglot-sweep.sh", shell=True)
        except:
            commentFile= open(commentPath, 'w+')
            commentFile.write("topo.py does not work!\n")
            commentFile.close()
            answer = [['B'], ['C', 'D'], ['A'], ['D'], ['D'], ['B']]
            quizPath = os.path.join(root, name, "Submission attachment(s)", "quiz.txt")
            quizFile = open(quizPath, 'r')

            lines = quizFile.xreadlines()
            count = 0
            i = 0
            errorCount = 0

            for line in lines:
                tokens = line.strip().split()
                if tokens[1] in answer[i]:
                    count += 1
                else:
                    errorCount += 1
                i += 1

            bonus = 0.5 * count
            print 'bonus', bonus

            if errorCount != 0:
                commentFile = open(commentPath,'a+')
                for item in answer:
                    commentFile.write("%s\n" % item)

                commentFile.close()

            gradeFile = open(gradePath, 'a+')
            gradeFile.write('5')
            gradeFile.write('\n')
            gradeFile.write('3')
            gradeFile.write('\n')
            gradeFile.write(str(errorCount*0.5))
            gradeFile.write('\n')
            gradeFile.close()
            continue
                
    
