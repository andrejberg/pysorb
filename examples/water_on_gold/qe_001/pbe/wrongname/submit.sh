#!/bin/bash
sleeptime=2h
qsub top.O1.Au5859.d.2.7.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au5859.d.3.1.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au5859.d.2.7.phi.0.psi.180.sh
sleep $sleeptime
qsub top.O1.Au5859.d.3.1.phi.0.psi.180.sh
sleep $sleeptime
qsub top.O1.Au5859.d.2.7.phi.45.psi.0.sh
sleep $sleeptime
qsub top.O1.Au5859.d.3.1.phi.45.psi.0.sh
sleep $sleeptime
qsub top.O1.Au5859.d.2.7.phi.45.psi.180.sh
sleep $sleeptime
qsub top.O1.Au5859.d.3.1.phi.45.psi.180.sh
sleep $sleeptime
