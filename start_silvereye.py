import json
import sys
import os
from Core.SilverEyeCore import SilverEye


def main(argv):
    if len(argv)<1:
        show_error_message_and_exit()

    inputfile = str(argv[0])

    if len(inputfile)<1:
        show_error_message_and_exit()

    with open(os.path.dirname(os.path.dirname(__file__)) +inputfile, 'r') as f:
        config = json.load(f)
        database_name = config['database_name']
        database_ip = config['database_ip']
        database_port = config['database_port']

    if database_name is None or database_ip is None or database_port is None or len(database_name) < 1 or \
            len(database_ip) < 1 or database_port < 1:
        print "Bad config file"
        sys.exit()

    silver_eye = SilverEye(database_ip, database_port, database_name)

    my_input = raw_input("Please press enter to start")
    silver_eye.start()

    my_input = raw_input("Please press enter to stop")
    silver_eye.stop()
def show_error_message_and_exit():
    print "Bad source config file"
    print "Please: python start_silvereye <config_file_source>"
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])