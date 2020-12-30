# AUTOGENERATED! DO NOT EDIT! File to edit: 02_dev.ipynb (unless otherwise specified).

__all__ = ['DevStack']

# Cell
from .iseninja import IseNinjaStack

from aws_cdk.aws_s3_assets import Asset

from aws_cdk import (
    aws_ec2,
    aws_iam,
    core
)

# Cell

class DevStack(IseNinjaStack):
    """
    Stack Contain Resources for setting up my Dev Host
    """
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        site_name = "IseNinjaHomePage"

        vpc = self.__build_vpc()
        machine_image = self.__build_linux_image()
        role = self.__build_dev_host_role()

        host = self.__build_dev_host(machine_image, vpc, role)

        asset = Asset(self, "DevConfigureScript", path="./assets/configure-dev-instance.sh")
        local_path = host.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key)

        # Userdata executes script from S3
        host.user_data.add_execute_file_command(file_path=local_path)
        asset.grant_read(host.role)


    def __build_vpc(self):
        return aws_ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[aws_ec2.SubnetConfiguration(name="public",subnet_type=aws_ec2.SubnetType.PUBLIC)])

    def __build_linux_image(self):
        return aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE)

    def __build_dev_host_role(self):
        # Instance Role and SSM Managed Policy
        role = aws_iam.Role(self, "DevHostRole", assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        return role

    def __build_dev_host(self, machine_image, vpc, role):
        return aws_ec2.Instance(self, "DevHost",
            instance_type=aws_ec2.InstanceType("t3.nano"),
            machine_image=machine_image,
            vpc = vpc,
            role = role
            )