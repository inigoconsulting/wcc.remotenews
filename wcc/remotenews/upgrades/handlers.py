from collective.grok import gs
from Products.CMFCore.utils import getToolByName

# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.remotenews to 1001',
                description=u'Upgrade wcc.remotenews to 1001',
                source='1000', destination='1001',
                sortkey=1, profile='wcc.remotenews:default')
def to1001(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.remotenews.upgrades:to1001')
