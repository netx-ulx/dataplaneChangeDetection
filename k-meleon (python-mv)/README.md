<!-- PROJECT LOGO -->
<p align="center">

  <h3 align="center">Python implementation of %SOMENAME%</h3>

  <p align="center">
    An implementation of the %SOMENAME%.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Files](#files)
* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Run](#run)

---
## Files
- change.py
- forecast-module.py: Implementation of forecasting models in python.
- kary_sketch.py: K-ary sketch data-structure implementation.
- main.py
- new_change.py 
- pcap_parser.py: .pcap file packet parser.
- test.py
---

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- GETTING STARTED -->
## Getting Started

We used python 3.8.5 to run this application. Other versions of python should run this solution but have not been tested.

<!-- PREREQUISITES -->
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
* statistics
```sh
pip3 install statistics
```

<!-- RUN -->
### Run
* To run the application:
```sh
python main.py <filepath> [options]
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
|    `--saved`     | `-s`           | positive integer |  1                         |     
|    `--thresh`    | `-t`           | positive float   |  0.1                       |     
|    `--width`     | `-w`           | positive integer |  5462                      |    

* Output
```sh
output/<filename>-<epoch>-<hash>-<key>-<T>.out
```
  * filename - Name of the pcap file
  * epoch - Size of the epoch used
  * hash - hashing algorithm used
  * key - Format of the key used
  * T - Threshold used by the Change Detection Module

* To test the application:
```sh
python test.py <filepath> [target timestamp]* [options]
```
or (Windows)
```sh
./test.bat [options]
```
Options:

|    long argument | short argument | value            | default                    |
|    ------------- |:--------------:| ---------------- | -------------------------- |   
|    `--depth`     | `-d`           | positive integer |  5                         |     
|    `--epoch`     | `-e`           | positive float   |  0.1                       |     
|    `--fmodel`    | `-f`           | string           |  ewma                      |     
|    `--hash`      | `-h`           | string           |  murmur3                   |       
|    `--saved`     | `-s`           | positive integer |  1                         |     
|    `--width`     | `-w`           | positive integer |  5462                      |    

* Output
```sh
  Best combination: false_positives/num_epochs accuracy false_positives changes_detected [alpha, threshold, key]
  Best Accuracy combination: false_positives/num_epochs accuracy false_positives changes_detected [alpha, threshold, key]
```