from django.contrib import admin
from .models import MasterMistakes
import os


class MasterMistakesAdmin(admin.ModelAdmin):
    list_display = ('sl', 'type', 'dt') 
    
    def save_model(self, request, obj, form, change):
        # Check if the object is being updated (not a new instance)
        if obj.pk:  # This means the object already exists (is being updated)
            old_instance = MasterMistakes.objects.get(pk=obj.pk)
            
            # Check each image field and delete the old image if a new one is uploaded
            for field in ['mist1_img', 'mist2_img', 'mist3_img', 'mist4_img', 'mist5_img', 'mist6_img', 'mist7_img',
                          'mist8_img', 'mist9_img', 'mist10_img', 'mist11_img', 'mist12_img', 'mist13_img']:
                old_image = getattr(old_instance, field)
                new_image = getattr(obj, field)

                # If the image is being updated, delete the old one
                if old_image != new_image and old_image:
                    # Delete old image from storage
                    if os.path.isfile(old_image.path):  # Check if the file exists
                        os.remove(old_image.path)

        # Call the parent save_model method to save the object
        super().save_model(request, obj, form, change)

admin.site.register(MasterMistakes, MasterMistakesAdmin)

