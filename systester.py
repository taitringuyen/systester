#!/usr/bin/python

import sys, os
import getopt, getpass
import pexpect
import re, time

def main():
  print "System tester"

  user = "amcclab"
  host = "10.76.213.10"
  password = "amcc1234"
  host_cmd_prompt = "\[PEXPECT\]\$ "
  iteration_time = 30

  # Login via SSH
  child = pexpect.spawn('ssh -l %s %s'%(user, host))
  print "SSH connected to %s" %(host)

  # Set command prompt to something more unique
  child.sendline("PS1='[PEXPECT]\$ '") # try sh style
  e = child.expect([pexpect.TIMEOUT, host_cmd_prompt], timeout = 10)
  if e == 0:
    print "# Couldn't set sh-style prompt -- trying csh-style."
    child.sendline("set prompt='[PEXPECT]\$ '")
    e = child.expect([pexpect.TIMEOUT, host_cmd_prompt], timeout = 10)
    if e == 0:
      print("Failed to set command prompt using sh or csh style.")
      print(child.before)
      sys.exit(1)

  # we should be at commad prompt and ready to run some commands
  print('---------------------------------------')
  print('Report of commands run on remote host.')
  print('---------------------------------------')

  child.sendline ('uname -a')
  child.expect(host_cmd_prompt)
  print(child.before)
  if 'linux' in child.before.lower():
    print "Good starting point"

  '''
  Start power cycle test
    - Enable capturing the SUT console
    - Power on SUT
    - Wait for the iteration timeout
    - Power off SUT
  '''
  # Enable capturing SUT console
  child.sendline('sudo cat /dev/ttyUSB1')
  e = child.expect([pexpect.TIMEOUT, "[sudo] password for amcclab:"], timeout = 10)
  if e == 0:
    print "password required"
    child.sendline(password)
  print "reading now..."
  # TODO: Power on SUT

  # Wait for the iteration timeout
  time.sleep(teration_time)
  # TODO: Power off SUT

  # Finish
  child.sendcontrol('c') #ctrl-c
  child.expect(host_cmd_prompt)
  print(child.before)

if __name__ == "__main__":
  main();
