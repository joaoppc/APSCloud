import boto3
from botocore.exceptions import ClientError
import json



key_pair_name = "joaoppcCloud"
security_group = "APSjoaoppc"
ec2 = boto3.client('ec2')

keypairJson = ec2.describe_key_pairs()
response = ec2.describe_vpcs()
ec2_2 = boto3.resource('ec2', region_name="us-east-1")
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
ip_publico={}

for instance in ec2_2.instances.all():
	if instance.tags is None:
		continue
	for tag in instance.tags:
		if tag['Key'] == 'Owner' and tag['Value']=='joaoppc' and instance.state['Name']=='running':
			instance.terminate()
			print('instance terminated')
			ip_publico[instance.instance_id]=instance.public_ip_address
			print(ip_publico)
			instance.wait_until_terminated()

for i in range(len(keypairJson['KeyPairs'])):
	if key_pair_name in keypairJson['KeyPairs'][i]['KeyName']:
		ec2.delete_key_pair(KeyName=key_pair_name)
		print('keypair deleted')
		#print(keypairJson['KeyPairs'])
		key_pair = ec2.create_key_pair(KeyName=key_pair_name)
		print('keypair created')

try:
	sec_groups = ec2.describe_security_groups()
	for j in range(len(sec_groups['SecurityGroups'])):
		if security_group in sec_groups['SecurityGroups'][j]['GroupName']:
			sec_group_id = sec_groups['SecurityGroups'][j]['GroupId']
			#print(sec_groups['SecurityGroups'][j]['GroupName'])
			#print(sec_groups['SecurityGroups'][j]['GroupId'])
			ec2.delete_security_group(GroupId=sec_group_id)
			print('Security Group Deleted')
			response = ec2.create_security_group(GroupName=security_group,
										  Description='APS',
										  VpcId=vpc_id)
			security_group_id = response['GroupId']
			#print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
			data = ec2.authorize_security_group_ingress(
			GroupId=security_group_id,
			IpPermissions=[
			{'IpProtocol': 'tcp',
			 'FromPort': 5000,
			 'ToPort': 5000,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
			{'IpProtocol': 'tcp',
			 'FromPort': 22,
			 'ToPort': 22,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
		])
	print('Ingress Successfully Set %s' % data)

			
except ClientError as e:
	print(e)

outfile = open('joaoppcCloud.pem','w')
KeyPairOut = str(key_pair['KeyMaterial'])
outfile.write(KeyPairOut)
print('chave salva como joaoppcCloud.pem')

instances = ec2_2.create_instances(
	ImageId='ami-0ac019f4fcb7cb7e6', 
	MinCount=1, 
	MaxCount=3,
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
				pip install pyrebase
				cd /APSCloud
				python server.py ''',
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
print('instance launched')
for instance in ec2_2.instances.all():
	if instance.tags is None:
		continue
	for tag in instance.tags:
		if tag['Key'] == 'Owner' and tag['Value']=='joaoppc' and instance.state['Name']=='running':
			instance.wait_until_running()
			print('intance launched %s',instance.instance_id)

for instance in instances:
	print(instance.id, instance.instance_type)

