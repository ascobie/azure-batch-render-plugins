import bpy
import logging
import webbrowser

class SubmitJobOperator(bpy.types.Operator):
    bl_idname = "batch_shared.submit_job"
    bl_label = "SubmitJobOperator"
    job_type = bpy.props.StringProperty()

    def __init__(self):
        self.log = logging.getLogger("batched_blender")

    def execute(self, context):
        self.log.debug("SubmitJobOperator.execute: " + self.job_type)
        #webbrowser.open("ms-batchlabs://route/market/blender/actions/render-movie-linux/submit", 1, True)

        return {"FINISHED"}
