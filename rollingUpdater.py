'''
Python script that does a rolling restart of an auto scaling group.
It does this to deploy a new build assuming the instances have a startup script to deploy from the S3
'''

import subprocess
import os,sys
import collections
import time

asCommandArgs = [
  '--access-key-id=aaaa',
  '--secret-key=bbbb',
  '--region=us-west-2',
]

EC2 = collections.namedtuple('EC2', ['id', 'groupName', 'AZ', 'state', 'status', 'launchConfig'])
LBInstance = collections.namedtuple('LBInstance', ['id', 'state', 'description', 'reasonCode'])


def GetASInstances():
    instanceList=[]
    describeCmdArgs = asCommandArgs[:]
    describeCmdArgs.insert(0, 'as-describe-auto-scaling-instances')
    proc = subprocess.Popen(describeCmdArgs, stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line != '':
            instanceList.append(EC2(*line.split()[1:]))
        else:
            break
    return instanceList

def GetLBInstances():
    instanceList=[]
    elbCommandArgs = [
       'elb-describe-instance-health',
       'CarlinLoadBalancer',
    ]
    elbCommandArgs.extend(asCommandArgs)
    proc = subprocess.Popen(elbCommandArgs, stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line != '':
            lineSplits = line.split()
            instanceList.append(LBInstance(lineSplits[1], lineSplits[2], 'description', 'reasonCode'))
        else:
            break
    return instanceList

def SetASGCapacity(newCapacity):
    setDesiredSizeCmdArgs = [
       'as-set-desired-capacity',
       'CarlinASG',
       '--desired-capacity={capacity}'.format(capacity=newCapacity),
    ]
    setDesiredSizeCmdArgs.extend(asCommandArgs)
    returnCode = subprocess.call(setDesiredSizeCmdArgs)
    if returnCode != 0:
        raise Exception("Command failed! {args}".format(args=setDesiredSizeCmdArgs))
    

def WaitUntilAllEC2sAreHealthy(numExpecting, timeout):
    startTime = time.time()
    while time.time() - startTime < timeout:
        ec2List = GetASInstances()
        unhealthyInstances = [ec2 for ec2 in ec2List if ec2.status != 'HEALTHY']
        if len(ec2List) == numExpecting and len(unhealthyInstances) == 0:
            return
    print 'We timed out waiting for a healthy ec2'

def WaitUntilLBIsHealthy(numExpecting, timeout):
    startTime = time.time()
    while time.time() - startTime < timeout:
        ec2List = GetLBInstances()
        unhealthyInstances = [ec2 for ec2 in ec2List if ec2.state != 'InService']
        if len(ec2List) == numExpecting and len(unhealthyInstances) == 0:
            return
    print 'We timed out waiting for a healthy lb'

            
def MarkInstancesUnhealthy(instanceList, timeBetween):
    '''
    Marks a list of ec2's unhealthy. Waits (timeBetween)s between each marking.
    '''
    for instance in instanceList:
        setInstanceHealthCmdArgs = [
           'as-set-instance-health',
           str(instance.id),
           '--status=Unhealthy',
        ]
        setInstanceHealthCmdArgs.extend(asCommandArgs)
        returnCode = subprocess.call(setInstanceHealthCmdArgs)
        print 'Just marked', instance, 'unhealthy. Waiting', timeBetween, 'seconds.'
        time.sleep(timeBetween)
        

def main():
    ec2IDs = GetASInstances()
    print 'Found ec2s:', ec2IDs

    print 'Launching an additional ec2'
    SetASGCapacity(len(ec2IDs) + 1)

    print 'Waiting for additional ec2 to launch'
    WaitUntilAllEC2sAreHealthy(len(ec2IDs) + 1, 300)
    print 'Waiting for LB Health'
    WaitUntilLBIsHealthy(len(ec2IDs) + 1, 300)

    print 'Marking old EC2s unhealthy'
    MarkInstancesUnhealthy(ec2IDs, 300)

    print 'Resetting ASG capacity'
    SetASGCapacity(1)

if __name__ == "__main__":
    main()
