# -*- coding: utf-8 -*-

from db.models import Linepost, Workerpost, Postgmpfile, Workflow
from django.db import transaction

class LinepostModel(object):

    @staticmethod
    def get_linepost(autoid, *args, **kwargs):
        flat = True if len(args) == 1 else False
        if autoid:
            kwargs.update(autoid=autoid)
        if len(args):
            return Linepost.objects.filter(**kwargs).values_list(*args,
                                                                 flat=flat)
        else:
            return Linepost.objects.filter(**kwargs)

    @staticmethod
    def get_worker(plid, seqid, postname, *args, **kwargs):
        flat = True if len(args) == 1 else False
        if plid:
            kwargs.update(plid=plid)
        if seqid:
            kwargs.update(seqid=seqid)
        if postname:
            kwargs.update(postname=postname)
        if len(args):
            return Workerpost.objects.filter(**kwargs).values_list(*args,
                                                                   flat=flat)
        else:
            return Workerpost.objects.filter(**kwargs)

    @staticmethod
    def get_gmpfile(wfid, *args, **kwargs):
        flat = True if len(args) == 1 else False
        if wfid:
            kwargs.update(wfid__in=wfid)
        if len(args):
            return Postgmpfile.objects.filter(**kwargs).values_list(*args,
                                                                    flat=flat)
        else:
            return Postgmpfile.objects.filter(**kwargs)

    @staticmethod
    def get_spareroomlist(plid, seqid, postname):
        kwargs = {'plid': plid, 'seqid': seqid, 'postname': postname}
        return Workflow.objects.filter(**kwargs).values_list('spareroom', flat=True)

    @staticmethod
    def start_linepost(lpid, rname, *args, **kwargs):

            Linepost.objects.filter(autoid=lpid).update(**kwargs)
            lastpost = Linepost.objects.filter(status=2, roomname=rname,starttime__lt=kwargs['starttime']).order_by('-starttime')
            if len(lastpost) > 0:
                return lastpost[0].autoid
            else:
                return 0
    @staticmethod
    def end_linepost(lpid=0, *args, **kwargs):
        return Linepost.objects.filter(autoid=lpid).update(**kwargs)
