#!/bin/bash
sleeptime=1h
qsub hollow.O1.Au535758.d.2.5.phi.0.psi.0.sh
sleep $sleeptime
qsub hollow.O1.Au535758.d.2.7.phi.0.psi.0.sh
sleep $sleeptime
qsub hollow.O1.Au535758.d.2.5.phi.0.psi.90.sh
sleep $sleeptime
qsub hollow.O1.Au535758.d.2.7.phi.0.psi.90.sh
sleep $sleeptime
