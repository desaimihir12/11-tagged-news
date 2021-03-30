from django.db import models
from django.db.models.signals import pre_save, post_delete, post_save
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver

# Create your models here.
def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id),
        title = str(instance.title),
        filename = filename
    )
    return file_path

class BlogPost(models.Model):
    title               = models.CharField(max_length=50, null=False, blank=False) 
    body                = models.TextField(max_length=5000, null=False, blank=False)
    image               = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name="date_publishd")
    date_updated        = models.DateTimeField(auto_now=True, verbose_name="date_updated")
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                = models.SlugField(blank=True, unique=True)
    upvote              = models.IntegerField(default=0)
    downvote            = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    body                = models.TextField(max_length=5000, null=False, blank=False)
    blog                = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name="date_publishd")
    date_updated        = models.DateTimeField(auto_now=True, verbose_name="date_updated")
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upvote              = models.IntegerField(default=0)
    downvote            = models.IntegerField(default=0)

    def __str__(self):
        return self.body

class PostVote(models.Model):
    TYPE                =   (
                                ('U', 'UpVote'),
                                ('D', 'DownVote')
                            )
    parent_post         = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type           = models.CharField(max_length=1, choices=TYPE)

    def __str__(self):
        return str(self.id) + " - " + self.author.username

class CommentVote(models.Model):
    TYPE                =   (
                                ('U', 'UpVote'),
                                ('D', 'DownVote')
                            )
    parent_comment      = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type           = models.CharField(max_length=1, choices=TYPE)
    
    def __str__(self):
        return str(self.id) + " - " + self.author.username

        
# if post is deleted also delete the image associatd to that post
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=PostVote)
def remove_post_vote(sender, instance, **kwargs):
    if(instance.vote_type == 'U'):
        instance.parent_post.upvote -= 1
    else:
        instance.parent_post.downvote -= 1
    print(instance.parent_post.upvote)
    print(instance.parent_post.downvote)
    instance.parent_post.save()

@receiver(post_delete, sender=CommentVote)
def remove_post_comment(sender, instance, **kwargs):
    if(instance.vote_type == 'U'):
        instance.parent_comment.upvote -= 1
    else:
        instance.parent_comment.downvote -= 1
    print(instance.parent_comment.upvote)
    print(instance.parent_comment.downvote)
    instance.parent_comment.save()


def pre_save_blog_post_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

def pre_add_post_vote(sender, instance, **kwargs):
    if(instance.vote_type == 'U'):
        instance.parent_post.upvote += 1
    else:
        instance.parent_post.downvote += 1
    print(instance.parent_post.upvote)
    print(instance.parent_post.downvote)
    instance.parent_post.save()

def pre_add_comment_vote(sender, instance, **kwargs):
    if(instance.vote_type == 'U'):
        instance.parent_comment.upvote += 1
    else:
        instance.parent_comment.downvote += 1
    print(instance.parent_comment.upvote)
    print(instance.parent_comment.downvote)
    instance.parent_comment.save()

# When Blogpose to be saved in the database call the function
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
pre_save.connect(pre_add_post_vote, sender=PostVote)
pre_save.connect(pre_add_comment_vote, sender=CommentVote)
