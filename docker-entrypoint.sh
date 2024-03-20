#!/bin/bash

echo "Starting container of nepsealpa"

celery -A nepsealpa.celery worker -l info
 
