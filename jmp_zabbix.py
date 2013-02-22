#! /usr/bin/env python
#####################################################
#  Zabbix rleated operations: login, check hosts,   #
#  update hosts, update applicaitons                #
#####################################################

import zabbix_api
import socket
import os
import sys
import json
import socket
import logging
import jmp_constants
from zabbix_api import ZabbixAPI, ZabbixAPIException

#####################################################
#  Function reads the jmp.properties file and       #
#  returns username,password, agent.conf path       #
# input:  path to jmp.properties file               #
# output:  list [username, password, path ]         #
#####################################################
def jmp_info(name):
        datafile = file(name)
        if not datafile:
            logging.error('file was not found')
        else:
            z_data = {}
            logging.info('file was found')
            for line in datafile:
                if "#" in line:
                    continue
                elif "jmpEnabled" in line:
                    line = line.strip('\n')
                    line = line.split("jmpEnabled=")
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
#####################################################
#  Function reads the agentd.conf file and returns  #
#  Server, ServerActive, Hostname                   #
# input:  path to zabbix_agentd.conf file           #
# output:  list [Server, ServerActive, Hostname ]   #
#####################################################
def z_info(name):
        datafile = file(name)
        z_data = {}
        for line in datafile:
            if "#" in line:
                continue  
            elif "Server=" in line:
                line = line.strip('\n')
                line = line.split("Server=")
                z_data['Server'] = line[1]
            elif "ServerActive=" in line:
                line = line.strip('\n')
                line = line.split("ServerActive=")
                z_data['ServerActive'] = line[1]
            elif "Hostname=" in line:
                line = line.strip('\n')
                line = line.split("Hostname=")
                z_data['Hostname'] = line[1]
        return z_data
#####################End#############################
#####################################################
#  Function connects to Zabbix Server               #
# input:  void                                      #
# output:  Boolean                                  #
#####################################################
def z_logging():        
        status = None
        zabbix_info = {}
        zagent_info = {}
        zabbix_info = jmp_info('jmp.properties')
        print zabbix_info
        zagent_info = z_info(zabbix_info['jsb_z_agent_conf'])
        print zagent_info
        zabbix_server_username=zabbix_info['username']
        zabbix_server_password=zabbix_info['password']
        zabbix_server_url='http://'+ zagent_info['Server'] + '/zabbix'
        print zabbix_server_url
        z=zabbix_api.ZabbixAPI(server=zabbix_server_url)
        z.login(user=zabbix_server_username, password=zabbix_server_password)
        return z
#####################End#############################
#####################################################
#  Function Check for the JapserServer Hostgroup    #
# input:  Zabbix Handle                             #
# output:  True or false                            #
#####################################################
def z_checkHostgroup(zabbix_handler, hostGroupName):        
        hostgroups = zabbix_handler.hostgroup.get(
        {
        #'filter': { 'name': hostgroup}, 
        'output': 'extend'
        })
        print hostgroups
        for item in hostgroup:
                if hostGroupName:
                    print "JasperServers exist"
                    #print item
                    return True
                else:
                    print "JasperServer hostgroup is not there, talk to your system Administrator"
                    return False
#####################End#############################
#####################################################
#  Function Check for JTA JMX Template templateid   #
# input:  Zabbix Handle , Template name             #
# output:  TemplateID if template exist             #
#####################################################
def get_jta_templateid(zabbix_handler, template_name):
        jta_template = zabbix_handler.template.get(
            {
            'filter': { 'name': template_name}, 
            'output': 'extend'
            })
        #print "JTA TEMPLATE ID IS"
        #print jta_template[0]['templateid']
        logging.info("JTA Template id is for"+ template_name)
        logging.info(jta_template[0]['templateid'])
        return jta_template[0]['templateid']
#####################End#############################
#####################################################
#  Function Check for zabbix \   version            #
# input:  Zabbix Handle , Template name             #
# output:  Zabbix verison                           #
#####################################################
def get_zabbix_api_version(zabbix_handler):
            print zabbix_handler.api_version()
#####################End#############################

#####################################################
#  Function Check for JasperServer group            #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
#####################################################
#Check for HostGroup JasperServer or what ever the name is for JTA hosts
def get_jasper_groupid(zabbix_handler,groupName):
        hostgroups = zabbix_handler.hostgroup.get(
            {
            'output': 'extend'
            })
        print hostgroups
        for item in hostgroups:
            #item = [s.encode('utf-8') for s in item]
            print item['name']
            if item['name'] == "JasperServers":
                print item['groupid']
                logging.debug('JasperServers is found')
                return item['groupid']
            else:
                continue    
        print "can't find JasperServers Group"
        logging.error('Cannot find JasperServers Group please check your Zabbix installation')
        logging.error('#####################################################################')
        return 0
#####################End#############################
#####################################################
#  Function get the hosts list for jTA's group      #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
##################################################### 
def get_jasperhosts(zabbix_handler,hostsgroupID):
        jta_apps_hosts = []
        hosts = zabbix_handler.host.get(
            {
            'filter': { 'groupid': hostsgroupID}, 
            'output': 'extend'
            })
        for item in hosts:
            if "jta" in item['host']:
                #print item['host']
                #print item['hostid']
                jta_apps_hosts.append(item['host'].strip('\n'))
        jta_apps_hosts = [s.encode('utf-8') for s in jta_apps_hosts]
        logging.debug('#####################################################')
        logging.debug(jta_apps_hosts)
        return jta_apps_hosts
#####################End#############################
#####################################################
#  Function retrive the host interface info for JTA #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
##################################################### 
def get_hostinterface(zabbix_handler,hostsgroupID):
        hosts = zabbix_handler.host.get(
            {
            'filter': { 'groupid': hostsgroupID}, 
            'output': 'extend'
            })
        for item in hosts:
            if "jta" in item['host']:
                #print item['host']
                #print item['hostid']
                interface = zabbix_handler.hostinterface.get(
                {
                'filter': { 'hostid': item['hostid']}, 
                'output': 'extend'
                })
        #logging.debug('#####################################################')
        #logging.debug(jta_apps_hosts)
        return interface
#####################################################
#  Function retrive the host interface info for JTA #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
##################################################### 
def get_interface(zabbix_handler,hostID):
        interface = zabbix_handler.hostinterface.get(
                {
                'filter': { 'hostid': hostID}, 
                'output': 'extend'
                })
        #logging.debug('#####################################################')
        #logging.debug(jta_apps_hosts)
        return interface








