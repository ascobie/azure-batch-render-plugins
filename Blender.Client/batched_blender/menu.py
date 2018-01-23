import logging
import urllib.request
import json
import bpy

from urllib.error import HTTPError

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
    bl_idname = "BATCH_LABS_submit_menu"
    bl_label = "Submit Job"

    def __init__(self):
        self.log = logging.getLogger('batched_blender')


    def draw(self, context):
        if len(_SUBMIT_MENU_OPTIONS) == 0:
            try:
                self.init_menu_items()
            except Exception as error:
                self.log.error("Failed to load job submit menu items")
        else:
            self.log.debug("menu items not null")

        self.log.debug("... about to show menu ...")
        for option in _SUBMIT_MENU_OPTIONS:
            self.layout.operator("batch_shared.submit_job", text=option.name).job_type=option.key

        self.log.debug("Sub-menu drawn")


    def init_menu_items(self):
        self.log.debug("Initializing submit menu items")
        del _SUBMIT_MENU_OPTIONS[:]

        try:
            response = urllib.request.urlopen("https://raw.githubusercontent.com/Azure/BatchLabs-data/master/ncj/blender/index.json")
        except HTTPError as error:
            self.log.error("Failed to call the GitHub BatchLabs-data repository", str(error))
            raise

        try:
            str_response = response.read().decode("utf-8")
        except Exception as error:
            self.log.error("An error occurred while reading the response", str(error))
            raise

        json_content = json.loads(str_response)
        for entry in json_content:
            self.log.debug("entry: " + str(entry))
            _SUBMIT_MENU_OPTIONS.append(SubmitMenuOption(entry["id"], entry["name"]))


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
    bl_label = "Azure Batch Rendering"


    def __init__(self):
        self.log = logging.getLogger('batched_blender')
        self.log.debug("Initializing main menu")


    def draw(self, context):
        self.layout.menu("BATCH_LABS_submit_menu")
        self.layout.operator("batch_shared.download_renders", text="Download Renders")
        self.layout.operator("batch_shared.monitor_pools", text="Monitor Pools")
        self.layout.operator("batch_shared.monitor_jobs", text="Monitor Jobs")
        self.log.debug("Main menu drawn")
