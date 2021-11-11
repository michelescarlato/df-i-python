# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# to run the bash command
import subprocess
import os, time

# Open the plain text file whose name is in textfile for reading.
#with open() as fp:
# Create a text/plain message
msg = EmailMessage()
#msg.set_content(fp.read())


commandHostname = 'hostname'
tempHostname = subprocess.Popen(commandHostname.split(), stdout=subprocess.PIPE)

hostname = str(tempHostname.communicate())
hostname = hostname.split("\n")
hostname = hostname[0].split('\\')


# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'Inodes problem on '+hostname[0].replace("(b'","")

# me == the sender's email address
# you == the recipient's email address
#msg['Subject'] = f'The contents of RRRR'
msg['From'] = "gcp-vms-maintenance@gmail.com"
msg['To'] = "michele.scarlato@gmail.com"

command = 'df -i'
temp = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# we use the communicate function
# to fetch the output
output = str(temp.communicate())
# splitting the output so that
# we can parse them line by line
output = output.split("\n")
output = output[0].split('\\')

for i in range(2):
    time.sleep(150)
    # a variable to store the output of ps aux
    res = []
    # iterate through the output
    # line by line
    for line in output:
        res.append(line)
    ps = subprocess.run(['ps', 'aux'], check=True, capture_output=True)
    processNames = subprocess.run(['grep', 'python3 Debian_license_collector.py'],
                                  input=ps.stdout, capture_output=True)
    pid = str(processNames.stdout)
    # pid = processNames.stdout.split("\n")
    pid = pid.split()
    pid = pid[1]
    pid = int(pid)

    # print the output
    for i in range(1, len(res) - 1):
        if "/dev/sda2" in res[i]:
            print(res[i])
            line = res[i].split()
            line[4] = line[4].replace("%","")
            line[4] = int(line[4])
            if line[4] > 28:
                # Send the message via our own SMTP server.
                s = smtplib.SMTP('localhost')
                s.send_message(msg)
                s.quit()
                print("Inodes issue")
                print("Killing python3 Debian_license_collector.py with PID "+str(pid))
                os.kill(pid, 9)
            else:
                print("Inodes ok")
