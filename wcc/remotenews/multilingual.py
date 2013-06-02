from plone.multilingualbehavior.utils import LanguageIndependentFieldsManager
from wcc.jsonapi.client import V10APIClient

class RemoteNewsFolderLIFM(LanguageIndependentFieldsManager):
   
    def copy_fields(self, translation):
        super(RemoteNewsFolderLIFM, self).copy_fields(translation)
        activity_uuid = getattr(self.context, 'q_activity', '')
        client = V10APIClient(self.context, self.context.endpoint)
        trans_ids = client.translation(activity_uuid)
        translation.q_activity = trans_ids.get(translation.language,
                                                activity_uuid)
