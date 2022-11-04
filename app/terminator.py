import os
import time
import boto3
import requests

url="http://169.254.169.254/latest/dynamic/instance-identity/document"

def get_current_instance_details():
    metadata = requests.get(url).json()
    return metadata["region"], metadata["instanceId"]

def calculate_time(modified_time):
    seconds = int(time.time() - modified_time)
    return (seconds / (60 * 60))

def stop_current_instance(region, instance_id):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=[instance_id])

def terminate(monitor_file, shutdown_time):
    while True:
        if os.path.exists(monitor_file):
            modified_time = os.path.getmtime(monitor_file)
            hours = calculate_time(modified_time)
            if hours >= shutdown_time:
                region, instance_id = get_current_instance_details()
                stop_current_instance(region, instance_id)
        time.sleep(10)