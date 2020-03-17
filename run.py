#!/usr/bin/env python3
"""
Created on March 17 2020

@author: Melchior du Lac
@description: Convert rpSBML file(s) to SBOL

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


##
#
#
def main(inputfile, input_format, output, rbs, max_prot_per_react, pathway_id):
    docker_client = docker.from_env()
    image_str = 'brsynth/rpsbmltosbol-standalone'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        shutil.copy(inputfile, tmpOutputFolder+'/input.dat')
        command = ['/home/tool_rpSBMLtoSBOL.py',
                   '-input',
                   '/home/tmp_output/input.dat',
                   '-output',
                   '/home/tmp_output/output.dat',
                   '-input_format',
                   str(input_format),
                   '-pathway_id',
                   str(pathway_id),
                   '-rbs',
                   str(rbs),
                   '-max_prot_per_react',
                   str(max_prot_per_react)]
        container = docker_client.containers.run(image_str, 
                                                 command, 
                                                 detach=True, 
                                                 stderr=True, 
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        print(err)
        shutil.copy(tmpOutputFolder+'/output.dat', output)
        container.remove()
 


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Given an rpSBML or a collection of rpSBML in a tar, convert to the SBOL format based on the selenzyme UNIPROT IDs')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-rbs', type=bool, default=True)
    parser.add_argument('-max_prot_per_react', type=int, default=3)
    parser.add_argument('-pathway_id', type=str, default='rp_pathway')
    params = parser.parse_args()
    main(params.input, params.input_format, params.output, params.rbs, params.max_prot_per_react, params.pathway_id)
