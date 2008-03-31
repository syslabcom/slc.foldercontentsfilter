from plone.app.content.browser.foldercontents import FolderContentsView

class FolderContentsFilterView(FolderContentsView):
    """ """
    def contents_table(self):
        import pdb;pdb.set_trace()
        table = FolderContentsTable(self.context, 
                        self.request, 
                        contentFilter = {  'Title': self.request.Title
                                            , 'path': { 'query':self.request.path
                                                      , 'depth': self.request.get('depth',1)}
                              
                                        }
                                    )
        return table.render()
    