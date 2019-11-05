#cscript prnjobs.vbs -z -p "Epson AL-2600" -j 4
#C:\Windows\System32\Printing_Admin_Scripts\ru-RU
import subprocess as sub


def get_os():
    output = str(sub.check_output('ver',shell = True))
    versions = {'4.00':'Windows 95',
                '4.10':'Windows 98',
                '4.90':'Windows Me',
                '3.10':'Windows NT 3.1',
                '3.50':'Windows NT 3.5',
                '3.51':'Windows NT 3.51',
                '4.0':'Windows NT 4.0',
                '5.1':'Windows XP',
                '5.2':'Windows Server 2003',
                '6.0':'Windows Vista',
                '6.1':'Windows 7',
                '6.2':'Windows 8',
                '6.3':'Windows 8.1',
                '10.0':'Windows 10',}
    for key,item in versions.items():
        if key in output:
            return versions[key]
    return False




files = {'prnjobs.vbs':False,'prncnfg.vbs':False,'prnmngr.vbs':False}

root = 'C:\\Windows\\System32\\Printing_Admin_Scripts\\'
dirs = ['ru-RU','en-US']
dir = None

def mkdir(dir):
    try:
        output = sub.check_output(dir,shell = True)
        return True
    except:
        return False


def get_scripts(script:str):
    if script == 'prnjobs.vbs':
        #getting prnjobs.vbs script
        return


def check_scripts():
    global files,root,dir

    #Checking root
    output = str(sub.check_output("dir "+root,shell = True))
    count = 0
    dir = False
    while count != len(dirs):
        if dirs[count] in output:
            dir = dirs[count]
            break
        count += 1

    if dir == False: #first step
        status = mkdir(root+dirs[1])
        if status == False:
            root = ".\\"
            status = mkdir(root+dirs[1])       
        dir = dirs[1]

    #Cheking available scripts
    output = str(sub.check_output("dir "+root+dir,shell = True))

    for key,item in files.items():
        if key in output:
            files[key] = True
        else:
            get_scripts(key)
            output = str(sub.check_output("dir "+root+dir,shell = True))
            if key in output:
                files[key] = True



def get_queue(action=None):
    '''
    action - Function, must take 2 arguments - id,printer
    '''
    output = str(sub.check_output("cscript "+root+dir+"\\prnjobs.vbs -l",shell = True))
    #Only for russian version
    id_bytes = '\\x88\\xa4\\xa5\\xad\\xe2\\xa8\\xe4\\xa8\\xaa\\xa0\\xe2\\xae\\xe0 \\xa7\\xa0\\xa4\\xa0\\xad\\xa8\\xef'
    printer_bytes = '\\x8f\\xe0\\xa8\\xad\\xe2\\xa5\\xe0'

    queue = []
    #parsing id
    while True:
        if output.find(id_bytes) == -1:
            break
        start = output.find(id_bytes)+len(id_bytes)+1
        id = int(output[start:output.find('\\r',start)])
        start = output.find(printer_bytes)+len(printer_bytes)+1
        printer = output[start:output.find('\\r',start)]
        if action != None:
            action(id,printer)
        queue.append([id,printer])
        try:
            output = output.replace(output[0:start+len(printer)],'')
        except:
            break
    return queue

def main_logic():
    return



def main():
    os = get_os()
    #Dependence from os version, change root, dirs, etc...
    check_scripts()
    get_queue()
    main_logic()


main()
#print(files)