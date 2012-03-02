#!/usr/bin/env python
import roslib; roslib.load_manifest('testserver')
import rospy
from std_msgs.msg import String
from rospy.impl.tcpros_base import TCPROSTransport
from rospy.impl.tcpros_base import TCPROSTransportProtocol
from prot import TestServerProtocol

import sys

PORT = 2048

if __name__ == "__main__":
  t = TCPROSTransport(TestServerProtocol(), "testservice")
  t.connect("127.0.0.1", PORT, "testservice_connection")

  msg = String()
  seq = 0
  while True:
    # Send line from stdin
    line = sys.stdin.readline()
    if not line:
      break;

    msg.data = line[:-1]
    t.send_message(msg, seq)
    seq+=1

    # Print response
    print t.receive_once()
