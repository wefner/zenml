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
from logging.handlers import TimedRotatingFileHandler
from typing import Any, ClassVar
from zenml.log_collector.base_log_collector import (
    BaseLogCollector, CustomFormatter
)


class FileLogCollector(BaseLogCollector):
    FLAVOR: ClassVar[str] = "default"

    def add_custom_handler(self, filename: str) -> Any:
        """Return a file handler for logging."""
        file_handler = TimedRotatingFileHandler(f"{filename}.log",
                                                when="midnight")
        file_handler.setFormatter(CustomFormatter())
        return file_handler
