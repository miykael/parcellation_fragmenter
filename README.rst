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


Fragments a cortical map into N equal-sized parcels. Besides looking beautiful, such surface parcellations can be used as a feature extraction method for machine learning approaches or similar.

The current versions takes in a surface, and optionally, a pre-existing cortical map, and divides the surface into a parameterized number of regions of interest (ROIs).  The fragmentations can be generated using Gaussian Mixture Models (GMMs), Ward Agglomerative clustering, K-Means, and Spectral Clustering.

The following figure shows an example of a whole surface fragmentation for 16, 64, 256, 1024, 4096 parcels using Gaussian Mixture Models:


.. image:: https://raw.githubusercontent.com/miykael/parcellation_fragmenter/master/figures/summary_gmm.png


The following figure shows an example of a fragmentation of the primary auditory cortex for 4, 16, 64, 256, 1024 using K-Means:

.. image:: https://raw.githubusercontent.com/miykael/parcellation_fragmenter/master/figures/summary_A1_kmeans.png

# How to install it

cd parcellation_fragmenter
pip install .

Eventually via pip... It requires the following python packages: `numpy`, `nibabel`, `nilearn`, `sklearn`


# How to run it

Simple, open the `fragmenter.py` script and change the values at the bottom accordingly.


# How to help with it

There are still many things that can be changed/adapted/added. So please feel free to check-out the [issues section](https://github.com/miykael/parcellation_fragmenter/issues) for what can be done, fork the project, send me a PR or give us a feedback!
