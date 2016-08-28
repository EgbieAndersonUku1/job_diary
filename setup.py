import os

# check python implementation
answer = input('[+] Would you like to run setup in a virtual environment (y/n) : ')
if answer.lower() == 'y':
    while True:
        name = raw_input('[+] Enter the name for the virtual environment : ')
        if name:
            break
    command = os.popen('virtualenv -p python {}'.format(os.path.join(os.getcwd(), name))
    print 'Open'
