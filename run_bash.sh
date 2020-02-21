#!/bin/bash

docker run -v $1:/home/input_file -v ${PWD}/results/:/home/results/ --rm brsynth/rpsbmltosbml-standalone:dev python /home/tool_rpSBMLtoSBOL.py -input /home/input_file -input_format $2 -outputSBOL /home/results/output.sbol.xml -rbs True -max_prot_per_react 3 -pathway_id rp_pathway

cp ${PWD}/results/output.sbol.xml .
rm -r ${PWD}/results/
