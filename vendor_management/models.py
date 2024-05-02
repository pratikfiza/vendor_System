from django.db import models
from django.db.models import Avg


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    def calculate_performance_metrics(self):
        # Calculate On-Time Delivery Rate
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_delivery_pos = completed_pos.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
        self.on_time_delivery_rate = (on_time_delivery_pos / total_completed_pos) * 100 if total_completed_pos != 0 else 0
        
        # Calculate Quality Rating Average
        self.quality_rating_avg = self.purchaseorder_set.filter(quality_rating__isnull=False).aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0
        
        # Calculate Average Response Time
        response_times = completed_pos.annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date')).aggregate(avg_response_time=Avg('response_time'))
        self.average_response_time = response_times['avg_response_time'].total_seconds() / 60 if response_times['avg_response_time'] else 0
        
        # Calculate Fulfilment Rate
        fulfilled_pos = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__lt=1)
        total_pos = self.purchaseorder_set.count()
        self.fulfillment_rate = (fulfilled_pos.count() / total_pos) * 100 if total_pos != 0 else 0

        self.save()
    
    
    class Meta:
        app_label = 'vendor_management'


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update vendor's performance metrics upon PO save
        if self.vendor:
            self.vendor.calculate_performance_metrics()
    
    class Meta:
        app_label = 'vendor_management'

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    class Meta:
        app_label = 'vendor_management'

