#!/usr/bin/env python

def verbose(func):
  def wrapper():
    print "Before", func.__name__
    result = func()
    print "After", func.__name__
    return result
  return wrapper

def hello():
  print 'Hello.'

hello = verbose(hello)

hello()

@verbose
def greet():
  print "Greetings."

greet()

@verbose
def howdy():
  print "Howdy."
