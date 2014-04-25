"""
Alldebrider.py: returns alldebrid link from standard hosting link

Requires: Alldebrid valid account

"""

import os
import sys
import logging
import urllib2
import argparse
import ConfigParser

class LinkException(Exception):
    """ Handle Alldebrid link exceptions """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Alldebrider(object):
    """ Handle debrid request """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_debrided_link(self, link):
        """ 
        Returns a alldebrided link from a standard hosting service link 
        """
        alldebrid_url = "https://www.alldebrid.com/service.php?pseudo=%s&password=%s&link=%s&view=1"
        
        response = urllib2.urlopen(alldebrid_url % (self.username, self.password, urllib2.quote(link)))
        response_content = response.read() 

        if "Link is dead" in response_content:
            raise LinkException("Link is dead")

        if "Invalid" in response_content:
            raise LinkException("Invalid link")

        return response_content


if __name__ == "__main__":
  
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)

    # parse command line arguments
    parser = argparse.ArgumentParser(prog='alldebrider')
    parser.add_argument('--url', help='input url')
    parser.add_argument('--conf', help='config file (default: ~/.alldebrid)', default="~/.alldebrid")
    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(os.path.expanduser(args.conf)):
        logging.error("Unable to find config file: %s" % args.conf)
        sys.exit(1)

    # get credentials from config file
    try:
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.expanduser(args.conf))
        username = conf.get("credentials","username")
        password = conf.get("credentials","password")
    except ConfigParser.Error as e:
        logging.error("""Unable to parse config file. 
Please make sure your config file format is the following:\n
[credentials]
username = yourusername
password = yourpassword""")
        sys.exit(1)
    
    # get a debrided link from a standard hosting service link
    try:
        debrider = Alldebrider(username, password)
        debrided_link = debrider.get_debrided_link(args.url)
        logging.info("Got debrided link: %s" % debrided_link)

        print debrided_link

    except LinkException as e:
        logging.error(e.value)
        sys.exit(1)
