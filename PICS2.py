


# +++++++++++++++++++++++++ Read this: +++++++++++++++++++++++++
# third part: 
# i was not able to change the requested path to this directory on my computer since it should be done in Internet Explorer's settings -> 'Move Folder' and there is only a possibility to browse. 
# this path is the one where i should browse 'C:\Users\user\AppData\Local\Microsoft\Windows\INetCache\Virtualized\C\Users\user\AppData\Local\Microsoft\Windows'
# but as seen, it is virtualised, thus - not visible in the 'browse' window :(

import win32api, win32file, win32event, win32con, win32com.client
import os, shutil
#--------------------------

def walk(path):
    ''' gets path, returns all the subfolder tree under the given path '''
    m = []
    for root, directories, filenames in os.walk(path):
        for filename in filenames: 
            m.append(os.path.join(root,filename) )
    return m
#------------------------

path = "D:\Elik\HW_Golan\Temporary Internet Files"
changeHandle = win32file.FindFirstChangeNotification(
    path,                                   # where to look for
    True,                                   # looking for changes not only in this directory, but in sub-directories too
    win32con.FILE_NOTIFY_CHANGE_FILE_NAME   # looking for recently added / deleted files
    ) 
print "waiting for changes on hadle: " + str(changeHandle)

# navigation to link with win32com.client:
ieApp = win32com.client.Dispatch("InternetExplorer.Application")
#ieApp.Visible = True
ieApp.Navigate('http://google.com/search?q=frc&tbm=isch')

# stop_handles holds one handle for the notifications and another one for standard winapi input. the second handle waits for input from the keyboard and is used to stop the 'while true' loop by cliking on any key
stop_handles = [changeHandle, win32api.GetStdHandle(win32api.STD_INPUT_HANDLE)] 

# before = os.listdir(path)
before = walk(path)
while True:
    # result = return value form waitfor... [ for infinite time until there were updates in the handle-path ]
    # result gets 0 if the return was because of a change-event. (otherwise it is an exception or some other error)
    result = win32event.WaitForMultipleObjects(stop_handles, 0, win32event.INFINITE)  # -> (handles, wait for one(0) / wait for all(1), event for one - infinte time)
    if result == win32con.WAIT_OBJECT_0:# ( if result == 0 ) 0 is the first handle in the []
        # after = os.listdir(path)
        after = walk(path)
        added = [f for f in after if not f in before]
        if len(added)!=0: 
            print "Added: ", ", ".join (added)
            for i in added:
                if i[-4:] == '.png' or i[-4:] == '.jpg' or i[-4:] == '.bmp' or i[-4:] == '.ico' or i[-4:] == '.gif' :   # or whatever other format :)
                    win32file.CopyFile(i, 'D:\\Elik\\HW_Golan\\PICS\\New folder\\'+i.rsplit('\\',1)[1], False)
                    print "copied: ", ", ".join (added)
        before = after
        win32file.FindNextChangeNotification(changeHandle)  # same as FindFirst... but with an already existing handle
    
    elif result == win32con.WAIT_OBJECT_0+1: #( if result == 1 ) 1 is the first handle in the []
        break

win32file.FindCloseChangeNotification (changeHandle)
print '++++++++++++++++++++++++\r\nstopped'

