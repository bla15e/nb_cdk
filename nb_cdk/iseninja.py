# AUTOGENERATED! DO NOT EDIT! File to edit: 00_iseninja.ipynb (unless otherwise specified).

__all__ = ['IseNinjaStack', 'config', 'ACCOUNT', 'ZONE_NAME', 'ZONE_ID', 'ZONE_CERT']

# Cell
import yaml

from aws_cdk import (
    aws_apigateway,
    aws_certificatemanager,
    aws_route53,
    aws_route53_targets,
    core
)

# Cell
config = yaml.safe_load(open("./config/config.yml"))
ACCOUNT=config["AWS_ACCOUNT_ID"]
ZONE_NAME = config["ISENINJA_ZONE_NAME"]
ZONE_ID = config["ISENINJA_ZONE_ID"]
ZONE_CERT = config["ISENINJA_ZONE_CERT"]

class IseNinjaStack(core.Stack):
    """
    Base CDK Stack for all stacks associated with ise.ninja
    """
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        self._cert = aws_certificatemanager.Certificate.from_certificate_arn(self, 'DomainCertificate', ZONE_CERT)

        self._hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(self, 'HostedZone',
                                                                         hosted_zone_id=ZONE_ID,
                                                                         zone_name=ZONE_NAME)


    def map_iseninja_subdomain_apigateway(self, subdomain: str, api: aws_apigateway.RestApi) -> str:
        """
        Maps a sub-domain of ise.ninja to an API gateway
        :param subdomain: The sub-domain (e.g. "api")
        :param api: The API gateway endpoint
        :return: The base url (e.g. "https://api.ise.ninja")
        """
        domain_name = subdomain + '.' + ZONE_NAME
        arecord_name = subdomain + "ISENINJADomain"
        construct_name = arecord_name + "Construct"
        url = 'https://' + domain_name

        # add the domain name to the api and the A record to our hosted zone
        domain = api.add_domain_name(construct_name, certificate=self._cert, domain_name=domain_name)

        aws_route53.ARecord(
            self, arecord_name,
            record_name=subdomain,
            zone=self._hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGatewayDomain(domain)))

        return url