# !/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

# legacy imports
import copy
import logging
import os
import os.path
import platform
import re
import string
import glob
import tempfile
import datetime

import arnold as ai
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.utils as utils
import mtoa.makeTx as makeTx

from ..core.qt import QtWidgets, QtCore
from ..core.tex import COLORSPACE_PATTERN, FILE_NODE_ATTR, TEXTURE_WITH_COLOR_SPACE, DEFAULT_COLOR_SPACE, parse_sequence_path, TX_COLOR_SPACE
from ..core.utils import getMayaWindow

valid_chars = string.ascii_letters

_regex = r'^([\w\_]+)\.([\w\_\*]+)$'
regex = re.compile(_regex)
logger = logging.getLogger(__name__)

img_extensions = [
    '.jpeg',
    '.jpg',
    '.tiff',
    '.tif',
    '.png',
    '.exr',
    '.hdr',
    '.bmp',
    '.tga',
]

default_texture_data = {
    'usage': {},
    'root': '',
    'name': '',
    'status': 'notx',
    'path': None,
    'txpath': None,
    'colorspace': None,
    'index': 0,
    'item': None
}

scene_default_texture_scan = [
    'file.fileTextureName',
    'aiImage.filename',
    'imagePlane.imageName',
    'mesh.mtoa_constant_*'
]

scene_expand_attributes = {
    'fileTextureName': 'computedFileTextureNamePattern'
}


class MakeTxThread(QtCore.QThread):
    maxProgress = QtCore.Signal(int)
    progress = QtCore.Signal(int)

    def __init__(self, manager, parent):
        QtCore.QThread.__init__(self, parent)
        self.txManager = manager
        self.filesCreated = 0
        self.createdErrors = 0
        self.is_canceled = False
        self.force = True

        self.processor = TxProcessor(self.txManager)

    def run(self):
        self.filesCreated = 0
        self.createdErrors = 0
        self.is_canceled = False
        self.processor.maxProgress.connect(self.emit_max_progress)
        self.processor.progress.connect(self.emit_progress)
        self.processor.createTx()

    # create a .tx file with the provided options. It will wait until it is finished
    def runMakeTx(self, texture, space):
        arg_options = self.txManager.get_tx_args()
        status = utils.executeInMainThreadWithResult(makeTx.makeTx, texture, colorspace=space, arguments=arg_options)
        return status

    def emit_max_progress(self, value):
        self.maxProgress.emit(value)

    def emit_progress(self, value):
        self.progress.emit(value)

    def set_forced(self, forced):
        self.processor.force = forced

    def cancel_tx(self):
        self.is_canceled = True


def MakeTXMessageCallback(logmask, severity, msg_string, metadata, user_ptr):
    message = str(msg_string)
    # maketx errors are given as warnings so we need to detect "ERROR" in the message text
    if "ERROR" in message or severity == ai.AI_SEVERITY_ERROR:
        error_message = message.split("\n")[-1]  # get last line of error
        om.MGlobal.displayError(error_message.split(":")[-1])
    elif severity == ai.AI_SEVERITY_WARNING:
        warning_message = message.split("\n")[-1]  # get last line of error
        om.MGlobal.displayWarning(warning_message.split(":")[-1])


class TxProcessor(QtCore.QObject):
    """docstring for TxProcessor"""

    maxProgress = QtCore.Signal(int)
    progress = QtCore.Signal(int)

    def __init__(self, txmanager):
        super(TxProcessor, self).__init__()
        self.txManager = txmanager
        self.filesCreated = 0
        self.createdErrors = 0
        self.cb_id = -1
        self.is_canceled = False
        self.force = True

    def test_progress(self):
        self.maxProgress.emit(100)
        for i in range(100):
            self.progress.emit(i)

        return

    def createTx(self):
        selected_textures = utils.executeInMainThreadWithResult(self.txManager.get_selected_textures)
        if not selected_textures:
            return self.test_progress()

        temp_file = os.path.join(
            tempfile.gettempdir(),
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        ).replace("\\", "/")

        render_colorspace = cmds.colorManagementPrefs(query=True, renderingSpaceName=True)
        colorspace_config = cmds.colorManagementPrefs(query=True, configFilePath=True)
        maya_resource_path = os.environ["MAYA_LOCATION"]
        maya_resource_path += "/Resources" if platform.system() == "Darwin" else "/resources"
        colorspace_config = colorspace_config.replace("<MAYA_RESOURCES>", maya_resource_path)

        cmEnable = cmds.colorManagementPrefs(query=True, cmEnabled=True)

        textureList = []

        arg_options = self.txManager.get_tx_args()

        universe = ai.AiUniverse()

        # create a callback to print errors to script editor
        self.cb_id = ai.AiMsgRegisterCallback(ai.AtMsgExtendedCallBack(MakeTXMessageCallback),
                                              ai.AI_LOG_WARNINGS | ai.AI_LOG_ERRORS, None)
        ai.AiMsgSetConsoleFlags(universe, ai.AI_LOG_ALL)

        options = ai.AiUniverseGetOptions(universe)
        color_manager = ai.AiNodeLookUpByName(universe, "ai_default_color_manager_ocio")
        ai.AiNodeSetStr(color_manager, "config", colorspace_config)
        ai.AiNodeSetStr(color_manager, "color_space_linear", render_colorspace)

        temp_data = []

        for i, textureData in enumerate(selected_textures):
            texture = textureData['path']

            if textureData['colorspace'] != '':
                colorSpace = textureData['colorspace']

            if not texture or not colorSpace:
                continue

            # Process all the files that were found previously for this texture (eventually multiple tokens)

            # inputFiles = utils.executeInMainThreadWithResult(makeTx.expandFilenameWithSearchPaths, texture)
            print("texture = ", texture)
            if os.path.isfile(texture):
                inputFiles = [texture]
                temp_data.append([texture, "", ""])
            else:
                rule = parse_sequence_path(texture)
                if not rule:
                    continue
                inputFiles = glob.glob(rule)
                temp_data.append([texture, rule, inputFiles])
            if not inputFiles:
                continue

            for inputFile in inputFiles:

                txArguments = "-v --unpremult --oiio"
                # force the colorconfig otherwise we can get errors see MTOA-1541
                txArguments += " --colorconfig " + colorspace_config
                if self.force:
                    txArguments += " -u"
                if not self.txManager.get_use_autotx():
                    txArguments = ' '.join(arg_options)

                    if cmEnable:
                        txArguments += ' --colorconvert "'
                        txArguments += colorSpace
                        txArguments += '" "'
                        txArguments += render_colorspace
                        txArguments += '"'
                else:
                    txArguments += " " + str(ai.AiTextureAutoTxFlags(inputFile, colorSpace, universe))
                # todo: 新版生成tx之后文件名自带色彩空间，由于特殊需求，在这里自定义输出文件名.
                output_tx = re.sub(r"\.[^.]+$", ".tx", inputFile)
                txArguments += " -o \"%s\"" % output_tx
                print("txArguments = ", txArguments)
                textureList.append([inputFile, txArguments, textureData['item'], textureData['colorspace']])

        with open(temp_file, "w") as f:
            f.write(str(temp_data))

        self.txManager.filesToCreate = len(textureList)
        texture_dict = {}
        for tex in textureList:
            if tex[0] not in texture_dict:
                texture_dict[tex[0]] = [tex[3]]
            else:
                texture_dict[tex[0]].append(tex[3])

        num_jobs_left = len(textureList)  # default to arbitrary value > 0

        # set the max progress on the progress bar/dialog
        self.maxProgress.emit(num_jobs_left)

        # Now I have a list of textures to be converted
        # let's give this list to arnold
        for i, textureToConvert in enumerate(textureList):
            self.txManager.set_status(textureToConvert[2], "processing ..")
            ai.AiMakeTx(textureToConvert[0], textureToConvert[1])
        status = ai.POINTER(ai.AtMakeTxStatus)()  # returns the current status of the input files
        source_files = ai.POINTER(ai.AtPythonString)()  # returns the list of input files in the same order as the status
        num_submitted = ai.c_uint()

        self.createdErrors = 0
        self.filesCreated = 0

        processed = 0
        processed_images = []
        while (num_jobs_left > 0):
            if self.is_canceled:
                print("[mtoa.tx] tx generation has been cancelled")
                ai.AiMakeTxAbort(ai.byref(status), ai.byref(source_files), ai.byref(num_submitted))
                break

            num_jobs_left = ai.AiMakeTxWaitJob(ai.byref(status), ai.byref(source_files), ai.byref(num_submitted))
            for i in range(0, num_submitted.value):
                # get the status and update the ui
                src_str = str(source_files[i])
                items = texture_dict.get(src_str, [])
                for cs in items:
                    output_tx = get_output_tx_path(src_str, cs, render_colorspace)
                    if status[i] in (ai.AiTxUpdated, ai.AiTxUpdate_unneeded) and os.path.exists(output_tx):
                        if src_str not in processed_images:
                            processed += 1
                            processed_images.append(src_str)
                    elif status[i] == ai.AiTxError:
                        # MTOA-1864 Early out if there's an error
                        processed = len(textureList)
                        num_jobs_left = 0

            # emit progress to the progress bar/dialog
            self.progress.emit(processed)

        if (num_submitted.value > len(textureList)):
            ai.AiMsgFatal("There are more submitted textures than there are textures! "
                          "Queue should have been cleared!")

        for i in range(0, num_submitted.value):

            src_str = str(source_files[i])

            if (status[i] == ai.AiTxUpdated):
                self.filesCreated += 1
                print("[mtoa.tx] {}: {} was updated".format(i, src_str))
            elif (status[i] == ai.AiTxError):
                self.createdErrors += 1
                print("[mtoa.tx] {}: {} could not be updated".format(i, src_str))
            elif (status[i] == ai.AiTxUpdate_unneeded):
                print("[mtoa.tx] {}: {} did not need to be updated".format(i, src_str))
            elif (status[i] == ai.AiTxAborted):
                print("[mtoa.tx] {}: {} was aborted".format(i, src_str))

        ai.AiMsgDeregisterCallback(self.cb_id)
        ai.AiUniverseDestroy(universe)
        utils.executeDeferred(self.txManager.on_refresh)

        return True


def sanitize_string(string):
    '''Converts a string with possible non-ascii characters into a clean safe
    string'''
    result = ''
    for letter in string:
        result += letter if letter in valid_chars else '_'
    return result


def is_image(file):
    '''Returns whether the input file is an image'''
    ext = os.path.splitext(file)[1]
    return ext in img_extensions


def set_colorspace(node):
    attr = FILE_NODE_ATTR.get(cmds.nodeType(node), "")
    if not attr:
        return
    f = cmds.getAttr("%s.%s" % (node, attr))
    if f.endswith('.tx'):
        cmds.setAttr("%s.colorSpace" % node, TX_COLOR_SPACE, type="string")
        return

    texture_type = re.findall(COLORSPACE_PATTERN, f)
    if not texture_type:
        return
    colorspace = TEXTURE_WITH_COLOR_SPACE.get(texture_type[0], None)
    if not colorspace:
        return
    cmds.setAttr("%s.colorSpace" % node, colorspace, type="string")


def get_colorspace(nodeattr):
    node = nodeattr.split('.')[0]
    colorSpace = 'auto'

    set_colorspace(node)

    if cmds.attributeQuery("colorSpace", node=node, exists=True):
        nodeColorSpace = cmds.getAttr(node + '.colorSpace')

        colorSpace = nodeColorSpace

    return colorSpace


def guessColorspace(filename):
    if filename.endswith('.tx'):
        return TX_COLOR_SPACE
    texture_type = re.findall(COLORSPACE_PATTERN, filename)
    if not texture_type:
        return False
    colorspace = TEXTURE_WITH_COLOR_SPACE.get(texture_type[0], None)
    if not colorspace:
        return False
    return colorspace


def get_folder_textures(folder, subfolders=False):
    '''Returns a dictionary with all textures found in a folder. If subfolders
    flag is True, subfolders will be also scanned.'''
    textures = {}
    files = []
    if not subfolders:
        files = [x for x in os.listdir(folder) if is_image(x)]
        files = [os.path.join(folder, x) for x in files]
    else:
        for root, fld, fileList in os.walk(folder):
            files += [os.path.join(root, x) for x in fileList if is_image(x)]

    # Normalize ALL texture paths to avoid slash conflicts
    files = [os.path.normpath(x) for x in files]

    for texture in files:
        textures[texture] = copy.deepcopy(default_texture_data)
        textures[texture]['path'] = texture
        textures[texture]['name'] = os.path.basename(texture)

    return build_texture_data(textures, expand=False)


def get_scanned_files(scan_attributes):
    '''Scans the current scene for textures based on an input list. The
    scan_attributes argument must be a list of strings, in which each of them
    should be the node type and the node attribute separated by a dot.
    Attributes accept the "*" wildcard.

    Example:
        >> get_scanned_files(['file.texturePath', 'mesh.mtoa_*'])
    '''
    textures = {}

    for scan in scan_attributes:
        if not regex.match(scan):
            raise ValueError(
                'Scan attribute "%s" does not match regex "%s"' %
                (scan, _regex))

        ntype, attr = scan.split('.')
        attributes = set()
        if '*' not in attr:
            nodes = cmds.ls('*.%s' % attr, r=True, type=ntype, o=True)
            [attributes.add('%s.%s' % (x, attr)) for x in nodes]
        else:
            for node in cmds.ls(type=ntype):
                for a in cmds.listAttr(node, r=True, st=attr) or []:
                    if not cmds.getAttr(".".join([node, a]), type=True) == 'string':
                        continue

                    attributes.add(".".join([node, a]))

        for attribute in attributes:

            node = attribute.split('.')[0]

            # for some attributes we need to use a differnt computed attribute
            # to get the actual result or expressions etc
            attr_exp = attribute
            for k, v in scene_expand_attributes.items():
                attr_exp = attribute.replace(k, v)

            texture_path = cmds.getAttr(attr_exp)
            if not texture_path:
                continue

            texture_path = os.path.normpath(texture_path)
            textures.setdefault(
                texture_path, copy.deepcopy(default_texture_data))
            textures[texture_path]['usage'][node] = {}
            textures[texture_path]['path'] = texture_path
            textures[texture_path]['name'] = os.path.basename(texture_path)

    return build_texture_data(textures)


def build_texture_data(textures, expand=True):
    '''Builds the texture's dictionary. If the expand flag is enabled, it will
    attempt to expand the variables in the path.'''
    for texture, texture_data in textures.items():
        if expand:
            texture_exp = makeTx.expandFilenameWithSearchPaths(texture)
            if len(texture_exp):
                texture_exp = texture_exp[0]
            else:
                texture_exp = texture
        else:
            texture_exp = texture

        root, name = os.path.split(texture)
        name_noext, ext = os.path.splitext(name)
        render_colorspace = cmds.colorManagementPrefs(q=True, renderingSpaceName=True)
        combined_status = []
        iinfo = makeTx.imageInfo(texture_exp)
        auto_cs = guessColorspace(name)
        if not auto_cs:
            auto_cs = makeTx.guessColorspace(iinfo)
        if len(texture_data['usage']):
            for node in texture_data['usage'].keys():
                cs = get_colorspace(node)
                if cs == 'auto':
                    cs = auto_cs
                if cs == 'linear':
                    cs = 'Raw'

                if ext == '.tx':
                    txstatus = 'onlytx'
                    txpath = texture
                else:
                    txpath_exp = get_output_tx_path(texture_exp, cs, render_colorspace)
                    ui_txpath = get_output_tx_path(texture, cs, render_colorspace)
                    if os.path.isfile(txpath_exp):
                        txstatus = 'hastx'
                        txpath = ui_txpath
                    else:
                        txstatus = 'notx'
                        txpath = None

                if not os.path.isfile(texture_exp):
                    txstatus = 'missing'

                if texture not in textures.keys():
                    textures.setdefault(
                        texture, copy.deepcopy(textures[texture]))

                if txstatus not in combined_status:
                    combined_status.append(txstatus)

                texture_data['usage'][node]['root'] = root
                texture_data['usage'][node]['name'] = node
                texture_data['usage'][node]['status'] = txstatus
                texture_data['usage'][node]['txpath'] = txpath
                texture_data['usage'][node]['path'] = texture
                texture_data['usage'][node]['colorspace'] = cs
                for k, v in iinfo.items():
                    texture_data['usage'][node][k] = v

            if (len(combined_status) > 1):
                txstatus = "mixed"
            else:
                txstatus = txstatus

        else:
            cs = auto_cs

            if ext == '.tx':
                txstatus = 'onlytx'
                txpath = texture
            else:
                txpath_exp = get_output_tx_path(texture_exp, cs, render_colorspace)
                ui_txpath = get_output_tx_path(texture, cs, render_colorspace)
                if os.path.isfile(txpath_exp):
                    txstatus = 'hastx'
                    txpath = ui_txpath
                else:
                    txstatus = 'notx'
                    txpath = None

            if not os.path.isfile(texture_exp):
                txstatus = 'missing'

            textures[texture]['txpath'] = txpath
            textures[texture]['colorspace'] = cs

        textures[texture]['root'] = root
        textures[texture]['name'] = name
        textures[texture]['status'] = txstatus
        textures[texture]['path'] = texture

    return textures


def get_output_tx_path(input_file, colorspace, render_colorspace):
    colorspace = render_colorspace = None
    input_file = re.sub(r"\.[^.]+$", ".tx", input_file)
    txpath = str(ai.AiTextureGetTxFileName(input_file, colorspace, render_colorspace, None))
    return txpath


def build_tx_arguments(
        update=True,
        verbose=True,
        nans=True,
        stats=True,
        unpremutl=True,
        threads=None,
        preset=None,
        extra_args=None):
    '''Builds the maketx argument list'''
    args = []
    if update:
        args.append('-u')

    if verbose:
        args.append('-v')

    if nans:
        args.append('--checknan')

    if stats:
        args.append('--stats')

    if unpremutl:
        args.append('--unpremult')

    if preset is not None:
        args.append('--' + preset)

    if extra_args:
        args += [x for x in extra_args.split(' ') if x]

    if threads is not None and threads > 0:
        args += ['--threads', str(threads)]

    return args


class DummyManager(object):
    """docstring for DummyManager"""

    def __init__(self):
        super(DummyManager, self).__init__()
        self.filesToCreate = []
        self.textures = []

    def on_refresh(self):
        """ dummy method """
        pass

    def get_use_autotx(self):
        return True

    def set_status(self, index, status):
        # self.textures[index]['status'] = status
        pass

    def get_status(self, index):
        return self.textures[index]['status']

    def get_tx_args(self):
        return ""

    def get_selected_textures(self):
        _textures = get_scanned_files(scene_default_texture_scan)
        self.textures = []
        i = 0
        for k in sorted(_textures.keys()):
            _textures[k]['index'] = i
            for node in _textures[k]['usage'].keys():
                _textures[k]['usage'][node]['item'] = None
                self.textures.append(_textures[k]['usage'][node])
            i += 1

        return self.textures


def updateAllTx(force, threaded=True):
    manager = DummyManager()

    # check if we are in batch mode
    if not cmds.about(batch=True):
        mayawindow = getMayaWindow()
        thread = MakeTxThread(manager, mayawindow)
        thread.set_forced(force)
        progress = QtWidgets.QProgressDialog("processing textures...", "Abort", 0, 2, mayawindow)
        progress.forceShow()
        progress.setWindowModality(QtCore.Qt.WindowModal)

        progress.canceled.connect(thread.cancel_tx)
        thread.maxProgress.connect(progress.setMaximum)
        thread.progress.connect(progress.setValue)
        thread.finished.connect(progress.deleteLater)

        thread.start()

    else:

        processor = TxProcessor(manager)
        return processor.createTx()

    return False
