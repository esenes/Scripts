import vxi11

######################  USER INPUT  ######################
scope_address = '169.254.155.165'
folder_name = '\"C:/test/tst1\"' # finish withouth /
file_format = 'csv' # csv without point
destination_dir = './' # finish with /
##########################################################


scope = vxi11.Instrument(scope_address)
print('\n'+scope.ask("*IDN?")+'\n')

# set scope path
scope.write('FILES:CWD '+folder_name)
scope_folder_set = scope.ask('FILES:CWD?')
scope_folder_set = scope_folder_set.split(' ')[-1]
print('Scope set to read '+scope_folder_set)
print('User asked for '+folder_name)
assert scope_folder_set == folder_name, 'FOLDER NOT FOUND'

# get file names
flist = scope.ask('FILES:DIR?')
flist = flist.replace('\n', '')
flist = flist.split(',')
print('Found '+str(len(flist))+' files.')

flist = [f.split(' ')[-1] for f in flist] # remove the GPIB command

cntr_good = 0
for f in flist:
    if f[-4:-1] == file_format:
        cntr_good += 1
print('Found '+str(cntr_good)+' files matching the format.')

# let's copy
print('Reading files')
for f in flist:
    print('Transferring '+f)
    scope.write('FILES:READFile '+f)
    stream_out = scope.read_raw()

    fh = open(destination_dir+f.strip('"'), 'wb')
    fh.write(stream_out)
    fh.close()
