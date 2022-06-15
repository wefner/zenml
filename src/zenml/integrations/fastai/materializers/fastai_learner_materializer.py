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
"""Implementation of the fastai Learner materializer."""

import os

from fastai.learner import Learner

from zenml.artifacts import ModelArtifact
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer

DEFAULT_FILENAME = "model.pkl"


class FastaiLearnerMaterializer(BaseMaterializer):
    """Materializer to read/write fastai models."""

    ASSOCIATED_TYPES = (Learner,)
    ASSOCIATED_ARTIFACT_TYPES = (ModelArtifact,)

    def handle_input(self, model: Learner) -> Learner:
        """Reads and returns a fastai model.

        Only loads the model, not the checkpoint.

        Args:
            model: The model to load.

        Returns:
            A loaded fastai model.
        """
        super().handle_input(model)

        with fileio.open(
            os.path.join(self.artifact.uri, DEFAULT_FILENAME), "rb"
        ) as f:
            return model.load(f)  # type: ignore[no-untyped-call]  # noqa

    def handle_return(self, model: Learner) -> None:
        """Writes a PyTorch model, as a model and a checkpoint.

        Args:
            model: A fastai model
        """
        super().handle_return(model)

        # Save entire model to artifact directory
        with fileio.open(
            os.path.join(self.artifact.uri, DEFAULT_FILENAME), "wb"
        ) as f:
            model.save(f)  # type: ignore[no-untyped-call]  # noqa
