---
description: Registering stacks, components, and flavors.
---

## Registering Stacks, Components, and Flavors

You can combine various MLOps tools into a ZenML stack as follows:

1. [Register a stack component](#registering-stack-components) to configure each tool
using `zenml <STACK_COMPONENT> register`.
2. [Register a stack](#registering-a-stack) to bring a particular combination of stack components 
together using `zenml stack register`.
3. [Register a stack flavor](../../advanced-guide/stacks/custom-flavors.md) to add a
new tool to the ZenML flavor registry, if the tool you are looking for is not supported out-of-the-box,
or if you want to modify standard behavior of standard flavors.

In this guide, we will learn about the first two, while the last is a slightly
[advanced topic covered later](../../advanced-guide/stacks/custom-flavors.md).

### Registering Stack Components

First, you need to create a new instance of the respective stack component
with the desired flavor using `zenml <STACK_COMPONENT> register <NAME> --flavor=<FLAVOR>`. 
Most flavors require further parameters that you can pass as additional
arguments `--param=value`, similar to how we passed the flavor.

E.g., to register a *local* artifact store, we could use the following command:

```shell
zenml artifact-store register <ARTIFACT_STORE_NAME> \
    --flavor=local \
    --path=/path/to/your/store
```

In case you do not know all the available parameters, you can also use the 
interactive mode to register stack components. This will then walk you through 
each parameter (to skip just press ENTER):

```shell
zenml artifact-store register <ARTIFACT_STORE_NAME> \
    --flavor=local -i
```

Or you could simply describe the flavor to give a list of configuration available:

```shell
zenml artifact-store flavor describe local
```

After registering, you should be able to see the new artifact store in the
list of registered artifact stores, which you can access using the following command:

```shell
zenml artifact-store list
```

Or on the UI directly:

![Orchestrator list](../../assets/starter_guide/stacks/01_orchestrator_list.png)

{% hint style="info" %}
Our CLI features a wide variety of commands that let you manage and use your
stack components and flavors. If you would like to learn more, please run
`zenml <STACK_COMPONENT> --help` or visit [our CLI docs](https://apidocs.zenml.io/latest/cli/).
{% endhint %}

### Registering a Stack

After registering each tool as the respective stack components, you can combine
all of them into one stack using the `zenml stack register` command:

```shell
zenml stack register <STACK_NAME> \
    --orchestrator <ORCHESTRATOR_NAME> \
    --artifact-store <ARTIFACT_STORE_NAME> \
    ...
```

{% hint style="info" %}
You can use `zenml stack register --help` to see a list of all possible 
arguments to the `zenml stack register` command, including a list of which 
option to use for which stack component.
{% endhint %}

And see them on the UI:

![Stack list](../../assets/starter_guide/stacks/02_stack_list.png)

### Activating a Stack

Finally, to start using the stack you just registered, set it as active:

```shell
zenml stack set <STACK_NAME>
```
Now all your code is automatically executed using this stack.

{% hint style="info" %}
Some advanced stack component flavors might require connecting to remote 
infrastructure components prior to running code on the stack. This can be done
using `zenml stack up`. See the [Managing Stack States](../../advanced-guide/stacks/stack-state-management.md)
section for more details.
{% endhint %}

### Changing Stacks

If you have multiple stacks configured, you can switch between them using the
`zenml stack set` command, similar to how you [activate a stack](#activating-a-stack).

### Unregistering Stacks

To unregister (delete) a stack and all of its components, run

```shell
zenml stack delete <STACK_NAME>
```

to delete the stack itself, followed by

```shell
zenml <STACK_COMPONENT> delete <STACK_COMPONENT_NAME>
```

to delete each of the individual stack components.

{% hint style="warning" %}
If you provisioned infrastructure related to the stack, make sure to
deprovision it using `zenml stack down --force` before unregistering the stack.
See the [Managing Stack States](../advanced-usage/stack-state-management.md) section for more details.
{% endhint %}

# Older content (page 2)

ZenML has two main locations where it stores information on the local machine.
These are the [Global Configuration](../../resources/global-config.md) and the 
_Repository_. The latter is also referred to as the _.zen folder_.

The ZenML **Repository** related to a pipeline run is the folder that contains 
all the files needed to execute the run, such as the respective Python scripts
and modules where the pipeline is defined, or other associated files.
The repository plays a double role in ZenML:

* It is used by ZenML to identify which files must be copied into Docker images 
in order to execute pipeline steps remotely, e.g., when orchestrating pipelines
with [Kubeflow](../../component-gallery/orchestrators/kubeflow.md).
* It defines the local active [Stack](#stacks) that will be used when running
pipelines from the repository root or one of its sub-folders, as shown
[below](#setting-the-local-active-stack).

## Registering a Repository

You can register your current working directory as a ZenML
repository by running:

```bash
zenml init
```

This will create a `.zen` directory, which contains a single
`config.yaml` file that stores the local settings:

```yaml
active_project_name: null
active_stack_name: default
```

{% hint style="info" %}
It is recommended to use the `zenml init` command to initialize a ZenML
_Repository_ in the same location of your custom Python source tree where you
would normally point `PYTHONPATH`, especially if your Python code relies on a
hierarchy of modules spread out across multiple sub-folders.

ZenML CLI commands and ZenML code will display a warning if they are not running
in the context of a ZenML repository, e.g.:

```shell
stefan@aspyre2:/tmp$ zenml stack list
Unable to find ZenML repository in your current working directory (/tmp) or any parent directories. If you want to use an existing repository which is in a different location, set the environment variable 'ZENML_REPOSITORY_PATH'. If you want to create a new repository, run zenml init.
Running without an active repository root.
Using the default local database.
┏━━━━━━━━┯━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┓
┃ ACTIVE │ STACK NAME │ ARTIFACT_STORE │ METADATA_STORE │ ORCHESTRATOR ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃   👉   │ default    │ default        │ default        │ default      ┃
┗━━━━━━━━┷━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛
```
{% endhint %}

## Setting the Local Active Stack

One of the most useful features of repositories is that you can configure a
different active stack for each of your projects. This is great if
you want to use ZenML for multiple projects on the same machine. Whenever you
create a new ML project, we recommend you run `zenml init` to create a separate
repository, then use it to define your stacks:

```bash
zenml init
zenml stack register ...
zenml stack set ...
```

If you do this, the correct stack will automatically get activated
whenever you change directory from one project to another in your terminal.

{% hint style="info" %}
Note that the stacks and stack components are still stored globally, even when
running from inside a ZenML repository. It is only the active stack setting
that can be configured locally.
{% endhint %}

### Detailed Example

<details>
<summary>Detailed usage example of local stacks</summary>

The following example shows how the active stack can be configured locally for a
project without impacting the global settings:

```
/tmp/zenml$ zenml stack list
Unable to find ZenML repository in your current working directory (/tmp/zenml)
or any parent directories. If you want to use an existing repository which is in
a different location, set the environment variable 'ZENML_REPOSITORY_PATH'. If
you want to create a new repository, run zenml init.
Running without an active repository root.
Using the default local database.
┏━━━━━━━━┯━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┓
┃ ACTIVE │ STACK NAME │ ARTIFACT_STORE │ METADATA_STORE │ ORCHESTRATOR ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃   👉   │ default    │ default        │ default        │ default      ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃        │ zenml      │ default        │ default        │ default      ┃
┗━━━━━━━━┷━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛

/tmp/zenml$ zenml init
ZenML repository initialized at /tmp/zenml.
The local active stack was initialized to 'default'. This local configuration will
only take effect when you're running ZenML from the initialized repository root,
or from a subdirectory. For more information on repositories and configurations,
please visit https://docs.zenml.io/developer-guide/stacks-repositories.


$ zenml stack list
Using the default local database.
┏━━━━━━━━┯━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┓
┃ ACTIVE │ STACK NAME │ ARTIFACT_STORE │ METADATA_STORE │ ORCHESTRATOR ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃   👉   │ default    │ default        │ default        │ default      ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃        │ zenml      │ default        │ default        │ default      ┃
┗━━━━━━━━┷━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛

/tmp/zenml$ zenml stack set zenml
Using the default local database.
Active repository stack set to: 'zenml'

/tmp/zenml$ zenml stack list
Using the default local database.
┏━━━━━━━━┯━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┓
┃ ACTIVE │ STACK NAME │ ARTIFACT_STORE │ METADATA_STORE │ ORCHESTRATOR ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃        │ default    │ default        │ default        │ default      ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃   👉   │ zenml      │ default        │ default        │ default      ┃
┗━━━━━━━━┷━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛

/tmp/zenml$ cd ..
/tmp$ zenml stack list
Unable to find ZenML repository in your current working directory (/tmp) or any
parent directories. If you want to use an existing repository which is in a
different location, set the environment variable 'ZENML_REPOSITORY_PATH'. If you
want to create a new repository, run zenml init.
Running without an active repository root.
Using the default local database.
┏━━━━━━━━┯━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┓
┃ ACTIVE │ STACK NAME │ ARTIFACT_STORE │ METADATA_STORE │ ORCHESTRATOR ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃   👉   │ default    │ default        │ default        │ default      ┃
┠────────┼────────────┼────────────────┼────────────────┼──────────────┨
┃        │ zenml      │ default        │ default        │ default      ┃
┗━━━━━━━━┷━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛
```

</details>

### Accessing the Active Stack

The following code snippet shows how you can retrieve or modify information
of your active stack and stack components in Python:

```python
from zenml.client import Client

client = Client()
active_stack = client.active_stack
print(active_stack.name)
print(active_stack.orchestrator.name)
print(active_stack.artifact_store.name)
print(active_stack.artifact_store.path)
```

### Registering and Changing Stacks

In the following we use the repository to register a new ZenML stack called
`local` and set it as the active stack of the repository:

```python
from zenml.repository import Repository
from zenml.artifact_stores import LocalArtifactStore
from zenml.orchestrators import LocalOrchestrator
from zenml.stack import Stack


repo = Repository()

# Create a new orchestrator
orchestrator = LocalOrchestrator(name="local")

# Create a new artifact store
artifact_store = LocalArtifactStore(
    name="local",
    path="/tmp/zenml/artifacts",
)

# Create a new stack with the new components
stack = Stack(
    name="local",
    orchestrator=orchestrator,
    artifact_store=artifact_store,
)

# Register the new stack
repo.register_stack(stack)

# Set the stack as the active stack of the repository
repo.activate_stack(stack.name)
```