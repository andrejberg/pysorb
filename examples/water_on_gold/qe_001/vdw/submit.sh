#!/bin/bash
sleeptime=1h
qsub top.O1.Au62.d.2.8.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au62.d.3.2.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au62.d.3.6.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au62.d.3.8.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au62.d.4.0.phi.0.psi.0.sh
sleep $sleeptime
qsub top.O1.Au62.d.2.8.phi.0.psi.90.sh
sleep $sleeptime
qsub top.O1.Au62.d.3.2.phi.0.psi.90.sh
sleep $sleeptime
qsub top.O1.Au62.d.3.6.phi.0.psi.90.sh
sleep $sleeptime
qsub top.O1.Au62.d.3.8.phi.0.psi.90.sh
sleep $sleeptime
qsub top.O1.Au62.d.4.0.phi.0.psi.90.sh
sleep $sleeptime
