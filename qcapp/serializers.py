from rest_framework import serializers
from django.conf import settings

from .models import QcAdminMistake,Unit, Line, MachineAllocation, machine_details, emp_allocate,Empwisesal,VueProcessSequence


class QcAdminMistakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QcAdminMistake
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = machine_details
        fields = ['id', 'Identity', 'Item', 'Description']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


from django.utils import timezone


class MachineAllocationSerializer(serializers.ModelSerializer):
    # Accept machine ID on write
    machine_id = serializers.PrimaryKeyRelatedField(queryset=machine_details.objects.all(), write_only=True)

    # Show machine details on read
    machine = MachineSerializer(read_only=True)

    employees = serializers.SerializerMethodField()

    class Meta:
        model = MachineAllocation
        fields = ['id', 'machine', 'machine_id', 'unit', 'line', 'allocated_at', 'employees']  # ✅ include machine_id

    def validate(self, data):
        if data.get('line') and data.get('unit') and data['line'].unit != data['unit']:
            raise serializers.ValidationError("Selected line does not belong to the selected unit")
        return data

    def create(self, validated_data):
        machine = validated_data.pop('machine_id')
        allocation = MachineAllocation.objects.create(machine=machine, **validated_data)
        return allocation

    def get_employees(self, obj):
        today = timezone.now().date()

        # Get the latest allocation for today
        latest_emp = (
            emp_allocate.objects
            .filter(machine_id=obj.machine.id, date=today)
            .order_by('-id')  # higher ID = last allocation
            .first()
        )

        if not latest_emp:
            return []
        
        # Get employee details from Empwisesal table
        emp_details = Empwisesal.objects.using('main').filter(code=latest_emp.emp_code).first()
        
        if emp_details and emp_details.photo:
            filename = emp_details.photo.split('\\')[-1]
            # Ensure no double slashes
            staff_url = settings.STAFF_IMAGES_URL.rstrip('/')
            photo_url = f"http://127.0.0.1:8000/{staff_url}/{filename}"
        else:
            # Default profile picture if none exists
            photo_url = "https://www.example.com/default-profile.png"

        return [
            {
                "emp_code": latest_emp.emp_code,
                "status": latest_emp.status,
                "photo":photo_url
            }
        ]
    

class EmpAllocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = emp_allocate
        fields = ["emp_code"]



class VueProcessSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VueProcessSequence
        fields = ['process_des', 'sl', 'prsid']

