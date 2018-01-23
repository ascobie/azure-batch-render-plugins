import bpy
import logging
import webbrowser
import os

from batched_blender.utils import BatchOps

class BatchSettings(object):
    """
    Initializes and manages the BatchLabs plugin session.
    Registers all classes and handles all sub-pages. Configures logging and
    User Preferences.
    """

    def __init__(self):
        self.props = self._register_props()
        self.log = self._configure_logging()
        self.ops = self._register_ops()
        self.log.debug("Initialised BatchLabs Blender plugin")


    def _register_props(self):
        """
        Retrieves the shared addon properties - in this case the User
        Preferences.

        :Returns:
            - :class:`.UserPreferences`
        """
        props = bpy.context.user_preferences.addons[__package__].preferences
        if not os.path.isdir(props.log_dir):
            try:
                os.mkdir(props.log_dir)
            except:
                raise EnvironmentError(
                    "Data directory not created at '{0}'.\n"
                    "Please ensure you have adequate permissions.".format(props.log_dir))

        return props


    def _configure_logging(self):
        """
        Configures the logger for the addon based on the User Preferences.
        Sets up a stream handler to log to Blenders console and a file
        handler to log to the Batch log file.
        """
        logger = logging.getLogger('batched_blender')
        logger.setLevel(int(self.props.log_level))
        console_format = logging.Formatter("Batch: [%(levelname)s] %(message)s")
        file_format = logging.Formatter("%(asctime)-15s [%(levelname)s] %(module)s: %(message)s")

        console_logging = logging.StreamHandler()
        console_logging.setFormatter(console_format)
        logger.addHandler(console_logging)
        logfile = os.path.join(self.props.log_dir, "batched_blender.log")
        file_logging = logging.FileHandler(logfile)
        file_logging.setFormatter(file_format)
        logger.addHandler(file_logging)

        return logger


    def _register_ops(self):
        """
        Registers the shared operators with a batch_shared prefix.

        :Returns:
            - A list of the names (str) of the registered operators.
        """
        ops = []
        #ops.append(BatchOps.register("shared.submit_job", "Submit Job", self._submit_job))
        ops.append(BatchOps.register("shared.monitor_jobs", "Monitor Jobs", self._monitor_jobs))
        ops.append(BatchOps.register("shared.monitor_pools", "Monitor Pools", self._monitor_pools))
        ops.append(BatchOps.register("shared.download_renders", "Download Renders", self._download_renders))

        return ops


    def _submit_job(self, op, context):
        """
        The execute method for the shared._submit_job operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        self.log.debug("Submit job ... " + bpy.data.filepath)
        self.log.debug("op " + str(op))
        self.log.debug("context " + str(context))
        self.log.debug(bpy.context.scene)
        # webbrowser.open("ms-batchlabs://route/market/blender/actions/render-movie-linux/submit", 1, True)

        return {'FINISHED'}


    def _monitor_jobs(self, op, context):
        """
        The execute method for the shared._monitor_jobs operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        self.log.debug("Monitor jobs ... ")
        webbrowser.open("ms-batchlabs://route/jobs", 1, True)

        return {'FINISHED'}


    def _monitor_pools(self, op, context):
        """
        The execute method for the shared._monitor_pools operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        self.log.debug("Monitor pools ... ")
        webbrowser.open("ms-batchlabs://route/pools", 1, True)

        return {'FINISHED'}


    def _download_renders(self, op, context):
        """
        The execute method for the shared._download_renders operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        self.log.debug("Download renders ... ")
        webbrowser.open("ms-batchlabs://route/data", 1, True)

        return {'FINISHED'}


    def redraw(self):
        """
        Somewhat hacky way to force Blender to redraw the UI.
        """
        bpy.context.scene.objects.active = bpy.context.scene.objects.active
