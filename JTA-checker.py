#! /usr/bin/env python

import os

#####################################################
#  Function to save the JTA deployed in             #
# JTA_List.txt  file                                #
# output:  file JTA_List.txt                        #
#####################################################
def get_apps_list():
		app_list = []
		dir_list = []
		#Path for the Mule App's folder 
		dir_list =  os.listdir("jasper/jasper-1.1/jsb-core/mule-standalone-3.3.0/apps/")
		print "DIR LIST"
		#print dir_list
		app_list_file = open('JTA_List.txt','w')
		for item in dir_list:
			if "txt" in item:
				#print item.strip('-anchor.txt')
				app_list_file.write(item.strip('-anchor.txt') + os.linesep)
				app_list.append(item.strip('-anchor.txt'))
		#print app_list
		app_list_file.close()
		return app_list
#####################End#############################
#####################################################
#  Function to update list of JTA deployed in       #
# JTA_List.txt  file                                #
# output:  file JTA_List.txt                        #
#####################################################
def update_apps_list(current_apps_list):
		app_list = []
		current_apps_list = []
		#Path for the Mule App's folder 
		dir_list =  os.listdir("jasper/jasper-1.1/jsb-core/mule-standalone-3.3.0/apps/")
		app_list_file = open('JTA_List.txt','w')
		for item in current_apps_list:
				app_list_file.write(item + os.linesep)
				app_list.append(item)
		print "UPDATED APPS LIST"
		print app_list
		app_list_file.close()
		return app_list
#####################End#############################
#####################################################
#  Function to check if a new JTA was deployed      #
#  or undeployed                                    #
# input:  void                                      #
# output:  list fo the new JTA's                    #
#####################################################
def get_apps_diff():
		apps_list = []
		f = open("JTA_List.txt")
		#Load the JTA's list from JTA_List file to check if new apps were deployed or undeployed
		apps_list = f.readlines()
		for item in  apps_list:
			apps_list[apps_list.index(item)] = item.strip('\n')
		f.close()
		dir_app_list = []
		current_app_list = []
		#Get currently deployed JTA's 
		dir_app_list =  os.listdir("jasper/jasper-1.1/jsb-core/mule-standalone-3.3.0/apps/")
		for item in dir_app_list:
			if "txt" in item:
				current_app_list.append(item.strip('-anchor.txt'))
		print "Saved Apps List:::"
		print apps_list
		print "Current app list:::"
		print current_app_list
		# Saved list fo the JTA
		set1 = set(apps_list)
		#List of the current JTA's the Mule/Apps folder 
		set2 = set(current_app_list)
		#chceck for deployed/deleted JTA's
		if not (set2.difference(set1) and set1.difference(set2)):
			print "No JTA deployed or deleted"
		else: 
			deployed_apps = set2.difference(set1)
			if deployed_apps:
				print list(deployed_apps)
				print "Go Add Applicaiton within JTA Server and update JTA_List.txt"
			deleted_apps = set1.difference(set2)
			if deleted_apps:
				print list(deleted_apps)
				print "Update the save list inside the JTA_List.txt"
		return apps_list
#####################End#############################
get_apps_diff()


