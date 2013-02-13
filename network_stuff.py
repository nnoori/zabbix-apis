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

z_info = z_log_info('jmp.properties')
print z_info

