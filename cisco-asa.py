from netmiko import ConnectHandler
import yaml
import os
import logging

path = os.environ["WORKDIR"]

try:
    with open(path + "/trigger_plugins/cisco-asa/dnifconfig.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        asauser = cfg['trigger_plugin']['CISCOASA_USER']
        asapass = cfg['trigger_plugin']['CISCOASA_PASS']
        asagroup = cfg['trigger_plugin']['CISCOASA_GROUP']
        asaip = cfg['trigger_plugin']['CISCOASA_FWIP']
        asasec = cfg['trigger_plugin']['CISCOASA_SECRET']
except Exception,e:
    logging.error("CISCO ASA API Error in reading local DNIF Config File {}".format(e))


def unblocksource(inward_array, var_array):
    var_array[0] = var_array[0].replace(" ", "")
    # Getting the user credential
    device = {
        'device_type': 'cisco_asa',
        'ip': asaip,
        'username': asauser,
        'password': asapass,
        'secret': asasec
    }
    for i in inward_array:
        try:
            if var_array[0] in i:
                try:
                    # Establishing SSH connection
                    ssh_connect = ConnectHandler(**device)
                except Exception,e:
                    logging.error("CISCO-ASA trigger-plugin unable to establish SSH connection: >>>{}<<<".format(e))
                    i["$CISCOAPIStatus"]= "Failed to connect with CISCO-ASA Firewall"
                ipsrc = str(i[var_array[0].replace(" ","")])
                logging.info(var_array)
                logging.info(i)
                try:
                    commands = ['object-group network ' + asagroup, 'no network-object host ' + ipsrc]
                    output = ssh_connect.send_config_set(commands)
                    output = ssh_connect.send_command("write mem")
                    logging.info("CISCO-ASA Output {}".format(output))
                    ssh_connect.disconnect()
                    logging.warning("CISCO-ASA Output {}".format(ssh_connect))
                    i["$CISCOAPIStatus"] = "IP released from CISCO-ASA"
                except Exception,e:
                    logging.error("CISCO-ASA API Error {}".format(e))
                    i["$CISCOAPIStatus"] = "Failed to release IP CISCO-ASA"
        except Exception,e:
            logging.error("CISCO-ASA API error %s"% e)
    return inward_array


def blocksource(inward_array, var_array):
    var_array[0] = var_array[0].replace(" ", "")
    # Getting the user credential
    device = {
        'device_type': 'cisco_asa',
        'ip': asaip,
        'username': asauser,
        'password': asapass,
        'secret': asasec
    }
    for i in inward_array:
        try:
            if var_array[0] in i:
                try:
                    # Establishing SSH connection
                    ssh_connect = ConnectHandler(**device)
                except Exception,e:
                    logging.error("CISCO-ASA trigger-plugin unable to establish SSH connection: >>>{}<<<".format(e))
                    i["$CISCOAPIStatus"]= "Failed to connect with CISCO-ASA Firewall"
                ipsrc = str(i[var_array[0].replace(" ","")])
                logging.warning(var_array)
                logging.warning(i)
                try:
                    commands = ['object-group network ' + asagroup, 'network-object host ' + ipsrc]
                    output = ssh_connect.send_config_set(commands)
                    output = ssh_connect.send_command("write mem")
                    logging.warning("CISCO-ASA Output {}".format(output))
                    ssh_connect.disconnect()
                    i["$CISCOAPIStatus"] = "Blocked on CISCO-ASA"
                except Exception,e:
                    logging.error("CISCO-ASA API Error {}".format(e))
                    i["$CISCOAPIStatus"] = "Failed to block on CISCO-ASA"
        except Exception,e:
            logging.error("CISCO-ASA API error %s"% e)
    return inward_array
