# -*- coding: latin-1 -*-
import sys
from setuptools import setup

"""

    setup
    ~~~~~

    Setup script for installation.

    See README.md for installing procedure.

    :copyright: Copyright 2023-2024 INRA-ECOSYS, see AUTHORS.
    :license: CeCILL-C, see LICENSE for details.

    **Acknowledgments**: The research leading these results has received funding through the 
    Investment for the Future programme managed by the Research National Agency 
    (BreedWheat project ANR-10-BTBR-03).

    .. seealso:: 1st article et al.
"""

"""
    Information about this versioned file:
        $LastChangedBy$
        $LastChangedDate$
        $LastChangedRevision$
        $URL$
        $Id$
"""

if sys.version_info < (3, 9):
    print('ERROR: Root_BRIDGES requires at least Python 3.9 to run.')
    sys.exit(1)

setup(
    name="Wheat_BRIDGES",
    version="0.0.1",
    packages=["wheat_bridges", "simulations", "test"],
    include_package_data=True,
    author="T.Gerault, F.Rees, R.Barillot and C.Pradal",
    author_email="tristan.gerault@inrae.fr, frederic.rees@inrae.fr, romain.barillot@inrae.fr, christophe.pradal@cirad.fr",
    description="Wheat_BRIDGES is a model of root-shoot CNW physiology at root segment scale",
    long_description="""TODO""",
    license="CeCILL-C",
    keywords="functional-structural plant model, wheat, uptake, rhizodeposition, trophic status, carbon, nitrogen, metabolism, remobilisation, source-sink relation, resource allocation",
    url="https://github.com/GeraultTr/Wheat_BRIDGES",
    download_url="https://github.com/GeraultTr/Wheat_BRIDGES.git"
)
