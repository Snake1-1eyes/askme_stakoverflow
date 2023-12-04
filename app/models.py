from django.db import models
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.
#User = get_user_model()


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('date').reverse()

    def hot_questions(self):
        return self.alias(c_rating=Count('rating')).filter(c_rating__gt=95).order_by('-c_rating')

    def tag_questions(self, tag_id):
        return self.prefetch_related('tags').filter(tags__id=tag_id)


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    head = models.CharField(max_length=256)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.ManyToManyField('Rating', related_name='questions')
    tags = models.ManyToManyField('Tag', related_name='questions')

    def tags_list(self):
        return self.tags.all()

    def rating_count(self):
        return self.rating.count()

    def answers_count(self):
        return Answer.objects.one_question_answers_count(self.id)

    objects = QuestionManager()


class AnswerManager(models.Manager):
    def one_question_answers_count(self, question_id):
        return self.filter(question=question_id).count()

    def question_answers(self, question_id):
        return self.filter(question=question_id).all()

    def right_question_answers(self, question_id):
        return self.question_answers(question_id).order_by('correctness').reverse()


class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.ManyToManyField('Rating', related_name='answers')
    correctness = models.BooleanField(default=False)

    def rating_count(self):
        return self.rating.count()

    objects = AnswerManager()


class Tag(models.Model):
    tag_name = models.CharField(max_length=256)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/')


class Rating(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
