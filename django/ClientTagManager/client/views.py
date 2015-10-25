from django.shortcuts import render
from django.http import HttpResponse
import argparse
import sys

import httplib2

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools


# Create your views here.
def Teste(request):
    import ipdb; ipdb.set_trace()
    return HttpResponse("Hello, world. You're at the polls index.")


def GetService(api_name, api_version, scope, client_secrets_path):
    """Get a service that communicates to a Google API.

    Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    scope: A list of strings representing the auth scopes to authorize for the
      connection.
    client_secrets_path: string A path to a valid client secrets file.

    Returns:
    A service that is connected to the specified API.
    """
    # Parser command-line arguments.
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native
    # client flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(api_name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def create_tag(name, source, rule):
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')

    return service.accounts().containers().tags().create(
        accountId='121962986', containerId='1525824',
        body={"liveOnly": False, "name": name,
              "parameter": [{"key": "html", "type": "template",
                             "value": source}],
              "type": "html"}).execute()


def delete_tag(tagId):
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().tags().delete(
      accountId='121962986', containerId='1525824', tagId=tagId).execute()


def update_tag(tagId, name, source, rule):
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().tags().update(
      accountId='121962986', containerId='1525824', tagId=tagId,
      body={"name": "Sample Custom HTML", "parameter":
            [{"key": "html", "type": "template",
              "value": "<script>alert('hello world')</script>"}],
            "type": "html"}).execute()


def list_all_tags():
    scope = ['https://www.googleapis.com/auth/tagmanager.readonly']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().tags().list(
      accountId='121962986', containerId='1525824').execute()


def get_tag(tagId):
    scope = ['https://www.googleapis.com/auth/tagmanager.readonly']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().tags().get(
      accountId='121962986', containerId='1525824', tagId=tagId).execute()


def create_trigger():
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().triggers().create(
      accountId='121962986',
      containerId='1525824',
      body={
        'name': 'titlo teste f',
        'type': 'pageview',
        'filter': [{
            'type': 'contains',
            'parameter': [{
                'type': 'template',
                'value': '{{Page Hostname}}',
                'key': 'arg0'
            }, {
                'type': 'template',
                'value': 'hostmaneteste2',
                'key': 'arg1'
            }]
        }]
      }
    ).execute()


def list_all_triggers():
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.readonly']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().triggers().list(
      accountId='121962986',
      containerId='1525824').execute()


def get_container_version(version):
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containerversions']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().versions().get(
      accountId='121962986',
      containerId='1525824',
      containerVersionId=version
    ).execute()


def get_container():
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containerversions']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().get(
      accountId='121962986',
      containerId='1525824',
    ).execute()


def create_version():
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containerversions']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().versions().create(
      accountId='121962986',
      containerId='1525824',
      body={
          'name': 'name',
          'notes': 'note',
          'quickPreview': False
      }
    ).execute()


def publish():
    scope = ['https://www.googleapis.com/auth/tagmanager.publish']
    service = GetService('tagmanager', 'v1', scope, 'client_secrets.json')
    return service.accounts().containers().versions().publish(
      accountId='121962986',
      containerId='1525824',
      containerVersionId='2'
    ).execute()
