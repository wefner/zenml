#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
from io import StringIO
import logging

from typing import Any, ClassVar
from zenml.log_collector.base_log_collector import (
    BaseLogCollector, CustomFormatter
)


class FileLogCollector(BaseLogCollector):

    FLAVOR: ClassVar[str] = "default"

    _log_stream = None
    _stream_handler: logging.Handler = None
    _file_obj = None
    _log_path = None

    def add_custom_handler(self, step_name: str, log_base_path: str):
        """Return a file handler for logging."""
        self._file_obj = open(f"{log_base_path}/{step_name}.log", 'w+')
        # self._log_stream = StringIO()
        self._stream_handler = logging.StreamHandler(self._file_obj)
        self._stream_handler.setFormatter(CustomFormatter())
        self.get_logger(step_name).addHandler(self._stream_handler)

    def remove_custom_handler(self, step_name: str):
        # self._file_obj.close()
        self.get_logger(step_name).removeHandler(self._stream_handler)
        self._file_obj.close()
