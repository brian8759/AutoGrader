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

        try:
            shutil.copy2(filePath, currentDir)
            #print filePath                                                                                                     
            print 'currently working on', name
            subprocess.call("sudo ./parkinglot-sweep.sh", shell=True)
        except:
            continue