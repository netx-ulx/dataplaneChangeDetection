<!-- PROJECT LOGO -->
<p align="center">

  <h3 align="center">K-ary Sketch</h3>

  <p align="center">
    An implementation of the K-ary Sketch.
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project


<!-- GETTING STARTED -->
## Getting Started

We used python 3.8.5 to run this application. Other versions of python should run this solution but have not been tested.

### Prerequisites

The following libraries must be installed to run this program.
* scapy
```sh
pip3 install scapy
```
* mmh3
```sh
pip3 install mmh3
```

<!-- USAGE EXAMPLES -->
## Usage
* To run the application:
```sh
python change.py
```
Options:

|    long argument | short argument | value            | default                    |
|    ------------- |:--------------:| ---------------- | -------------------------- |
|    `--alpha`     | `-a`           | positive float   |  0.7                       |     
|    `--depth`     | `-d`           | positive integer |  5                         |     
|    `--epoch`     | `-e`           | positive float   |  0.1                       |     
|    `--fmodel`    | `-f`           | string           |  ewma                      |     
|    `--hash`      | `-h`           | string           |  murmur3                   |     
|    `--key`       | `-k`           | opts...          |  src,dst,sport,dport,proto |     
|    `--path`      | `-p`           | string           |  traces/trace1.pcap        |     
|    `--saved`     | `-s`           | positive integer |  1                         |     
|    `--thresh`    | `-t`           | positive float   |  0.1                       |     
|    `--width`     | `-w`           | positive integer |  5462                      |    


* To test the application:
```sh
python test.py
```

* Output
```sh
X-hash-key-T.out
```
  * X - Size of the epoch used
  * hash - hashing algorithm used
  * key - Format of the key used
  * T - Threshold used by the Change Detection Module

<!-- CONTACT -->
## Contact

Gonçalo Matos -  goncalo.o.matos@tecnico.ulisboa.pt

