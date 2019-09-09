import boto3
import datetime
import os

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    print("\n\nAWS snapshot backups starting at %s" % datetime.datetime.now())
    instances = ec2.instances.filter(
        InstanceIds=['i-04b2fd1458c42c890']
    )
    
    for instance in instances:
        instance_name = instance.tags[0]['Value']

        for volume in ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance.id]}]):
            description = '%s-%s-%s' % (instance_name, volume.volume_id, 
                datetime.datetime.now().strftime("%Y%m%d"))
                
            # create ebs snaphost
            if volume.create_snapshot(VolumeId=volume.volume_id, Description=description):
                print("Snapshot created with description [%s]" % description)

    print("\n\nAWS snapshot backups completed at %s" % datetime.datetime.now())
    return True