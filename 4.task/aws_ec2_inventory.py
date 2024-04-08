#!/usr/bin/env python
import boto3
import json

def get_ec2_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'id': instance['InstanceId'],
                'private_ip': instance['PrivateIpAddress'],
                'public_ip': instance.get('PublicIpAddress', 'N/A'),
                'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            })
    return instances

def main():
    # Define the AWS regions you want to include in the inventory
    regions = ['ap-south-1']  # Add more regions if needed

    inventory = {'_meta': {'hostvars': {}}}
    for region in regions:
        instances = get_ec2_instances(region)
        inventory[region] = {'hosts': [instance['id'] for instance in instances]}
        for instance in instances:
            inventory['_meta']['hostvars'][instance['id']] = {
                'ansible_host': instance['public_ip'] if instance['public_ip'] != 'N/A' else instance['private_ip'],
                'private_ip': instance['private_ip'],
                'tags': instance['tags']
            }

    print(json.dumps(inventory))

if __name__ == '__main__':
    main()

