import bpy
import json
import os
import urllib.request
import uuid
import webbrowser

from batched_blender.constants import Constants
from urllib.error import HTTPError

class SubmitMenuOption:
    def __init__(self, key, name):
        self.key = key
        self.name = name

class BatchLabsRequestHandler(object):
    """
    Handles calls to BatchLabs as well as requests to the NCJ data repo
    """
    _session_id = None
    _submit_actions = []
    _logger = None

    def __init__(self, session_id, logger):
        print("BatchLabsRequestHandler init")
        self._session_id = session_id
        self._logger = logger

        self._load_menu_options()
        self._logger.debug("Initialised BatchLabsRequestHandler")

    def menu_options(self):
        return self._submit_actions

    def call_batch_labs(self, action_str, argument_dict=None):
        batchlabs_url = str.format(
            "{}/{}?session={}",
            Constants.BATCH_LABS_BASE_URL,
            action_str,
            self._session_id)

        # todo: append any dictionary arguments
        self._logger.debug("Calling labs with URL: " + batchlabs_url)

        webbrowser.open(batchlabs_url, 1, True)

    def _load_menu_options(self):
        """
        Calls the BatchLabs-data repo to load the submit actions
        for this application.
        """
        self._logger.debug("Initializing submit menu items")
        del self._submit_actions[:]

        try:
            response = urllib.request.urlopen(Constants.DATA_REPO_APP_INDEX_URL)
        except HTTPError as error:
            self._logger.error("Failed to call the GitHub BatchLabs-data repository: " + str(error))
            raise

        try:
            str_response = response.read().decode("utf-8")
        except Exception as error:
            self._logger.error("An error occurred while reading the response: " + str(error))
            raise

        json_content = json.loads(str_response)
        for action in json_content:
            self._logger.debug("Found action: " + str(action))
            self._submit_actions.append(SubmitMenuOption(action["id"], action["name"]))
