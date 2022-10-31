import os
import time
import boto3
import requests

def terminate(monitor_file, shutdown_time):
    while True:
        modified_time = os.path.getmtime(monitor_file)
        seconds = int(time.time() - modified_time)
        hours = seconds / (60 * 60)
        if hours >= shutdown_time:
            metadata = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document").json()
            ec2 = boto3.client('ec2', region_name=metadata["region"])
            ec2.stop_instances(InstanceIds=[metadata["instanceId"]])
        time.sleep(10)