from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Building(models.Model):
    name = models.CharField(max_length = 1000)

    def __unicode__(self):
        return self.name

class Floor(models.Model):
    name = models.CharField(max_length = 1000)
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return self.name

class Bin(models.Model):
    building = models.ForeignKey(Building);
    description = models.TextField()
    floor = models.ForeignKey(Floor)
    location = models.CharField(max_length = 1000)

    def __unicode__(self):
        return unicode(self.building) + " " + unicode(self.floor) + " " + self.description

class BinStatus(models.Model):
    theBin = models.ForeignKey(Bin)
    status = models.CharField(max_length = 1000)    # Emptied, full, not_full
    time = models.DateTimeField(auto_now = True)    # timestamp current time
    byUser = models.ForeignKey(User, related_name = 'byUser')

    def __unicode__(self):
        return unicode(self.theBin.building.name + " " + self.theBin.description + " " + self.theBin.floor.name + " " + self.status)

##### OLD

# class Paper(models.Model):
#     by_user = models.ForeignKey(User, related_name = 'by_user')
#     title = models.CharField(max_length = 1000)
#     body = models.TextField()
#     due = models.DateField()
#     time = models.DateTimeField(auto_now = True)

#     def __unicode__(self):
#         return self.title

# class Comments(models.Model):
#     thepaper = models.ForeignKey(Paper)
#     by_user = models.OneToOneField(User)
#     comment = models.TextField()
#     upvotes = models.IntegerField(default = 0)
#     downvotes = models.IntegerField(default = 0)

#     def __unicode__(self):
#         return self.comment

# class PaperForm(ModelForm):
#     class Meta:
#         model = Paper
#         exclude = ['by_user']
