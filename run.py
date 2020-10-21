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


def main(inputfile, input_format, output, rbs, max_prot_per_react, tirs, topX, pathway_id):
    """Call the docker to convert a collection of rpSBML into a collection of SBOL

    :param inputfile: The path to the TAR collection of rpSBML
    :param intput_format: The input format of the file. Valid options: tar, sbml
    :param output: The path to the output TAR collection of SBOL
    :param rbs: Calculate or not the RBS strength
    :param max_prot_per_react: The maximum number of proteins per reaction (Default: 3)
    :param tirs: The RBS strength values
    :param topX: The top number of UNIPROT id's per reaction to use
    :param pathway_id: The Groups id of the heterologous pathway

    :type inputfile: str
    :type input_format: str
    :type output: str
    :type rbs: bool
    :type max_prot_per_react: int
    :type tirs: list
    :type topX: int
    :type pathway_id: str

    :rtype: None
    :return: None
    """
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
        if os.path.exists(inputfile):
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
            if 'ERROR' in err_str:
                print(err_str)
            elif 'WARNING' in err_str:
                print(err_str)
            if not os.path.exists(tmpOutputFolder+'/output.dat'):
                print('ERROR: Cannot find the output file: '+str(tmpOutputFolder+'/output.dat'))
            else:
                shutil.copy(tmpOutputFolder+'/output.dat', output)
            container.remove()
        else:
            logging.error('Cannot find one or more of the input file: '+str(inputfile))
            exit(1)


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
