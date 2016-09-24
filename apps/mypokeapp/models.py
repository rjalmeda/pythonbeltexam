from __future__ import unicode_literals

from django.db import models
from ..mylogin.models import Users
# Create your models here.

class PokeManager(models.Manager):
    def registerpoke(self, postdata):
        you = Users.objects.get(id=postdata['pokefrom'])
        target = Users.objects.get(id=postdata['poketo'])
        instantpoke = Poke.objects.create(FK_poke_from = you, FK_poke_to = target)
        return instantpoke
    
    def pokefromcount(self, userid):
        you = Users.objects.get(id=userid)
        count = Poke.objects.filter(FK_poke_to = you).exclude(FK_poke_from = you).values('FK_poke_from').distinct().count()
        return count
    
    def pokedfrom(self, userid):
        you = Users.objects.get(id = userid)
        pokersid = Users.objects.filter(poke_user__FK_poke_to = you).exclude(id=userid).values('id').distinct()
        pokersid = list(pokersid)
        allpokers = []
        for poker in pokersid:
            allpokers.append(Users.objects.get(id=poker['id']))
        return allpokers
    
    def pokerscount(self, userid):
        you = Users.objects.get(id = userid)
        pokersid = Users.objects.filter(poke_user__FK_poke_to = you).exclude(id=userid).values('id').distinct()
        pokersid = list(pokersid)
        allpokerscount = []
        for poker in pokersid:
            frompoker = Users.objects.get(id=poker['id'])
            allpokerscount.append(Poke.objects.filter(FK_poke_from = frompoker).filter(FK_poke_to = you).exclude(FK_poke_from=you).count())
        return allpokerscount

class Poke(models.Model):
    FK_poke_from = models.ForeignKey(Users, related_name='poke_user')
    FK_poke_to = models.ForeignKey(Users, related_name='poke_target')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = PokeManager()