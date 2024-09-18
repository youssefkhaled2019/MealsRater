from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
#uuid-slug
class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    no_of_ratings=models.IntegerField(default=0)
    avg_rating=models.IntegerField(default=0)

    # def no_of_ratings(self):
    #     ratings = Rating.objects.filter(meal=self)
    #     return len(ratings)
    
    # def avg_rating(self):
    #     # sum of ratings stars  / len of rating hopw many ratings 
    #     sum = 0
    #     ratings = Rating.objects.filter(meal=self) # no of ratings happened to the meal 

    #     for x in ratings:
    #         sum += x.stars

    #     if len(ratings) > 0:
    #         return sum / len(ratings)
    #     else:
    #         return 0 
        
    def __str__(self):
        return self.title
    


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    # def __str__(self):
    #     return self.meal  ???



    class Meta:
        unique_together = (('user', 'meal'),)
        index_together = (('user', 'meal'),)

# pre_save  used before the transaction saves.
# post_save used after the transaction saves.

@receiver(post_save, sender=Rating)
def pre_save_person(sender, instance, **kwargs):

    if not instance.pk:
        print ('INSERT !!!!!!')
        x=instance.meal
        x.no_of_ratings=1
        x.avg_rating=instance.stars
        x.save()
    else:
        print ('UPDATE !!!!!!')
       # print(raw)
        # print(instance.stars)
        ratings=Rating.objects.filter(meal=instance.meal)
        no_of_ratings=len(ratings)
        sum = 0
       
        for x in ratings:
            sum += x.stars
        print(sum)
    
        avg_rating= sum/no_of_ratings if no_of_ratings>0 else 0
        print(no_of_ratings,avg_rating)
        meal=Meal.objects.get(id=instance.meal.pk)
        meal.no_of_ratings=no_of_ratings
        meal.avg_rating=avg_rating
        meal.save()


