#!/usr/bin/env bash

set -Eeo pipefail

pre_run () {
  zenml integration install fastai
  pip install huggingface_hub
}

pre_run_forced () {
  zenml integration install fastai -y
  pip install huggingface_hub -Uqq
}
