"""
Class for an OGS run.

Parameters
----------
task_root : string, optional
    Path to the destiny folder. Default is the current working dir
task_id : string, optional
    Name for the ogs task. Default: "ogs"
output_dir : string, optional
    Path to the output directory. Default is the task_root folder.

Properties
----------
bc : Boundary Condition
    Information of the Boundary Conditions for the model.
cct : Communication Table
    Information of the Communication Table for the model.
fct : Function
    Information of the Function definitions for the model.
gem : geochemical thermodynamic modeling coupling
    Information of the geochemical thermodynamic modeling
    coupling for the model.
gli : Geometry
    Information of the Geometry for the model.
ic  : Initial Condition
    Information of the Initial Conditions for the model.
krc : Kinetric Reaction
    Information of the Kinetric Reaction for the model.
mcp : reactive components for modelling chemical processes
    Information of the reactive components for
    modelling chemical processes for the model.
mfp : Fluid Properties
    Information of the Fluid Properties for the model.
mmp : Medium Properties
    Information of the Medium Properties for the model.
mpd : Distributed Properties (list of files)
    Information of the Distributed Properties for the model.
msh : Mesh
    Information of the Mesh for the model.
msp : Solid Properties
    Information of the Solid Properties for the model.
num : Settings for the numerical solver
    Information of the numerical solver for the model.
out : Output Settings
    Information of the Output Settings for the model.
pcs : Process settings
    Information of the Process settings for the model.
pct : Particle Definition for Random walk
    Information of the Particles defined for Randomwalk setting.
pqc : Phreqqc coupling (not supported yet)
    Information of the Boundary Conditions for the model.
rei : Reaction Interface
    Information of the Reaction Interface for the model.
rfd : definition of time-curves for variing BCs or STs
    Information of the time curves for the model.
st  : Source Term
    Information of the Source Term for the model.
tim : Time settings
    Information of the Time settings for the model.
"""

from __future__ import absolute_import, division, print_function

import os
import glob
import sys
import time
from copy import deepcopy as dcp
from whichcraft import which

from pexpect.popen_spawn import PopenSpawn
import pexpect

from ogs5py.fileclasses import (BC, CCT, FCT, GEM, GLI, GLIext, IC, KRC, MCP,
                                MFP, MMP, MPD, MSH, MSP, NUM, OUT, PCS, PCT,
                                REI, RFD, RFR, ST, TIM)
from ogs5py.tools._types import OGS_EXT

# pexpect.spawn just runs on unix-like systems
if sys.platform == 'win32':
    OGS_NAME = "ogs.exe"
    CmdRun = PopenSpawn
else:
    OGS_NAME = "ogs"
    CmdRun = pexpect.spawn

# current working directory
CWD = os.getcwd()

# Top Comment for ogs5py
TOP_COM = "|-----------Written with ogs5py-----------|"


class OGS(object):
    """Class for an OGS5 model.

    In this class everything for an OGS5 model can be specified.

    Attributes
    ----------
    bc  : Boundary Condition
        Information of the Boundary Conditions for the model.
    cct : Communication Table
        Information of the Communication Table for the model.
    fct : Function
        Information of the Function definitions for the model.
    gem : geochemical thermodynamic modeling coupling
        Information of the geochemical thermodynamic modeling
        coupling for the model.
    gli : Geometry
        Information of the Geometry for the model.
    ic  : Initial Condition
        Information of the Initial Conditions for the model.
    krc : Kinetric Reaction
        Information of the Kinetric Reaction for the model.
    mcp : reactive components for modelling chemical processes
        Information of the reactive components for
        modelling chemical processes for the model.
    mfp : Fluid Properties
        Information of the Fluid Properties for the model.
    mmp : Medium Properties
        Information of the Medium Properties for the model.
    msh : Mesh
        Information of the Mesh for the model.
    msp : Solid Properties
        Information of the Solid Properties for the model.
    num : Settings for the numerical solver
        Information of the numerical solver for the model.
    out : Output Settings
        Information of the Output Settings for the model.
    pcs : Process settings
        Information of the Process settings for the model.
    pct : Particle Definition for Random walk
        Information of the Particles defined for Randomwalk setting.
    pqc : Phreqqc coupling (not supported yet)
        Information of the Boundary Conditions for the model.
    rei : Reaction Interface
        Information of the Reaction Interface for the model.
    rfd : definition of time-curves for variing BCs or STs
        Information of the time curves for the model.
    st  : Source Term
        Information of the Source Term for the model.
    tim : Time settings
        Information of the Time settings for the model.

    mpd : Distributed Properties (list of files)
        Information of the Distributed Properties for the model.
    gli_ext : list for external Geometry definition
        External definition of surfaces (TIN) or polylines (POINT_VECTOR)
    rfr : list of restart files
        RESTART files as defined in the INITIAL_CONDITION

    """

    def __init__(self, task_root=CWD+"/ogs5model",
                 task_id="model", output_dir=None):
        '''
        Initialize an OGS file.

        Parameters
        ----------
        task_root : string, optional
            Path to the destiny folder. Default is the current working dir
        task_id : string, optional
            Name for the ogs task. Default: "model"
        output_dir : string, optional
            Path to the output directory. Default is the task_root folder.
        '''
        self._task_root = task_root
        self._task_id = task_id
        self.output_dir = output_dir

        self.bc = BC(task_root=task_root, task_id=task_id)
        self.cct = CCT(task_root=task_root, task_id=task_id)
        self.fct = FCT(task_root=task_root, task_id=task_id)
        self.gem = GEM(task_root=task_root, task_id=task_id)
        self.gli = GLI(task_root=task_root, task_id=task_id)
        self.ic = IC(task_root=task_root, task_id=task_id)
        self.krc = KRC(task_root=task_root, task_id=task_id)
        self.mcp = MCP(task_root=task_root, task_id=task_id)
        self.mfp = MFP(task_root=task_root, task_id=task_id)
        self.mmp = MMP(task_root=task_root, task_id=task_id)
        self.msh = MSH(task_root=task_root, task_id=task_id)
        self.msp = MSP(task_root=task_root, task_id=task_id)
        self.num = NUM(task_root=task_root, task_id=task_id)
        self.out = OUT(task_root=task_root, task_id=task_id)
        self.pcs = PCS(task_root=task_root, task_id=task_id)
        self.pct = PCT(task_root=task_root, task_id=task_id)
        self.rei = REI(task_root=task_root, task_id=task_id)
        self.rfd = RFD(task_root=task_root, task_id=task_id)
        self.st = ST(task_root=task_root, task_id=task_id)
        self.tim = TIM(task_root=task_root, task_id=task_id)

        # create a list for mpd files
        self.mpd = []

        # create a list for external Geometry definition (TIN and POINT_VECTOR)
        self.gli_ext = []

        # create a list for RESTART files in the INITIAL_CONDITION
        self.rfr = []

        # store the Top Comment
        self._top_com = TOP_COM

    @property
    def top_com(self):
        """
        Get and set the top comment for the ogs files.
        """
        return self._top_com

    @top_com.setter
    def top_com(self, value):
        self._top_com = value
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).top_com = value

    @property
    def task_root(self):
        """
        Get and set the task_root path of the ogs model.
        """
        return self._task_root

    @task_root.setter
    def task_root(self, value):
        self._task_root = value
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).task_root = value
        for i in range(len(self.mpd)):
            self.mpd[i].task_root = value
        for i in range(len(self.gli_ext)):
            self.gli_ext[i].task_root = value
        for i in range(len(self.rfr)):
            self.rfr[i].task_root = value

    @property
    def task_id(self):
        """
        Get and set the task_id name of the ogs model.
        """
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).task_id = value
        # the mpd file is not connected to the task_id since its name
        # is explicitly given in the MMP file

    def add_mpd(self, mpd_file):
        '''
        Method to add an ogs MEDIUM_PROPERTIES_DISTRIBUTED file to the model.
        This is used for disributed information in the MMP file.

        See ogs5py.MPD for further information
        '''
        if isinstance(mpd_file, MPD):
            mpd_file.task_root = self.task_root
            self.mpd.append(mpd_file)

    def del_mpd(self, index=None):
        '''
        Method to delete MEDIUM_PROPERTIES_DISTRIBUTED file.

        Parameters
        ----------
        index : int or None, optional
            The index of the mpd-file that should be deleted. If None, all
            mpd-files are deleted. Default: None
        '''
        if index is None:
            self.mpd = []
        elif -len(self.mpd) <= index < len(self.mpd):
            del self.mpd[index]
        else:
            print("OGS.del_mpd: given index is not valid.")

    def add_gli_ext(self, gli_ext_file):
        '''
        Method to add an external Geometry definition file to the model.
        This is used for TIN definition in SURFACE or POINT_VECTOR definition
        in POLYLINE in the GLI file.

        See ogs5py.GLI for further information
        '''
        if isinstance(gli_ext_file, MPD):
            gli_ext_file.task_root = self.task_root
            self.gli_ext.append(gli_ext_file)

    def del_gli_ext(self, index=None):
        '''
        Method to delete external Geometry file.

        Parameters
        ----------
        index : int or None, optional
            The index of the external gli file that should be deleted.
            If None, all external gli files are deleted. Default: None
        '''
        if index is None:
            self.gli_ext = []
        elif -len(self.gli_ext) <= index < len(self.gli_ext):
            del self.gli_ext[index]
        else:
            print("OGS.del_gli_ext: given index is not valid.")

    def add_rfr(self, rfr_file):
        '''
        Method to add an ogs RESTART file to the model.
        This is used for disributed information in the IC file.

        See ogs5py.IC for further information
        '''
        if isinstance(rfr_file, RFR):
            rfr_file.task_root = self.task_root
            self.rfr.append(rfr_file)

    def del_rfr(self, index=None):
        '''
        Method to delete RESTART file.

        Parameters
        ----------
        index : int or None, optional
            The index of the RESTART file that should be deleted.
            If None, all RESTART files are deleted. Default: None
        '''
        if index is None:
            self.rfr = []
        elif -len(self.rfr) <= index < len(self.rfr):
            del self.rfr[index]
        else:
            print("OGS.del_rfr: given index is not valid.")

    def write_input(self):
        '''
        method to call all write_file() methods that are initialized
        '''
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).write_file()

        for mpd_file in self.mpd:
            mpd_file.write_file()

        for gliext in self.gli_ext:
            gliext.write_file()

        for rfr_file in self.rfr:
            rfr_file.write_file()

    def reset(self):
        '''
        Delete every content.
        '''
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).reset()
        self.mpd = []
        self.gli_ext = []
        self.rfr = []

    def load_model(self, task_root, task_id=None,
                   use_task_root=False, use_task_id=False,
                   skip_files=None, skip_ext=None,
                   encoding=None, verbose=False):
        '''
        Load an existing OGS5 model.

        Parameters
        ----------
        task_root : str
            Path to the destiny folder.
        task_id : str or None, optional
            Task ID of the model to load. If None is given, it will be
            determind by the found files. Default: None
        use_task_root : Bool, optional
            State if the given task_root should be used for this model.
            Default: False
        use_task_root : Bool, optional
            State if the given task_id should be used for this model.
            Default: False
        skip_files : list or None, optional
            List of file-names, that should not be read. Default: None
        skip_ext : list or None, optional
            List of file-extensions, that should not be read. Default: None
        encoding : str or None, optional
            encoding of the given files. If ``None`` is given, the system
            standard is used. Default: ``None``
        verbose : bool, optional
            Print information of the reading process. Default: False

        Notes
        -----
        This method will search for all known OGS5 file-extensions in the
        given path (task_root).
        Additional files from:
            - GLI (POINT_VECTOR + TIN)
            - MMP (distributed media properties)
            - IC (RESTART)
        will be read automatically.
        '''
        self.reset()

        if skip_files is None:
            skip_files = []
        if skip_ext is None:
            skip_ext = []
        # search for possible task_ids in the directory
        found_ids = search_task_id(task_root)
        if not found_ids:
            if verbose:
                print("ogs5py.OGS.laod_model - nothing was found at: " +
                      task_root)
            return False
        # take the first found task_id
        if task_id is None:
            # take the first found task_id
            task_id = found_ids[0]
        # check if the given task_id is found
        elif task_id not in found_ids:
            if verbose:
                print("ogs5py.OGS.laod_model - didn't find given task_id: " +
                      task_root)
                print(found_ids)
            return False
        # overwrite the task_root
        if use_task_root:
            self.task_root = task_root
        # overwrite the task_id
        if use_task_id:
            self.task_id = task_id

        # iterate over all ogs file-extensions
        for ext in OGS_EXT:
            if verbose:
                print(ext, end=" ")
            # skip certain file extensions if wanted
            if ext in skip_ext or ext[1:] in skip_ext:
                continue
            # search for files with given extension
            files = glob.glob(os.path.join(task_root, task_id+ext))
            # if nothing was found, skip
            if not files:
                continue
            # take the first found file if there are multiple
            fil = files[0]
            # skip file if wanted
            if os.path.basename(fil) in skip_files or fil in skip_files:
                continue
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).read_file(fil,
                                             encoding=encoding,
                                             verbose=verbose)

            # append GEOMETRY defnitions
            if ext == ".gli":
                for ply in self.gli.POLYLINES:
                    # POINT_VECTOR definition of a POLYLINE
                    ext_name = ply["POINT_VECTOR"]
                    if ext_name is not None:
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = GLIext(typ="POINT_VECTOR",
                                          file_name=f_name,
                                          file_ext=f_ext,
                                          task_root=self.task_root)
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.gli_ext.append(dcp(ext_file))
                for srf in self.gli.SURFACES:
                    # Triangulation definition of a SURFACE
                    ext_name = srf["TIN"]
                    if ext_name is not None:
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = GLIext(typ="TIN",
                                          file_name=f_name,
                                          file_ext=f_ext,
                                          task_root=self.task_root)
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.gli_ext.append(dcp(ext_file))

            # append MEDIUM_PROPERTIES_DISTRIBUTED defnitions
            if ext == ".mmp":
                for i in range(len(self.mmp.mainkw)):
                    # external PERMEABILITY_DISTRIBUTION
                    if "PERMEABILITY_DISTRIBUTION" in self.mmp.subkw[i]:
                        index = self.mmp.subkw[i].index(
                            "PERMEABILITY_DISTRIBUTION")
                        ext_name = self.mmp.cont[i][index][0][0]
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = MPD(file_name=f_name,
                                       file_ext=f_ext,
                                       task_root=self.task_root)
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.mpd.append(dcp(ext_file))
                    # external POROSITY_DISTRIBUTION
                    if "POROSITY_DISTRIBUTION" in self.mmp.subkw[i]:
                        index = self.mmp.subkw[i].index(
                            "POROSITY_DISTRIBUTION")
                        ext_name = self.mmp.cont[i][index][0][0]
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = MPD(file_name=f_name,
                                       file_ext=f_ext,
                                       task_root=self.task_root)
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.mpd.append(dcp(ext_file))

            # append RESART defnitions
            if ext == ".ic":
                for i in range(len(self.ic.mainkw)):
                    if "DIS_TYPE" in self.ic.subkw[i]:
                        index = self.ic.subkw[i].index("DIS_TYPE")
                        if self.ic.cont[i][index][0][0] != "RESTART":
                            continue
                        ext_name = self.ic.cont[i][index][0][1]
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = RFR(file_name=f_name,
                                       file_ext=f_ext,
                                       task_root=self.task_root)
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.rfr.append(dcp(ext_file))
        return True

    def run_model(self, ogs_root=None, ogs_name=OGS_NAME,
                  print_log=True, save_log=True,
                  log_path=None, log_name=None):
        '''
        Run the defined OGS5 model.

        Parameters
        ----------
        ogs_root : str or None, optional
            path to the ogs executable. If ``None`` is given, the default sys
            path will be searched with ``which``. Default: None
        ogs_name : str or None, optional
            Name of to the ogs executable to search for.
            Just used if ,ogs_root is ``None``. Default: ``"ogs"``
        print_log : bool, optional
            state if the ogs output should be displayed in the terminal.
            Default: True
        save_log : bool, optional
            state if the ogs output should be saved to a file.
            Default: True
        log_path : str or None, optional
            Path, where the log file should be saved. Default: None
            (the defined output directory or the task_root directory)
        log_name : str or None, optional
            Name of the log file. Default: None
            (task_id+time+"_log.txt")

        Return
        ------
        success : bool
            State if OGS5 returned, that it terminated 'normally'.
        '''
        # look for the standard ogs executable in the standard-path
        if ogs_root is None:
            check_ogs = which(ogs_name)
            if check_ogs is None:
                print("Please put the ogs executable in the default sys path: "
                      + str(os.defpath.split(os.pathsep)))
                print("Or provide the path to your executable")
                return False
            else:
                ogs_root = check_ogs

        # create the model_root for ogs
        model_root = os.path.join(self.task_root, self.task_id)
        # create the command to call ogs
        args = [ogs_root, model_root]
        # add optional output directory
        # check if output directory is an absolute path with os.path.isabs
        # otherwise set it in the task_root directory
        if self.output_dir is not None:
            # format the outputdir
            output_dir = os.path.dirname(self.output_dir+"/")
            # check if outputdir is given as absolut path
            if not os.path.isabs(output_dir):
                # if not, put the outputfolder in the task_root
                output_dir = os.path.join(self.task_root, output_dir)
            # create the outputdir
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # append the outputdir to the ogs-command
            args.append("--output-directory")
            args.append(output_dir)
        else:
            output_dir = self.task_root

        # set standard log_name
        if log_name is None:
            log_name = (self.task_id + "_" +
                        time.strftime("%Y-%m-%d_%H-%M-%S") + "_log.txt")
        # put the logfile in the defined output-dir
        if log_path is None:
            log_path = output_dir
        log = os.path.join(log_path, log_name)

        # create a splitted output stream (to file and stdout)
        out = Output(log, print_log=print_log)
        # call ogs with pexpect
        child = CmdRun(
            " ".join(args),
            timeout=None,
            logfile=out,
        )
        child.expect(pexpect.EOF)
        # close the output stream
        out.close()

        success = "Simulation time" in out.last_line

        if not save_log:
            os.remove(log)

        return success


class Output(object):
    """A class to duplicate an output stream to stdout/err.
    This works in a manner very similar to the Unix 'tee' command.
    When the object is closed or deleted, it closes the original file given to
    it for duplication.
    """
    # from https://github.com/ipython/ipython/blob/master/IPython/utils/io.py
    # Inspired by:
    # http://mail.python.org/pipermail/python-list/2007-May/442737.html

    def __init__(self, file_or_name, mode="w", channel='stdout',
                 print_log=True):
        """Construct a new Output object.

        Parameters
        ----------
        file_or_name : filename or open filehandle (writable)
          File that will be duplicated
        mode : optional, valid mode for open().
          If a filename was give, open with this mode.
        channel : str, one of ['stdout', 'stderr']
        """
        if channel not in ['stdout', 'stderr']:
            raise ValueError('Invalid channel spec %s' % channel)

        if hasattr(file_or_name, 'write') and hasattr(file_or_name, 'seek'):
            self.file = file_or_name
        else:
            self.file = open(file_or_name, mode)
        self.channel = channel
        self.ostream = getattr(sys, channel)
        self._closed = False
        self.encoding = sys.stdout.encoding
        if not self.encoding:
            self.encoding = "utf-8"
        self.print_log = print_log
        self.last_line = ""

    def close(self):
        """Close the file and restore the channel."""
        self.flush()
        self.file.close()
        self._closed = True

    def write(self, data):
        """Write data to both channels."""
        self.last_line = data.decode(self.encoding)
        self.file.write(self.last_line)
        if self.print_log:
            self.ostream.write(data)
            self.ostream.flush()

    def flush(self):
        """Flush both channels."""
        self.file.flush()
        if self.print_log:
            self.ostream.flush()

    def __del__(self):
        if not self._closed:
            self.close()


def search_task_id(task_root):
    '''
    Search for OGS model names in the given path

    Parameters
    ----------
    task_root : str
        Path to the destiny folder.

    Return
    ------
    found_ids : list of str
        List of all found task_ids.
    '''
    found_ids = []
    # iterate over all ogs file-extensions
    for ext in OGS_EXT:
        # search for files with given extension
        files = glob.glob(os.path.join(task_root, "*"+ext))
        # take the first found file if there are multiple
        for fil in files:
            tmp_id = os.path.splitext(os.path.basename(fil))[0]
            if tmp_id not in found_ids:
                found_ids.append(tmp_id)
    return found_ids
