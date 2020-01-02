#
# Regex filter for real servers section in virtual ports
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

#
# Match real servers from the virtual port section
#


def rservers_filter(text):

    # text= ["\r\n    https: rport https, group 29, ewpcbcclu3web-443, health https (HTTPS),\
    #           \ pbind sslid, dbind\r\n        Real Servers:\r\n        2: 10.192.40.149,\
    #           \ ewpcbcclu3web01, group ena, health  (runtime HTTPS), 294 ms, UP\r\n\
    #           \        3: 10.192.40.150, ewpcbcclu3web02, group ena, health  (runtime\
    #           \ HTTPS), 218 ms, UP"]
    virtual_ports_tuples_dict = dict()
    real_servers_tuples_dict = dict()

    for idx, vports in enumerate(text):
        _v = virtual_ports_tuples_dict.update({idx: re.findall(
            r"\s+(?P<vport>\S+): rport\s(?P<rport>\S+) group\s(?P<vport_group>\d+).*", vports)})
        # _r = real_servers_tuples_dict.update({idx:re.findall(r"\s+(?P<rserver_instance>\d+):\s+(?P<rserver_name>\S+),\sbackup\s(?P<rserver_backup>\S+),\s(?P<rserver_response>\d+)\sms,\sgroup\s(?P<rserver_group_state>\S+),\s(?P<rserver_state>\S+).*", vports)})

        _r = real_servers_tuples_dict.update({idx: re.findall(
            r"\s+(?P<rserver_instance>\d+):\s+(?P<rserver_ip>\S+),\s+(?P<rserver_name>\S+),[\sbackup\s\d+,\s]{0,1}\sgroup\s(?P<rserver_group>\S+),.*(?P<rserver_response>\d+)\sms,.*.*", vports)})

    virtual_ports_dict = dict()

    for idx, vports in virtual_ports_tuples_dict.items():
        for v in vports:
            rserver_instances_list = []
            for rserver_idx, server in real_servers_tuples_dict.items():
                if rserver_idx == idx:
                    for r in server:
                        # _v = rserver_instances_list.append({"rserver_instance": r[0], "rserver_name": r[1], "rserver_backup": r[2], "rserver_response": r[3], "rserver_group_state": r[4], "rserver_state": r[5]})
                        _v = rserver_instances_list.append(
                            {"rserver_instance": r[0], "rserver_ip": r[1], "rserver_name": r[2], "rserver_group": r[3], "rserver_response": r[4]})
            _v = virtual_ports_dict.update({v[0]: {"virtual_port": v[0], "rport": v[1].replace(
                ',', ''), "group": v[2], "rserver": rserver_instances_list}})

    return virtual_ports_dict


class FilterModule(object):

    def filters(self):

        return {

            'rservers_filter': rservers_filter

        }
