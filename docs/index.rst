.. python-graphenelib documentation master file, created by
   sphinx-quickstart on Fri Jun  5 14:06:38 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. http://sphinx-doc.org/rest.html
   http://sphinx-doc.org/markup/index.html
   http://sphinx-doc.org/markup/para.html
   http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html
   http://rest-sphinx-memo.readthedocs.org/en/latest/ReST.html

Welcome to python-graphenelib's documentation!
===============================================

Graphene is a blockchain technology (i.e. software) that allows for fast
transactions and decentralized trading of assets as well as customized on-chain
smart contracts. Graphene itself is a platform to develop customized
blockchains like BitShares, Steem or PeerPlays.

In practice, Graphene is only a concept implementation and does not directly
have its own public blockchain.

The first public blockchain to use the Graphene technology is *BitShares 2.0*.
However, this library should be able to interface with any other Graphene-based
blockchain, too.

This library serves as a core library that bundles core features for
these platforms, which have their own libraries build on top of this
library.

Python-Graphene Libraries
-------------------------
.. toctree::
   :maxdepth: 3

   installation
   classes

Graphene API
------------
.. toctree::
   :maxdepth: 1

   graphene-objects
   graphene-api
   witness
   wallet

Packages
--------

.. toctree::
   :maxdepth: 4

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
