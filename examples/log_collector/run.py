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
import logging

from zenml.pipelines import pipeline
from zenml.steps import step


@step
def step_that_logs(step_logger: logging.Logger):
    step_logger.warning("OH YEAH!")
    step_logger.info("OH YEAH!")
    step_logger.error("Kool Aid Man")


@pipeline(enable_cache=False)
def pipeline_that_logs(a):
    a()


pipeline_that_logs(a=step_that_logs()).run()


