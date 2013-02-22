#! /usr/bin/env python
#####################################################
#  The script here checks the JTA's anchor files in #
#  Mule/apps folder                                 #
#####################################################
import os
import logging
#####################################################
#  Function to save the JTA deployed in             #
# JTA_List.txt  file                                #
# output:  file JTA_List.txt                        #
#####################################################
def get_apps_list(jasper_home_dir):
		app_list = []
		dir_list = []
		#Path for the Mule App's folder 
		dir_list =  os.listdir(jasper_home_dir + "/jsb-core/mule-standalone-3.3.0/apps/")
		app_list_file = open('jta_list.txt','w')
		for item in dir_list:
			if "txt" in item:
				app_list_file.write(item.strip('-anchor.txt') + os.linesep)
				app_list.append(item.strip('-anchor.txt'))
		app_list_file.close()
		print app_list
		#logging.debug(app_list)
		return app_list
#####################End#############################
#####################################################
#  Function to update list of JTA deployed in       #
# JTA_List.txt  file                                #
# output:  file JTA_List.txt                        #
#####################################################
def update_apps_list(current_apps_list):
		app_list = []
		#Path for the Mule App's folder 
		app_list_file = open('jta_list.txt','w')
		#clear the jta's list to accomedate the latest
		app_list_file.truncate()
		for item in current_apps_list:
				app_list_file.write(item + os.linesep)
				app_list.append(item)
		print "UPDATED APPS LIST"
		#logging.debug("UPDATED APPS LIST")
		print current_apps_list
		#logging.debug(current_apps_list)
		app_list_file.close()
		return 
#####################End#############################
#####################################################
#  Function to check if a new JTA was deployed      #
#  or undeployed                                    #
# input:  void                                      #
# output:  list fo the new JTA's                    #
#####################################################
def get_apps_diff():
		apps_list = []
		deployed_apps = []
		deleted_apps = []
		dir_app_list = []
		current_app_list = []
		f = open("jta_list.txt")
		#Load the JTA's list from JTA_List file to check if new apps were deployed or undeployed
		apps_list = f.readlines()
		for item in  apps_list:
			apps_list[apps_list.index(item)] = item.strip('\n')
		f.close()
		#Get currently deployed JTA's 
		dir_app_list =  os.listdir("jasper/jasper-1.1/jsb-core/mule-standalone-3.3.0/apps/")
		for item in dir_app_list:
			if "txt" in item:
				current_app_list.append(item.strip('-anchor.txt'))
		#print "Saved Apps List:::"
		#print apps_list
		#print "Current app list:::"
		#print current_app_list
		logging.debug("Saved Apps List:::")
		logging.debug(apps_list) 
		logging.debug("Current app list:::") 
		logging.debug(current_app_list)
		# Saved list fo the JTA
		set1 = set(apps_list)
		#List of the current JTA's the Mule/Apps folder 
		set2 = set(current_app_list)
		#chceck for deployed/deleted JTA's
		if set2.difference(set1):
			deployed_apps = set2.difference(set1)
			#print "Deployed Apps List:::"
			logging.debug("Deployed Apps List:::")
			#print list(deployed_apps)
			logging.debug(list(deployed_apps))
			update_apps_list(current_app_list)
			return {'deployed_apps': deployed_apps, 'deleted_apps' : deleted_apps, 'apps_list' : apps_list}
		elif set1.difference(set2):
			deleted_apps = set1.difference(set2)
			#print "Deleted Apps List:::"
			#print list(deleted_apps)
			logging.debug("Deleted Apps List:::")
			logging.debug(list(deleted_apps))
			#Update the list fo the saved apps
			update_apps_list(current_app_list)
			return {'deployed_apps': deployed_apps, 'deleted_apps' : deleted_apps, 'apps_list' : apps_list}
		else:
			#print "No JTA deployed or deleted"
			logging.debug("No JTA deployed or deleted")
			return {'deployed_apps': deployed_apps, 'deleted_apps' : deleted_apps, 'apps_list' : apps_list}
	#####################End#############################

