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
def main(inputfile, input_format, output, rbs, max_prot_per_react, tirs, topX, pathway_id):
    docker_client = docker.from_env()
    image_str = 'brsynth/rpsbmltosbol-standalone:dev'
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
                   '-topX',
                   str(topX),
                   '-tirs',
                   str(tirs),
                   '-max_prot_per_react',
                   str(max_prot_per_react)]
        container = docker_client.containers.run(image_str, 
                                                 command, 
                                                 detach=True, 
                                                 stderr=True, 
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        err_str = err.decode('utf-8')
        print(err_str)
        if not 'ERROR' in err_str:
            shutil.copy(tmpOutputFolder+'/output.dat', output)
        container.remove()
 


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Given an rpSBML or a collection of rpSBML in a tar, convert to the SBOL format based on the selenzyme UNIPROT IDs')
    parser.add_argument('-input', type=str, help='input file path', required=True)
    parser.add_argument('-input_format', type=str, help='input file format. May be either "tar" (i.e. collection of SBML in tar archive) or "sbml"', required=True)
    parser.add_argument('-output', type=str, help='output SBOL file path', required=True)
    parser.add_argument('-rbs', type=str, default='True', help='calculate the RBS?')
    parser.add_argument('-topX', type=int, default=5, help='convert the top X scoring SBML files')
    parser.add_argument('-tirs', type=str, default='10000,20000,30000', help='RBS numbers relative strengths (must be the same length of "max_prot_per_react")')
    parser.add_argument('-max_prot_per_react', type=int, default=3, help='number of RBS per reactions')
    parser.add_argument('-pathway_id', type=str, default='rp_pathway', help='name of the heterologous pathway in the SBML files')
    params = parser.parse_args()
    main(params.input, params.input_format, params.output, params.rbs, params.max_prot_per_react, params.tirs, params.topX, params.pathway_id)
