from django.db import models

class ElectricityPricePrediction(models.Model):
    demand = models.FloatField()
    demand_pos_RRP = models.FloatField()
    RRP_positive = models.FloatField()
    demand_neg_RRP = models.FloatField()
    RRP_negative = models.FloatField()
    frac_at_neg_RRP = models.FloatField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    solar_exposure = models.FloatField(null=True, blank=True)
    rainfall = models.FloatField(null=True, blank=True)
    school_day = models.BooleanField()
    holiday = models.BooleanField()
    predicted_price = models.FloatField()

    def __str__(self):
        return f"Prediction: ${self.predicted_price}"
