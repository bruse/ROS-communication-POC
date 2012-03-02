#!/usr/bin/env python
# Author: Andreas Bruse
# Description:
# Quick and dirty server for testing the feasability of writing the network
# code using ros. If anything real would ever come out of this, the
# TCPServer.run() function should probably be re-implemented here to
# work properly with select, so that we wont need that useless thread
# causing race conditions.

import roslib; roslib.load_manifest('testserver')
import rospy
from std_msgs.msg import String
from rospy.impl.tcpros_base import TCPServer
from rospy.impl.tcpros_base import TCPROSTransport
from rospy.impl.tcpros_base import TCPROSTransportProtocol

from prot import TestServerProtocol

import select

PORT = 2048

inputs = []

def inbound_handler(sock, addr):
  print "%s connected." % (str(addr))

  t = TCPROSTransport(TestServerProtocol(), "testservice")
  t.set_socket(sock, "client")
  t.write_header()	
  t.read_header()

  inputs.append(sock)

if __name__ == '__main__':
  s = TCPServer(inbound_handler, PORT)	
  s.start()

  while True:
    inputready,outputready,exceptready = select.select(inputs, [], [], 1)
    for s in inputready:
      # s is really just a python socket, but let's use
      # ROS to parse the message and write a response
      t = TCPROSTransport(TestServerProtocol(), "testservice")
      t.set_socket(s, "client")
      try:
        data = t.receive_once()

        # Echo all messages
        seq = 0
        for msg in data:
          msg.data = "This is a reply of the message '%s'." % (msg.data)
          t.send_message(msg, seq)
          seq += 1

        print "Echoed data"
      except rospy.exceptions.TransportTerminated:
        print "Closing connection"
        s.close()
        inputs.remove(s)
      except rospy.exceptions.TransportException:
        print "Error from client. Closing connection."
        s.close()
        inputs.remove(s)
