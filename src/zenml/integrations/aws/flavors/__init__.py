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
"""AWS integration flavors."""

from zenml.integrations.aws.flavors.aws_container_registry_flavor import (
    AWSContainerRegistryConfig,
    AWSContainerRegistryFlavor,
)
from zenml.integrations.aws.flavors.aws_secrets_manager_flavor import (
    AWSSecretsManagerConfig,
    AWSSecretsManagerFlavor,
)
from zenml.integrations.aws.flavors.sagemaker_step_operator_flavor import (
    SagemakerStepOperatorConfig,
    SagemakerStepOperatorFlavor,
)

__all__ = [
    "AWSContainerRegistryFlavor",
    "AWSContainerRegistryConfig",
    "AWSSecretsManagerFlavor",
    "AWSSecretsManagerConfig",
    "SagemakerStepOperatorFlavor",
    "SagemakerStepOperatorConfig",
]
