from five import grok
from plone.directives import dexterity, form
from wcc.remotenews.content.remotenewsfolder import IRemoteNewsFolder

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IRemoteNewsFolder)
    grok.require('zope2.View')
    grok.template('remotenewsfolder_view')
    grok.name('view')

