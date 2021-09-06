<!-- PROJECT LOGO -->
<p align="center">

  <h3 align="center">K-MELEON</h3>

  <p align="center">
    Implementation of the K-MELEON.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Python Implementation](#python-implementation)
  * [P4 Implementation](#p4-implementation)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project
Identifying traffic changes accurately sits at the core of many network tasks, from congestion analysis to intrusion detection. Modern systems leverage sketch-based structures that achieve favourable memory-accuracy tradeoffs by maintaining compact summaries of traffic data. Mainly used to detect heavy-hitters (usually the major source of network congestion), some can be adapted to detect traffic changes, but they fail on generality. As their core data structures track elephant flows, they miss to identify mice traffic that may be the main cause of change (e.g., microbursts or low-volume attacks).

In this work I present k-meleon, an in-network online change detection system that identifies heavy-changes -- instead of changes amongst heavy-hitters only, a subtle but crucial difference. My main contribution is a variant of the k-ary sketch (a well-known heavy change detector) that runs on the data plane of a switch. The main challenge was the batch-based design of the original. To address it, k-meleon features a new stream-based design that matches the pipeline computation model and fits its tough constraints. The preliminary evaluation of this prototype shows that k-meleon achieves the same level of accuracy for online detection as the offline k-ary, detecting changes for any type of flow: be it an elephant, or a mouse.

<!-- PYTHON IMPLEMENTATION -->
### Python Implementation [(here)](./k-ary%20(python)/)

<!-- P4 IMPLEMENTATION -->
### P4 Implementation [(here)](./k-meleon%20(p4)/)

<!-- CONTACT -->
## Contact

Gonçalo Matos -  goncalo.o.matos@tecnico.ulisboa.pt