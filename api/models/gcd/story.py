from django.db import models
from decimal import Decimal
from api.models.gcd.issue import GCDIssue
from api.models.gcd.storytype import GCDStoryType


class GCDStory(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('sequence_number',)
        db_table = 'gcd_stories'
    
    story_id = models.AutoField(primary_key=True)
    
    # Core story fields.
    title = models.CharField(max_length=255)
    title_inferred = models.BooleanField(default=False, db_index=True)
    feature = models.CharField(max_length=255)
    type = models.ForeignKey(GCDStoryType)
    sequence_number = models.IntegerField()
    
    page_count = models.DecimalField(
        max_digits=10, decimal_places=3,
        null=True, db_index=True
    )
    page_count_uncertain = models.BooleanField(default=False, db_index=True)
                                     
    script = models.TextField()
    pencils = models.TextField()
    inks = models.TextField()
    colors = models.TextField()
    letters = models.TextField()
    editing = models.TextField()
                                     
    no_script = models.BooleanField(default=False, db_index=True)
    no_pencils = models.BooleanField(default=False, db_index=True)
    no_inks = models.BooleanField(default=False, db_index=True)
    no_colors = models.BooleanField(default=False, db_index=True)
    no_letters = models.BooleanField(default=False, db_index=True)
    no_editing = models.BooleanField(default=False, db_index=True)
                                     
    job_number = models.CharField(max_length=25)
    genre = models.CharField(max_length=255)
    characters = models.TextField()
    synopsis = models.TextField()
    reprint_notes = models.TextField()
    notes = models.TextField()
    keywords = models.TextField(null=True)
        
    # Fields from issue.
    issue = models.ForeignKey(GCDIssue)
                                     
    # Fields related to change management.
    reserved = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)
                                     
    deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return '#'+str(self.story_id)+' '+self.title
