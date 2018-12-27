# Cisco Adaptive Security Appliance (ASA) 
https://www.cisco.com/c/en_in/products/security/adaptive-security-appliance-asa-software/index.html

### Overview

**Cisco ASA** Next-Generation Firewalls help you to balance security effectiveness with productivity. The solution offers the combination of the industry's most deployed stateful firewall with a comprehensive range of next-generation network security services. Protect your business with superior visibility and highly effective, threat-focused defense across the entire attack continuum. It provides comprehensive visibility, reduced cost and complexity, and real-time protection from malware and emerging threats.

All **Cisco ASA** Next-Generation Firewalls are powered by Cisco Adaptive Security Appliance (ASA) Software, with enterprise-class stateful inspection and next-generation firewall capabilities. ASA software can also be configured to Integration with other essential network security technologies.

#### PRE-REQUISITES to use Cisco ASA and DNIF  
Install netmiko python library for this Integration  
**`pip install netmiko`**  
Outbound access required for github to clone the plugin  
**Enable ssh path for Cisco ASA firewall**   

| Protocol   | Source IP  | Source Port  | Direction	 | Destination Domain | Destination Port  |  
|:------------- |:-------------|:-------------|:-------------|:-------------|:-------------|  
| TCP | DS,CR,A10 | Any | Egress	| github.com | 443 | 
| TCP | DS,CR,A10 | Any | Egress	| Cisco ASA FW | 443 |  

**Note** The above rule assumes both request and response in enabled  

### Cisco ASA trigger plugin functions  
Details of the function that can be used with the Cisco ASA is given in this section.  
[blocksource](#blocksource)  
[unblocksource](#unblocksource)  

### blocksource 
This function allows for a IP to be blocked on the Cisco ASA firewall .

#### Input  
- IP address

#### Example
```
_fetch $SrcIP from event where $Intel=True limit 1
>>_trigger api cisco-asa blocksource $SrcIP
```
  
#### Output  
  ![block_source](https://user-images.githubusercontent.com/37173181/50285438-38fee800-0482-11e9-9532-73f72adff375.jpg)

    
The output of the lookup call has the following structure (for the available data)
    
|     Field     |             Description              |
|---------------|--------------------------------------|
| $CISCOAPIStatus   | Returns Success/Failure status for blocking IP  |


### unblocksource
This function allows for an blocked IP to be released from the firewall

#### Input  
- IP address

#### Example
```
_fetch $SrcIP from event limit 1
>>_trigger api cisco-asa unblocksource $SrcIP
```  
#### Output  
  ![unblock_source](https://user-images.githubusercontent.com/37173181/50285638-d5c18580-0482-11e9-8015-3c923fcfad9c.jpg)

    
The output of the lookup call has the following structure (for the available data)
    
|     Field     |             Description              |
|---------------|--------------------------------------|
| $CISCOAPIStatus   | Returns Success/Failure status for releasing IP  |


### Using the Cisco ASA API and DNIF  
The Cisco ASA  API is found on github at 
https://github.com/dnif/trigger-cisco-asa

### Getting started with Cisco ASA API and DNIF

1. ####    Login to your Data Store, Correlator, and A10 containers.  
   [ACCESS DNIF CONTAINER VIA SSH](https://dnif.it/docs/guides/tutorials/access-dnif-container-via-ssh.html)
2. ####    Move to the `‘/dnif/<Deployment-key>/trigger_plugins’` folder path.
```
$cd /dnif/CnxxxxxxxxxxxxV8/trigger_plugins/
```
3. ####   Clone using the following command  
```  
git clone https://github.com/dnif/trigger-cisco-asa.git cisco-asa
```
4. ####   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/cisco-asa/’` folder path and open dnifconfig.yml configuration file     
    
   Replace the tag: <Add_your_cisco-asa_*> with your Cisco ASA details
```
trigger_plugin:
  CISCOASA_USER: <Add_your_cisco-asa_username>
  CISCOASA_PASS: <Add_your_cisco-asa_password>
  CISCOASA_SECRET: <Add_your_cisco-asa_enablepass/secret>
  CISCOASA_GROUP: <Add_your_cisco-asa_block>
  CISCOASA_FWIP: <Add_your_cisco-asa_firewall_IP>
```
