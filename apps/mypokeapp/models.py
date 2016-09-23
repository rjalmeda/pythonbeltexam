from __future__ import unicode_literals

from django.db import models
from ..mylogin.models import Users
# Create your models here.

class PokeManager(models.Manager):
    def registerpoke(self, postdata):
        print postdata['pokefrom']
        print postdata['poketo']
        you = Users.objects.get(id=postdata['pokefrom'])
        target = Users.objects.get(id=postdata['poketo'])
        print you
        print target
        instantpoke = Poke.objects.create(FK_poke_from = you, FK_poke_to = target)
        return instantpoke
    
    def pokefromcount(self, userid):
        print userid
        you = Users.objects.get(id=userid)
        count = Poke.objects.filter(FK_poke_to = you).values('FK_poke_from').distinct().count()
        print count
        return count
    
    def pokedfrom(self, userid):
        you = Users.objects.get(id=userid)
        pokersid = Users.objects.filter(poke_user__FK_poke_to = you).values('id').distinct()
        pokersid = list(pokersid)
        print pokersid
        allpokers = []
        for poker in pokersid:
            print poker['id']
            allpokers.append(Users.objects.get(id=poker['id']))
            print allpokers
            print type(allpokers)
        print allpokers
        return allpokers
    
    def pokerscount(self, userid):
        you = Users.objects.get(id=userid)
        pokersid = Users.objects.filter(poke_user__FK_poke_to = you).values('id').distinct()
        pokersid = list(pokersid)
        print pokersid
        allpokerscount = []
        for poker in pokersid:
            print poker['id']
            frompoker = Users.objects.get(id=poker['id'])
            allpokerscount.append(Poke.objects.filter(FK_poke_from = frompoker).filter(FK_poke_to = you).count())
            print allpokerscount
            print type(allpokerscount)
        print allpokerscount
        return allpokerscount

class Poke(models.Model):
    FK_poke_from = models.ForeignKey(Users, related_name='poke_user')
    FK_poke_to = models.ForeignKey(Users, related_name='poke_target')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = PokeManager()