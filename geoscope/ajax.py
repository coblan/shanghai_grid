# encoding:utf-8

from __future__ import unicode_literals
from .models import BlockGroup,BlockPolygon
from helpers.director.model_func.dictfy import to_dict 
from .polygon import poly2dict

def get_global():
    return globals()

def block_group_items(group_pk):
    group = BlockGroup.objects.get(pk=group_pk)
    ls =[]
    for x in group.blocks.all():
        dc={
            'bounding':poly2dict(x.bounding)
        }
        ls.append(to_dict(x,filt_attr=dc))
    return ls
    


def submit_block(blocks):
    for block in blocks:
        blockgroup= BlockGroup.objects.get(pk=block.get('group'))
        # blockpolygon = BlockPolygon.objects.get(pk=block.get('block'))
        blockgroup.dispatched.blocks.append(block.get('block'))
        blockgroup.dispatched.last=block.get('block')
        blockgroup.dispatched.save()
    return {'status':'success'}

