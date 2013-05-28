from wcc.remotenews.interfaces import ISynchronizer
from wcc.remotenews.content.remotenewsfolder import IRemoteNewsFolder
from Products.CMFPlone.utils import _createObjectByType
import requests
import hashlib
import time
from five import grok
from wcc.remoteuuid.interfaces import IMutableRemoteUUID
from zope.event import notify
from zope.lifecycleevent import (
    ObjectCreatedEvent, ObjectModifiedEvent,
    ObjectAddedEvent, ObjectMovedEvent
)
import transaction
from zope.container.interfaces import INameChooser
from dateutil.parser import parse as parse_date
from DateTime import DateTime
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from wcc.jsonapi.interfaces import ISignatureService

class Synchronizer(grok.Adapter):
    grok.implements(ISynchronizer)
    grok.context(IRemoteNewsFolder)

    def __init__(self, context):
        self.context = context

    def update(self):
        items = []
        for item in self._fetch():
            r = self._update(item)
            if r:
                items.append(r)
        return items

    def _fetch(self):
        endpoint = self.context.endpoint
        if endpoint.endswith('/'):
            api_url = endpoint[:-1]
        api_url = '%s/1.0/news' % (api_url)
        ss = ISignatureService(self.context)
        params = ss.sign_params(api_url, {'language':self.context.language})
        print api_url, str(params)
        resp = requests.get(api_url, params=params)
        return resp.json

    def _update(self, data):
        obj = self._constructItem(data)

        # skip if modificationdate is the same
        modification_date = DateTime(parse_date(data['modified']))
        if obj.getField('modification_date').get(obj) == modification_date:
            return

        obj.setTitle(data['title'])
        obj.setDescription(data['description'])
        obj.getField('text').set(obj, data['text'])
        
        effective_date = DateTime(parse_date(data['date']))
        obj.getField('effectiveDate').set(obj, effective_date)

        image_url = data['images'].get('large', None)
        self._set_image(obj, image_url)

        obj.getField('imageCaption').set(obj, data['image_caption'])

        if data['state'] == 'published':
            wftool = getToolByName(obj, 'portal_workflow')
            try:
                wftool.doActionFor(obj, "publish")
            except WorkflowException:
                pass

        notify(ObjectModifiedEvent(obj))

        modification_date = DateTime(parse_date(data['modified']))
        obj.getField('modification_date').set(obj, modification_date)

        od = obj.__dict__
        od['notifyModified'] = lambda *args: None
        obj.reindexObject()
        del od['notifyModified']
        return obj

    def _set_image(self, obj, image_url):
        if not image_url:
            return

        try:
            image = requests.get(image_url).content
        except:
            return
        
        if not image:
            return

        obj.getField('image').set(obj, image)


    def _constructItem(self, data):
        uuid = data['uuid']
        brains = self.context.portal_catalog(remoteUUID=uuid)
        if brains:
            return brains[0].getObject()
        
        tempid = str(time.time())
        item = _createObjectByType('wcc.remotenews.remotenewsitem',
                self.context, tempid)
        notify(ObjectCreatedEvent(item))
        notify(ObjectAddedEvent(item))
        transaction.savepoint(optimistic=True)
        oid = INameChooser(self.context).chooseName(data['title'], item)
        item.unindexObject()
        item._setId(oid)
        self.context._delObject(tempid, suppress_events=True)
        self.context._setObject(oid, item, set_owner=0, suppress_events=True)
        mutableuuid = IMutableRemoteUUID(item)
        mutableuuid.set(data['uuid'])
        notify(ObjectMovedEvent(item, oldParent=self.context, oldName=tempid,
            newParent=self.context, newName=oid))
        return item
