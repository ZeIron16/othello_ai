#!/bin/bash
# Lancer ton programme et enregistrer son PID
./Egaroucid_for_Console.out &
echo $! > /tmp/egaroucid.pid
wait $!
