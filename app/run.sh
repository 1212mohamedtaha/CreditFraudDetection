#!/bin/bash
nohup python3 -u /app/cons.py > consOut.log  &
nohup python3 -u /app/prod.py > prodOut.log  