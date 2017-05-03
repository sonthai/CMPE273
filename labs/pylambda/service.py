# -*- coding: utf-8 -*-

print "Loading function"
def handler(event, context):
    print "hello, world"
    print event 
    # Your code goes here!
    e = event.get('e')
    pi = event.get('pi')
    return e + pi
