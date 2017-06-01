""" Module that holds the EstherPhotonMatterInteractor class.  """
##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

import os, shutil

from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor
from SimEx.Utilities.hydro_txt_to_opmd import convertTxtToOPMD
from esther_execute import Esther_execute as EstherRun

class EstherPhotonMatterInteractor(AbstractPhotonInteractor):
    """
    Class interfacing the Esther Radiation-Hydrodynamics simulation backengine.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters for the EstherPhotonMatterInteractor.
        :type parameters: EstherPhotonMatterInteractorParameters

        :param input_path: Path to the input data for this calculator.
        :type input_path: str

        :param output_path: Path to write output data generated by this calculator to.
        :type output_path: str

        """

        # Init base class.
        super( EstherPhotonMatterInteractor, self).__init__(parameters, input_path, output_path)

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return None

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return None

    def backengine(self):
        """ This method drives the backengine xrts."""
        # Serialize the parameters (generate the input deck).
        self.parameters._serialize()

        # Setup path to esther input file.
        esther_files_path = self.parameters._esther_files_path

                # Prepare for copying over the input files to where esther_py expects them.
        esther_entrees_dir = os.path.join(os.environ['ESTHER_ESTHER'], 'ESTHER_entrees', 'SIMEX', os.path.split(esther_files_path)[-1])
        #os.rename(esther_files_path,  esther_entrees_dir)
        shutil.copytree(esther_files_path,  esther_entrees_dir)

        esther_case_filename = os.path.join( esther_entrees_dir, self.parameters._esther_filename+".txt")
        if not os.path.isfile(esther_case_filename):
            raise IOError("Esther input file %s not found." % (esther_case_filename))


        # Create the run.
        esther_run = EstherRun(
                filename_cas=esther_case_filename,
                chemin_esther=os.path.join(os.environ['ESTHER_ESTHER'],""),
                multiple=False,
                nprocs=1, ### FIXME, read SIMEX_NCORES
                forcer_passage=False, # Forces continuation if esther requests input.
                widComment=None,
                interval=1000,
                recup_sorties_esth = False)

        return esther_run.message

    @property
    def data(self):
        """ Query for the field data. """
        return self.__run_data

    def _readH5(self):
        """
        Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
         ### TODO

    def saveH5(self):
        """
        Method to save the data to a file.
        """

        h5_path = convertTxtToOPMD(self.parameters._esther_files_path)
        if self.output_path is not None:
            shutil.move(h5_path, self.output_path)
