import logging
import os

import bpy

from batched_blender.constants import Constants

class SubmitJobOperator(bpy.types.Operator):
    bl_idname = Constants.OP_ID_SUBMIT_JOB
    bl_label = "SubmitJobOperator"
    job_type = bpy.props.StringProperty()

    def __init__(self):
        self.log = logging.getLogger(Constants.LOG_NAME)

    def execute(self, context):
        # todo: check for and throw error if no job_type set
        self.log.debug("SubmitJobOperator.execute: " + self.job_type)

        handler = context.scene.batch_session.request_handler
        launch_url = str.format("market/blender/actions/{}/{}", self.job_type, "submit")
        if not bpy.data.filepath:
            handler.call_batch_labs(launch_url)
        else:
            handler.call_batch_labs(
                launch_url,
                {Constants.SUBMIT_JOB_DICT_SCENE_FILE: os.path.basename(bpy.data.filepath)})

        return {"FINISHED"}
