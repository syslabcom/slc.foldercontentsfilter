from plone.app.content.browser.foldercontents import FolderContentsView, FolderContentsTable
from plone.app.content.browser.interfaces import IFolderContentsView
from zope.interface import implements

class FolderContentsFilterView(FolderContentsView):
    """ """
    implements(IFolderContentsView)

    def contents_table(self):
        title = self.request.get('Title', '').strip()
        if title != '':
            title = title + '*'
        path = self.request.get('path', '')
        depth = self.request.get('depth',1)
        if title:
            contentFilter = { 'Title': title
                            , 'path': { 'query': path
                                      , 'depth': depth}
                            }
        else:
            contentFilter = {}
            
        table = FolderContentsTable(self.context, 
                                    self.request, 
                                    contentFilter = contentFilter
                                   )
        return table.render()
    