from five import grok
from wcc.remotenews.content.remotenewsfolder import IRemoteNewsFolder
from wcc.remotenews.interfaces import ISynchronizer
from Products.CMFCore.interfaces import ISiteRoot

class Synchronize(grok.View):
    grok.context(IRemoteNewsFolder)
    
    def render(self):
        data = ISynchronizer(self.context).update()
        return u'%s items updated' % (len(data))

class SynchronizeAll(grok.View):
    grok.name('remotenews-mega-update')
    grok.context(ISiteRoot)

    def render(self):
        remotenewsfolders = self.context.portal_catalog(
            portal_type='wcc.remotenews.remotenewsfolder',
            Language='all'
        )

        totalitems = 0
        for brain in remotenewsfolders:
            obj = brain.getObject()
            data = ISynchronizer(obj).update()
            totalitems += len(data)

        return u'%s folders updated. %s items updated' % (
            len(remotenewsfolders), totalitems
        )
