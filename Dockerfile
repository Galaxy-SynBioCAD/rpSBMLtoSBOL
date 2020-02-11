FROM brsynth/rprest

#RUN apt-get update && apt-get install --quiet --yes git

RUN pip install pandas numpy scipy sklearn pysbol pySBOL synbiochem-py


