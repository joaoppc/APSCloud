import boto3
from botocore.exceptions import ClientError
import json
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
import requests
import threading
import time



ec2 = boto3.client('ec2')
ec2_2 = boto3.resource('ec2', region_name="us-east-1")

app = Flask(__name__, static_url_path="")
api = Api(app)

ip_publico={}
key_pair_name = "joaoppcCloud"
security_group = "APSjoaoppc"

for instance in ec2_2.instances.all():
	if instance.tags is None:
		continue
	for tag in instance.tags:
		if tag['Key'] == 'Owner' and tag['Value']=='joaoppc' and instance.state['Name']=='running':
			ip_publico[instance.instance_id]=instance.public_ip_address
			

if __name__ == '__main__':
	outfile2 = open('iplist.json','w')
	ipjson = str(json.dumps(ip_publico))
	outfile2.write(ipjson)

	def req0():
		req0 = str(requests.get("http://" + list(ip_publico.values())[0] + ":5000/healthcheck"))
		try:
			while req0 == '<Response [200]>':
				#time.sleep(1)
				
					print(str(requests.get("http://" + list(ip_publico.values())[0] + ":5000/healthcheck"))+list(ip_publico.values())[0])
		except:		
			print('error'+list(ip_publico.values())[0])
			print()
			for instance in ec2_2.instances.all():
				print(list(ip_publico.values())[0])
				if instance.public_ip_address == list(ip_publico.values())[0]:
					instance.terminate()
					del ip_publico[instance.instance_id]
					print('terminated')
					instance.wait_until_terminated()
					print('creating')
					new_instance = ec2_2.create_instances(
						ImageId='ami-0ac019f4fcb7cb7e6', 
						MinCount=1, 
						MaxCount=1,
						KeyName=key_pair_name,
						InstanceType="t2.micro",
						SecurityGroups=[security_group] ,
						UserData='''#!/bin/sh

									git clone https://github.com/joaoppc/APSCloud
									apt-get install software-properties-common -y
									apt-add-repository universe
									apt-get update
									apt-get install python-pip -y
									pip install Flask 
									pip install flask_restful 
									pip install flask_httpauth
									cd /APSCloud
									python serverAPS.py ''',
						TagSpecifications=[
							{
								'ResourceType': 'instance',
								'Tags': [
									{
										'Key': 'Owner',
										'Value': 'joaoppc'
									},
								]
							},
						],
					)
					print('created')
					new_instance.wait_until_running()
					ip_publico[new_instance.instance_id] = new_instance.public_ip_address
					print('added')
					req0()
				 

	def req1():
		req1 = str(requests.get("http://" + list(ip_publico.values())[1] + ":5000/healthcheck"))
		try:
			while req1 == '<Response [200]>':
			
				#time.sleep(1)
				print(str(requests.get("http://" + list(ip_publico.values())[1] + ":5000/healthcheck"))+list(ip_publico.values())[1])
		except:		
			print('error'+list(ip_publico.values())[1])
			for instance in ec2_2.instances.all():
				print(list(ip_publico.values())[1])
				if instance.public_ip_address == list(ip_publico.values())[1]:
					instance.terminate()
					print('terminated')
					del ip_publico[instance.instance_id]
					instance.wait_until_terminated()
					print('creating')
					new_instance = ec2_2.create_instances(
						ImageId='ami-0ac019f4fcb7cb7e6', 
						MinCount=1, 
						MaxCount=1,
						KeyName=key_pair_name,
						InstanceType="t2.micro",
						SecurityGroups=[security_group] ,
						UserData='''#!/bin/sh

									git clone https://github.com/joaoppc/APSCloud
									apt-get install software-properties-common -y
									apt-add-repository universe
									apt-get update
									apt-get install python-pip -y
									pip install Flask 
									pip install flask_restful 
									pip install flask_httpauth
									cd /APSCloud
									python serverAPS.py ''',
						TagSpecifications=[
							{
								'ResourceType': 'instance',
								'Tags': [
									{
										'Key': 'Owner',
										'Value': 'joaoppc'
									},
								]
							},
						],
					)
					print('created')
					new_instance.wait_until_running()
					ip_publico[new_instance.instance_id] = new_instance.public_ip_address
					print('added')
					req1()

	def req2():
		req2 = str(requests.get("http://" + list(ip_publico.values())[2] + ":5000/healthcheck"))
		try:
			while req2 == '<Response [200]>':
			#time.sleep(1)
			
				print(str(requests.get("http://" + list(ip_publico.values())[2] + ":5000/healthcheck"))+list(ip_publico.values())[2])
		except:		
			print('error'+list(ip_publico.values())[2])
			for instance in ec2_2.instances.all():
				print(list(ip_publico.values())[2])
				if instance.public_ip_address == list(ip_publico.values())[2]:
					instance.terminate()
					print('terminated')
					del ip_publico[instance.instance_id]
					instance.wait_until_terminated()
					print('creating')
					new_instance =ec2_2.create_instances(
						ImageId='ami-0ac019f4fcb7cb7e6', 
						MinCount=1, 
						MaxCount=1,
						KeyName=key_pair_name,
						InstanceType="t2.micro",
						SecurityGroups=[security_group] ,
						UserData='''#!/bin/sh

									git clone https://github.com/joaoppc/APSCloud
									apt-get install software-properties-common -y
									apt-add-repository universe
									apt-get update
									apt-get install python-pip -y
									pip install Flask 
									pip install flask_restful 
									pip install flask_httpauth
									cd /APSCloud
									python serverAPS.py ''',
						TagSpecifications=[
							{
								'ResourceType': 'instance',
								'Tags': [
									{
										'Key': 'Owner',
										'Value': 'joaoppc'
									},
								]
							},
						],
					)
					print('created')
					new_instance.wait_until_running()
					ip_publico[new_instance.instance_id] = new_instance.public_ip_address
					print('added')
					req2()		


	t0 = threading.Timer(1.0,req0)
	t1 = threading.Timer(1.0,req1)
	t2 = threading.Timer(1.0,req2)
	

	t0.start()
	t1.start()
	t2.start()


#print(ipjson)