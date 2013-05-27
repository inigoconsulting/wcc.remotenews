from collective.grok import gs
from wcc.remotenews import MessageFactory as _

@gs.importstep(
    name=u'wcc.remotenews', 
    title=_('wcc.remotenews import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.remotenews.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
