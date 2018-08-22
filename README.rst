============
fragmenter
============

.. start-badges

.. image:: https://img.shields.io/github/issues/miykael/parcellation_fragmenter.svg
  :target: https://github.com/miykael/parcellation_fragmenter/issues/

.. image:: https://img.shields.io/github/issues-pr/miykael/parcellation_fragmenter.svg
  :target: https://github.com/miykael/parcellation_fragmenter/pulls/

.. image:: https://img.shields.io/github/contributors/miykael/parcellation_fragmenter.svg
  :target: https://GitHub.com/miykael/parcellation_fragmenter/graphs/contributors/

.. image:: https://github-basic-badges.herokuapp.com/commits/miykael/parcellation_fragmenter.svg
  :target: https://github.com/miykael/parcellation_fragmenter/commits/master

.. image:: https://github-size-badge.herokuapp.com/miykael/parcellation_fragmenter.svg
  :target: https://github.com/miykael/parcellation_fragmenter/archive/master.zip

.. image:: http://hits.dwyl.io/miykael/parcellation_fragmenter.svg
  :target: http://hits.dwyl.io/miykael/parcellation_fragmenter

Fragment a cortical surface into a parameterized number of parcels.  We imagine that this method could be use as a feature extraction method for machine learning approaches later on.

The class 'Fragment' takes in as input a surface mesh and applies clustering algorithms to the mesh.  Follwing the 'sklearn' convention, the fragmentation is generated using a 'fit' method.  Additionally, we provide the option to constrain fragmentation to follow previously generated anatomical boundaries.

The fragmentation can be performed with Gaussian Mixture Models, K-Means, Ward Agglomerative Clustering, and Spectral Clustering.

The following figure shows an example of a whole surface fragmentation with 16, 64, 256, 1024, and 4096 parcels using GMMs:

.. image:: https://raw.githubusercontent.com/miykael/parcellation_fragmenter/master/figures/summary_gmm.png

The following figure shows an example of a fragmentation of the superior temporal cortex with 4, 16, 64, 256, 1024 using K-Means:

.. image:: https://raw.githubusercontent.com/miykael/parcellation_fragmenter/master/figures/summary_A1_kmeans.png

# How to install it

.. bash
  cd fragmenter
  pip install .

# How to help with it

There are still many things that can be changed/adapted/added. So please feel free to check-out the [issues section](https://github.com/miykael/parcellation_fragmenter/issues) for what can be done, fork the project, send me a PR or give us a feedback!
