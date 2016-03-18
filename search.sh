#!/bin/bash

ack "django" | percol | py -x 'x.split(":")'
