#!/usr/bin/env python 
import subprocess
from time import sleep
def grabRecent():
    mountCommand = "sudo mount -o ro /piusb.bin /mnt"
    unmountCommand = "sudo umount /mnt"

    findCmd = 'cd /mnt; ls -t | head -n1'

    runCmd(mountCommand)

    filename = runCmd(findCmd)[:-1]

    copyDest = "/home/pi/piShift/"+filename

    copyCmd = "cp /mnt/" + filename + " " + copyDest 

    runCmd(copyCmd)

    runCmd(unmountCommand)

    return filename

def getMD5(fname):
    md5Command = "md5sum " + fname
    result = runCmd(md5Command)
    return result.split()[0]

def runCmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]
    return output

lastHash = None
proc = None
while True:
    newName = grabRecent()
    newHash = getMD5(newName)
    if(proc):
        if (proc.poll()!=None):
            print ("=====YOUR PROGRAM DIED. TRY AGAIN?=====")
            print ("=====THE OUTPUT WAS: ========")
            print ""
            print (proc.communicate()[0])
            print ("=====WAITING FOR NEW FILE======")
            proc = None
    if (newHash!=lastHash and newName!="pishift.py"): #avoid recursion by not running this file automatically
        if (proc):
            proc.kill() #kill the old python file that was running, and start running the new process
            print ("======KILLED======")
        print ("======RUNNING NEW FILE: "+newName+"======")
        proc = subprocess.Popen(["python",newName],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        lastHash = newHash 
    else:
        #print ("======NO CHANGES FOUND======")
        pass
    sleep(1)