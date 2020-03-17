# rpSBMLtoSBOL

Convert a single or multiple rpSBML files to SBOL using the UNIPROT id's from Selenzyme

## Input

Required information:
* **input**: (string) Path to either tar.xz input collection of rpSBML files or a single rpSBML file.
* **input_format**: (string) Format of the input

Advanced options:
* **pathway_id**: (string, default: rp_pathway) The SBML groups ID (defined in rpReader) that points to the heterologous reactions and chemical species.
* **max_prot_per_react**: (integer, default: 3) Include the Ribosome Biding Site output in the SBOL
* **rbs**: (boolean, default: True) Number of enzymes for each coding sequence

## Output

* **output**: (string) Path to the output SBOL file

## Installing

To build the image using the Dockerfile, use the following command:

```
docker build -t brsynth/rpsbmltosbml-standalone:dev .
```

### Running the tests

To run the test, untar the test.tar.xz file and run the following command:

```
python run.py -input test/test_rpGlobalScore.tar  -input_format tar -output test/test_sbol.tar
```

## Prerequisites

* Base Docker Image: [brsynth/rpBase](https://hub.docker.com/r/brsynth/rpbase)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson

### How to cite rpSBMLtoSBOL?
