from django.db import models
from django.db.models.deletion import DO_NOTHING,CASCADE

# Create your models here.

class State(models.Model):
    state = models.CharField(max_length=25,null=False)
    state_abbrev = models.CharField(max_length=2, unique=True, null=False)
    population = models.IntegerField(default=0,null=False)
    death_count = models.IntegerField(default=0)

    class Meta:
        db_table = "pd_state"

    def __str__(self):
        return (self.state)

class Drug(models.Model):
    drug_name = models.CharField(max_length=50, unique=True,null=False)
    is_opioid = models.BooleanField(null=False)

    class Meta:
        db_table = "pd_drug"

    def __str__(self):
        return (self.drug_name)
        
class Prescriber(models.Model):
    npi = models.IntegerField(null=False,primary_key=True)
    first_name = models.CharField(max_length=20,null=False)
    last_name = models.CharField(max_length=20,null=False)
    gender = models.CharField(max_length=1,null=False)
    state = models.ForeignKey('State', to_field="state_abbrev", db_column="state", null=False, on_delete=models.CASCADE)
    credentials = models.CharField(max_length=20)
    specialty = models.CharField(max_length=100,null=False)
    is_opioid_prescriber = models.CharField(max_length=20,null=False)
    total_prescriptions = models.IntegerField(null=False)
    picture_path = models.ImageField(default="{{MEDIA_URL}}/photos/profile_male",upload_to="photos")

    class Meta:
        db_table = "pd_prescriber"

    def __str__(self):
        return(self.last_name + ", " + self.first_name)

class Triple(models.Model):
    npi = models.ForeignKey('Prescriber', to_field="npi", db_column="npi", null=False, on_delete=models.CASCADE)
    drug_id = models.ForeignKey('Drug', to_field="id", db_column="drug_id",null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

    class Meta:
        db_table = "pd_prescriber_drug_triple"

    def __str__(self):
        return(str(self.npi) + ": " + str(self.quantity))