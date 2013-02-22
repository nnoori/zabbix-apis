import socket

#####################################################
#  Function reads the agentd.conf file and returns  #
#  Server, ServerActive, Hostname                   #
# input:  path to zabbix_agentd.conf file           #
# output:  list [Server, ServerActive, Hostname ]   #
#####################################################
def z_info(name):
        datafile = file(name)
        z_data = []
        for line in datafile:
            if "#" in line:
                continue  
            elif "Server" in line:
            	z_data.append(line.lstrip("ServerActive="))
            elif "ServerActive" in line:
            	z_data.append(line.lstrip("Server="))
            elif "Hostname" in line:
            	z_data.append(line.lstrip("Hostname="))
        return z_data

#####################################################
#  Function reads the jmp.properties file and       #
#  returns Server, ServerActive, Hostname           #
# input:  path to zabbix_agentd.conf file           #
# output:  list [Server, ServerActive, Hostname ]   #
#####################################################
def z_log_info(name):
        datafile = file(name)
        z_data = []
        for line in datafile:
            if "username" in line:
            	line = line.strip('\n')
            	line = line.lstrip("username")
            	z_data.append(line.strip(' '))
            elif "password" in line:
            	line = line.strip('\n')
            	line = line.lstrip("password")
            	z_data.append(line.strip(' '))
            elif "z_agent_conf" in line:
            	line = line.strip('\n')
            	line = line.lstrip("z_agent_conf")
            	z_data.append(line.strip(' '))
        return z_data

#####################################################
#  Function returns the hostname of OS - hostname   #
#####################################################

def sys_hostname():
		if socket.gethostname().find('.')>=0:
		    name=socket.gethostname()
		    return "if " + name
		else:
		    name=socket.gethostbyaddr(socket.gethostname())[0]
		    return name


def jmp_info(name):
        datafile = file(name)
        z_data = {}
        for line in datafile:
            if "#" in line:
                print line
                continue
            elif "jmpEnabled" in line:
                line = line.strip('\n')
                line = line.split("jmpEnabled=")
                print line
                z_data['jmpEnabled'] = line[1]
            elif "username" in line:
                line = line.strip('\n')
                line = line.split("username=")
                z_data['username'] = line[1]
            elif "password=" in line:
                line = line.strip('\n')
                line = line.split("password=")
                z_data['password'] = line[1]
            elif "jsb_z_agent_conf" in line:
                line = line.strip('\n')
                line = line.split("jsb_z_agent_conf=")
                z_data['jsb_z_agent_conf'] = line[1]
            elif "jta_z_agent_conf" in line:
                line = line.strip('\n')
                line = line.split("jta_z_agent_conf=")
                z_data['jta_z_agent_conf'] = line[1]
            elif "jmp_template" in line:
                line = line.strip('\n')
                line = line.split("jmp_template=")
                z_data['jmp_template'] = line[1]
            elif "jasper_home" in line:
                line = line.strip('\n')
                line = line.split("jasper_home=")
                z_data['jasper_home'] = line[1]
            elif "jsb.jmxremote" in line:
                line = line.strip('\n')
                line = line.split("jsb.jmxremote=")
                z_data['jsb.jmxremote'] = line[1]
            elif "jsbHostGroup" in line:
                line = line.strip('\n')
                line = line.split("jsbHostGroup=")
                z_data['jsbHostGroup'] = line[1]
            elif "jtaHostGroup" in line:
                line = line.strip('\n')
                line = line.split("jtaHostGroup=")
                z_data['jtaHostGroup'] = line[1]
        return z_data
#####################End#############################
z_info = jmp_info('jmp.properties')
print z_info

