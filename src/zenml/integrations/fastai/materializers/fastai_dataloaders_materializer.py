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
"""Implementation of the fastai DataLoader materializer."""

import os
from typing import cast

import torch
from fastai.data.core import DataLoaders

from zenml.artifacts import DataArtifact
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer

DEFAULT_FILENAME = "fastai_dataloaders.pt"


class FastaiDataLoadersMaterializer(BaseMaterializer):
    """Materializer to read/write fastai dataloaders."""

    ASSOCIATED_TYPES = (DataLoaders,)
    ASSOCIATED_ARTIFACT_TYPES = (DataArtifact,)

    def handle_input(self, data_type: DataLoaders) -> DataLoaders:
        """Reads and returns a fastai DataLoader.

        Args:
            data_type: The type of the dataloader to load.

        Returns:
            A loaded fastai dataloader.
        """
        super().handle_input(data_type)
        with fileio.open(
            os.path.join(self.artifact.uri, DEFAULT_FILENAME), "rb"
        ) as f:
            return cast(DataLoaders, torch.load(f))  # type: ignore[no-untyped-call]  # noqa

    def handle_return(self, dataloaders: DataLoaders) -> None:
        """Writes a fastai dataloader.

        Args:
            dataloader: A fastai.data.core.DataLoader
        """
        super().handle_return(dataloaders)

        # Save entire dataloader to artifact directory
        with fileio.open(
            os.path.join(self.artifact.uri, DEFAULT_FILENAME), "wb"
        ) as f:
            torch.save(dataloaders, f)
