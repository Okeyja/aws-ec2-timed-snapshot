# Amazon EC2 自动快照功能

## 简介

通过CloudWatch的定时事件功能触发Lambda函数，函数脚本将为您代码中指定InstanceId的EC2实例的**所有**EBS卷打上快照（snapshot）。

## 配置IAM权限

1. IAM -> 策略 -> 创建策略 -> JSON方式 -> 保存为 **timed_snapshot_policy**

  ```json
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Effect": "Allow",
           "Action": [
               "logs:*"
           ],
           "Resource": "*"
       },
       {
           "Effect": "Allow",
           "Action": "ec2:Describe*",
           "Resource": "*"
       },
       {
           "Effect": "Allow",
           "Action": [
               "ec2:CreateSnapshot",
               "ec2:DeleteSnapshot",
               "ec2:CreateTags",
               "ec2:ModifySnapshotAttribute",
               "ec2:ResetSnapshotAttribute"
           ],
           "Resource": [
               "*"
           ]
       }
   ]
  }
  ```

2. IAM -> 角色 -> 创建角色 -> 指定策略为 **timed_snapshot_policy** -> 保存为 **timed_snapshot_role**。

## 创建函数

1. Lambda -> 创建函数 -> 指定角色为 **timed_snapshot_role**，保存为**timed_snapshot**。
2. 粘贴**lambda_function代码**，默认会遍历所有非关机状态的所有实例，根据需要编辑代码 **InstanceIds数组**。

## 创建定时器

1. Cloudwatch -> 事件 -> 规则 ->创建规则。
2. 选择**事件源**为计划事件，调整频率或编写您的Cron表达式。
3. 添加**目标**为Lambda函数，选择刚才创建的**timed_snapshot**。
4. 保存。

## 参考链接

https://cloud.tencent.com/info/33fc4f33b9cb504c26009510c2696800.html