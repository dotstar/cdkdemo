#!/usr/bin/env python3

from aws_cdk import core

from hello.hello_stack import MyStack


app = core.App()
MyStack(app, "ehi-lab", env={'region': 'us-east-2'})

app.synth()
