#!/bin/bash
err=0
trap 'err=1' ERR
flake8 --config=scripts/flake8-setup.cfg ${@:-}
test ${err} = 0
