import boto3
import datetime
import os

ec2 = boto3.resource('ec2')


def lambda_handler(event, context):
    print("\n\nAWS snapshot backups starting at %s" % datetime.datetime.now())
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for instance in instances:
        instance_name = instance.tags[0]['Value']

        for volume in ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance.id]}]):
            description = '%s-%s-%s' % (instance_name, volume.volume_id,
                                        datetime.datetime.now().strftime("%Y%m%d"))

            # create ebs snapshots
            if volume.create_snapshot(
                    VolumeId=volume.volume_id,
                    Description=description,
                    TagSpecifications=[
                        {
                            'ResourceType': 'snapshot',
                            'Tags': [{'Key': 'CreatedBy', 'Value': 'timed_snapshot'}]
                        }
                    ]):
                print("Snapshot created with description [%s]" % description)

            # delete expired snapshot
            for snapshot in volume.snapshots.filter(
                    Filters=[
                        {
                            'Name': 'tag:CreatedBy',
                            'Values':
                                [
                                    'timed_snapshot'
                                ]
                        }
                    ]):
                # expried datetime
                retention_days = 7
                if datetime.datetime.now().replace(tzinfo=None) - snapshot.start_time.replace(
                        tzinfo=None) > datetime.timedelta(days=retention_days):
                    print("\t\tDeleting snapshot [%s - %s]" % (snapshot.snapshot_id, snapshot.description))
                    snapshot.delete()

    print("\n\nAWS snapshot backups completed at %s" % datetime.datetime.now())
    return True
