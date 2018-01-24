import bpy
import logging
import webbrowser

from batched_blender.constants import Constants

class DownloadRendersOperator(bpy.types.Operator):
    bl_idname = Constants.OP_ID_DOWNLOAD_RENDERS
    bl_label = "DownloadRendersOperator"

    def __init__(self):
        self.log = logging.getLogger(Constants.LOG_NAME)

    def execute(self, context):
        self.log.debug("DownloadRendersOperator.execute")
        webbrowser.open(str.format("{}/{}", Constants.BATCH_LABS_BASE_URL, "data"), 1, True)

        return {"FINISHED"}
