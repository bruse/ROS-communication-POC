#!/usr/bin/env python
import roslib; roslib.load_manifest('testserver')
import rospy
from std_msgs.msg import String
from rospy.impl.tcpros_base import TCPROSTransport
from rospy.impl.tcpros_base import TCPROSTransportProtocol
import md5

class TestServerProtocol(TCPROSTransportProtocol):
  def __init__(self):
    super(TestServerProtocol, self).__init__("testprotocol", String)

  def get_header_fields(self):
    return {'type': 'testprotocol',
            'md5sum': md5.new('testprotocol').digest()}
