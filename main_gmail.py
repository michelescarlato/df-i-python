# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage
from dotenv import load_dotenv

# to run the bash command
import subprocess
import os, time


load_dotenv()


gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

commandHostname = 'hostname'
tempHostname = subprocess.Popen(commandHostname.split(), stdout=subprocess.PIPE)

hostname = str(tempHostname.communicate())
hostname = hostname.split("\n")
hostname = hostname[0].split('\\')


sent_from = gmail_user
to = [os.getenv('RECIPIENT')]#['recipient@gmail.com']
subject = 'Inodes problem on '+hostname[0].replace("(b'","")
body = 'Inodes warning ... and process killed.'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)




command = 'df -i'
temp = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# we use the communicate function
# to fetch the output
output = str(temp.communicate())
# splitting the output so that
# we can parse them line by line
output = output.split("\n")
output = output[0].split('\\')

for i in range(3):
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
        if "/dev/nvme0n1p5" in res[i]:
            print(res[i])
            line = res[i].split()
            line[4] = line[4].replace("%","")
            line[4] = int(line[4])
            if line[4] > 70:
                # Send the message via our own SMTP server.
                try:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, email_text)
                    server.close()
                    print ('Email sent!')
                except:
                    print ('Something went wrong...')

                print("Inodes issue")
                print("Killing python3 Debian_license_collector.py with PID "+str(pid))
                os.kill(pid, 9)
            else:
                print("Inodes ok")
