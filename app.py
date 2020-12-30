from aws_cdk import core
from nb_cdk.website import WebsiteStack
from nb_cdk.dev import DevStack

print("Initializing App...")
app = core.App()

print("Creating Website")
website = WebsiteStack(app, "PersonalWebsite")

dev_stack = DevStack(app, "DevStack")

print("Synthezing Application")
app.synth()