Python Adapter Template for Action Orchestrator
=========================



## Pre-reqs
1. AO instance running on K8S
2. Python and Wheel installed somewhere (prefer on AO instance)
3. For wheel, do `pip install wheel` with Administrator level
4. Wheel is also found here - https://pypi.org/project/wheel/

## Install Video

TBD

## Install (Full Make Method)

1. Create a directory on your AO instance
2. Download the git repo and load the files to your server. Use the download button or `git clone`
3. Create the Schemas
    1. Either via UI or via API steps below (Video of that here - https://cisco.webex.com/cisco/lsr.php?RCID=7a83f541c13a4cbea930a6f462ecfbd5 password:QwqBBY2m)
    2. Or Via POST API call against https://server:port/api/v1/schemas (AO standalone)
    3. Or Via POST API call against https://server:port/be-console/api/v1/schemas (Complete Suite+AO)
    4. Run the API calls with the .json schema files in the /adapter_schema directory
4. Schema must be created in the order of Runtime User, Adapter, Target, Activties, Events
   
    **Note:** order of activities does not matter
5. In your adapter directory, build your wheel file with the command `python setup.py bdist_wheel` . If you do not have this on your AO server then do it where ever you have wheel and python installed, but it must be in the same directory you created above.
    **NOTE:** If you wish to increase this build time, you need to comment out the jail info. See article: TBD
    **NOTE:** You *should not* leave jail stuff commented out for production builds, only for quick dev builds
6. Build the container by running `docker build . -t <TAG> -f Dockerfile`
     1. Your <TAG> should be the location of the container in a repo or local
     2. You can also make it a container repo like "containers.cisco.com/shaurobe/my-adapter"
7. To deploy, run the Kubernetes command `kubectl create -f yaml/<some name>-adapter.yaml -n cisco`
8. Restart your console pod in AO as needed

## Install (Easy Method)

1. Follw steps 1-4 in the Full Make method above
2. Deploy the pod via Kubernetes command `kubectl create -f yaml/<some name>-adapter.yaml -n cisco'
3. Restart your console pod in AO as needed

## How To VODs

1. Upgrade schema - https://cisco.webex.com/cisco/lsr.php?RCID=0aab8090027d42efbe7dd6fdc80b05b5
   password: hVjfm9UF
2. See complete how-to develop an activity at https://techzone.cisco.com/t5/Action-Orchestrator-AO/Action-Orchestrator-Tech-Blog-Training-Information-and-More/ta-p/1254715

## Upgrade


**Note:** Will not make major schema changes until PATCH is supported


1. If you want to make it from scratch do steps 2-4, if you want to just update to latest code, do step 4 
2. Load the latest wheel and docker file
3. Re-run steps 5 and 6 above
4. Restart both the console pod and adapter pod

**Note:** The below is generic information about the Python Adapter setup for AO




Action Orchestrator Python Information 
=========================

## Overview
This template can be used to create a python based adapter.
The template is written in Python.


### Notes
Template has three actions:
1. hello_world
2. create_template
3. run_script
There is also one action which is supposed to be by default in every adapter, verify_target.
Usually verify_target action is used to verify connection and credentials to the target during its creation in UI.


### Run adapter locally
Run adapter locally
1. Install required packages: python-dotenv, six, requests.
2. Create self-signed certificates in the custom python adapter project folder:
    Run "make create-certs" - this will create all needed certificates to run adapter https service  locally

After running certificate creation commands you will have the following files created:
    "secrets/ssl/cert/certificate.pem"
    "secrets/ssl/cert/private_key.pem"

If you want to use your own certificates, then add following environment variables:
    export CERTFILE=path_to_certificate.pem
    export PKEYFILE=path_to_private_key.pem
    export CAFILE=path_to_ca_certificate.pem

3.  Prepare JAIL environment.

Download Jailkit package and follow the INSTALL.TXT instructions.

Here are common commands to install Jail environment:
    wget http://olivier.sessink.nl/jailkit/jailkit-2.20.tar.gz
    tar -xzvf jailkit-2.20.tar.gz
    cd jailkit-2.20;./configure && make && make install
    mkdir /jail (or use some other directory)
    jk_init -j /jail jk_lsh
    PYTHON_PATH=$(which python)
    PYTHON_LIB_PATH=$(python -c "import os, inspect; print os.path.dirname(inspect.getfile(inspect))")
    jk_cp -j /jail $PYTHON_PATH
    jk_cp -j /jail $PYTHON_LIB_PATH
    groupadd script_executer
    adduser script_executer -G script_executer
    jk_jailuser -n -j /jail script_executer

Export environment variables needed to run the adapter:
    export JAIL_DIR=/jail
    export JAIL_USERNAME=script_executer
    export JAIL_GROUPNAME=script_executer

4. Add the custom adapter project directory to PYTHONPATH using the following command: export PYTHONPATH=PathToCustomPythonAdapterProject

5. Run adapter:  python worker/activities-worker

(worker/activities-worker is the main entry point to run the adapter)

Worker URL for requests - http://localhost:8082/api/v1/function

### Files
1. setup.py, setup.cfg,requires.txt - are used for building python package
2. Dockerfile - used to create adapter docker container
Example commands:
cd 'cloned adapter repo folder'
python setup.py bdist_wheel
docker build -t ad-template ( ad-template - container name for the adapter)

3. Jenkinsfile, Jenkinsfile-lambda - used in jenkins jobs
4. event-json - contains sample api calls to run each action


### activities_python Folders

Actions folder contains three template actions and sample test files:
1. Hello World - represents an action to demonstrate input and output parameters.
2. Create Template - represents an action with api POST request. BasicConstants.ACTIVITY_2_URL is api relative URL for the action2.
3. Run Script - represents an action to run python script in jail env.
4. Verify Target - represents an action for verifying target.

common folder - is a common adapter library.

constants folder files: You can change the values of these constants to customize your adapter.

events/event_resolver.py : Type resolver for incoming requests. We have four event types with corresponding actions.

pythonutils - contains different models used in actions.


Other folders/files:
--------------------

functions/lambda_function_name/handler.py is used to run adapter as aws lambda function. The name 'lambda_function_name' should be the same as name in adapter lambda schema.

schemas/generate_schemes.py - is used to generate schemes for current template adapter. you can simply run it in python.
If you want to make your own changes in schemes please refer to the schemes documentation.

scripts/run_test.sh - script is used in build to run tests

worker/activities-worker - is used to run adapter as microservice


#Easy Tag Replace#
change to name of your adapter [template-adapter] e.g[mysql-adapter]

version number [1.0]

Yaml file  [demo-adapter] e.g[mysql-adapter]

name of repo [ad-app]  e.g [ad-mysql]

name of the app TemplateUser e.g MySql_User

Rename TemplateUser e.g MySql_User

Rename TemplateTarget e.g MySql_Target

Rename TemplateLaunchParams e.g MySql_LaunchParams

Rename BasicConstants e.g MySql_Constants

#File Rename#
Rename files that start with template_ to somthing like mysql_target or mysql_target