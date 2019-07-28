from aws_cdk import (
    aws_ec2 as ec2,
    core
)

from .hello_construct import HelloConstruct


class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the VPC

        vpc = ec2.Vpc(self, "VPC", max_azs=1, cidr='10.0.0.0/16',
                      subnet_configuration=[
                          {
                              'cidrMask': 24,
                              'name': 'Ingress',
                              'subnetType': ec2.SubnetType.PUBLIC,
                          },
                          {
                              'cidrMask': 24,
                              'name': 'Application',
                              'subnetType': ec2.SubnetType.PRIVATE,
                          }
                      ]
        )

        publicsubnet = vpc.public_subnets[0].subnet_id
        privatesubnet = vpc.private_subnets[0].subnet_id

        publicinstancetags = [
            core.CfnTag(key="Name", value="MyPublicLabHost"),
            core.CfnTag(key="Project", value="lab"),
            core.CfnTag(key="CostCenter", value="1520")
        ]

        privateinstancetags = [
            core.CfnTag(key="Name", value="MyPrivateLabHost"),
            core.CfnTag(key="Project", value="lab"),
            core.CfnTag(key="CostCenter", value="1520")
        ]

        mypublicinstance = ec2.CfnInstance(self, 'MyPublicLabHost',
                                     instance_type='t3.nano',
                                     subnet_id=publicsubnet,
                                     image_id=ec2.AmazonLinuxImage().get_image(self).image_id,
                                     tags=publicinstancetags)

        myprivateinstance = ec2.CfnInstance(self, 'MyPrivateLabHost',
                                     instance_type='t3.nano',
                                     subnet_id=privatesubnet,
                                     image_id=ec2.AmazonLinuxImage().get_image(self).image_id,
                                     tags=privateinstancetags)


