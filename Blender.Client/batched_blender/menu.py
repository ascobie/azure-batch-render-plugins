import logging
import urllib.request
import json
import bpy

from urllib.error import HTTPError
from batched_blender.constants import Constants

_SUBMIT_MENU_OPTIONS = []

class SubmitMenuOption:
    def __init__(self, key, name):
        self.key = key
        self.name = name

class BatchLabsBlenderSubMenu(bpy.types.Menu):
    """
    Submit job sub menu. Calls off to the BatchLabs-data repo to get the submit job
    option types and displays them.
    """
    bl_idname = Constants.SUBMIT_MENU_ID
    bl_label = Constants.SUBMIT_MENU_LABEL

    def __init__(self):
        self.log = logging.getLogger(Constants.LOG_NAME)

    def draw(self, context):
        if len(_SUBMIT_MENU_OPTIONS) == 0:
            try:
                self.init_menu_items()
            except:
                self.log.error("Failed to load job submit menu items")

        self.log.debug("Showing submit job menu")
        if len(_SUBMIT_MENU_OPTIONS) > 0:
            for option in _SUBMIT_MENU_OPTIONS:
                self.layout.operator(Constants.OP_ID_SUBMIT_JOB, text=option.name).job_type = option.key
        else:
            self.log.debug("Submit job menu empty")
            self.log.debug("Check: " + Constants.DATA_REPO_APP_INDEX_URL)

    def init_menu_items(self):
        self.log.debug("Initializing submit menu items")
        del _SUBMIT_MENU_OPTIONS[:]

        try:
            response = urllib.request.urlopen(Constants.DATA_REPO_APP_INDEX_URL)
        except HTTPError as error:
            self.log.error("Failed to call the GitHub BatchLabs-data repository: " + str(error))
            raise

        try:
            str_response = response.read().decode("utf-8")
        except Exception as error:
            self.log.error("An error occurred while reading the response: " + str(error))
            raise

        json_content = json.loads(str_response)
        for action in json_content:
            self.log.debug("Found action: " + str(action))
            _SUBMIT_MENU_OPTIONS.append(SubmitMenuOption(action["id"], action["name"]))


class BatchLabsBlenderMenu(bpy.types.Menu):
    """
    BatchLabs menu options for Blender.
    Displays a menu item under the info > render menu.
    Azure Batch Rendering
        > Submit Job (BatchLabsBlenderSubMenu)
            > [Dynamic submit actions ...]
        > Download Renders
        > Monitor Pools
        > Monitor Jobs
    """
    bl_label = Constants.MAIN_MENU_LABEL

    def __init__(self):
        self.log = logging.getLogger(Constants.LOG_NAME)

    def draw(self, context):
        self.layout.menu(Constants.SUBMIT_MENU_ID)
        self.layout.operator(Constants.OP_ID_DOWNLOAD_RENDERS, text="Download Renders")
        self.layout.operator(Constants.OP_ID_MONITOR_JOBS, text="Monitor Jobs")
        self.layout.operator(Constants.OP_ID_MONITOR_POOLS, text="Monitor Pools")
        self.log.debug("BatchLabs menu shown")
