# -*- coding: utf-8 -*-

from document.models.documentmodel import DocumentModel


class DocumentController(object):

    def get_document(self, autoid=0, *args, **kwargs):
        return DocumentModel.get_document(autoid, *args, **kwargs)
