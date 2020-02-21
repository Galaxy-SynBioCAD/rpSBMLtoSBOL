# rpSBMLtoSBOL

Convert a single or multiple rpSBML files to SBOL.

## Information Flow

### Input

Required information:
* **rpSBML input**: Either tar.xz input collection of rpSBML files or a single rpSBML file.
* **Include RBS**: Include the Ribosome Biding Site output in the SBOL
* **Max Enzymes per reaction**: Number of enzymes for each coding sequence

Advanced options:
* **Name of the heterologous pathway**: (default: rp_pathway) The SBML groups ID (defined in rpReader) that points to the heterologous reactions and chemical species.
* **REST IP address**: The IP address of the REST service

### Output

* **SBOL**: Output SBOL file

## Installing

To build the image using the Dockerfile, use the following command:

```
docker build -t brsynth/rpsbmltosbml-standalone .
```

### Prerequisites

* [Docker](https://docs.docker.com/v17.09/engine/installation/)
* [libSBML](http://sbml.org/Software/libSBML)
* [libSBOL](https://sbolstandard.org/libsbol-2-1-1-release/)

## Contributing

TODO

## Versioning

Version 0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson

### How to cite rpSBMLtoSBOL?

TODO
