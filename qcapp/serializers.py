from rest_framework import serializers
from django.conf import settings
from datetime import date

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
        # latest_emp = (
        #     emp_allocate.objects
        #     .filter(machine_id=obj.machine.id, date=today)
        #     .order_by('-id')  # higher ID = last allocation
        #     .first()
        # )
        latest_emp = (
            emp_allocate.objects
            .filter(
                machine_id=obj.machine.id,
                date=today,
                unit=obj.unit.id,     # 👈 important
                line=obj.line.id      # 👈 important
            )
            .order_by('-id')
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
            photo_url = f"https://hfapi.herofashion.com/{staff_url}/{filename}"
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




class MachineTrasnsferSerializer(serializers.ModelSerializer):

    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=machine_details.objects.all(),
        source='machine'
    )
    machine = serializers.CharField(source='machine.Identity', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    line_number = serializers.IntegerField(source='line.line_number', read_only=True)

    class Meta:
        model = MachineAllocation
        fields = ['id', 'machine', 'machine_id', 'unit', 'unit_name', 'line', 'line_number', 'allocated_at']

    def validate(self, data):
        unit = data.get('unit', getattr(self.instance, 'unit', None))
        line = data.get('line', getattr(self.instance, 'line', None))
        machine = data.get('machine', getattr(self.instance, 'machine', None))

        # ✅ Line belongs to unit validation
        if line and unit and line.unit != unit:
            raise serializers.ValidationError("Selected line does not belong to the selected unit")

        # ✅ NEW CONDITION: employee allocation check
        today = date.today()

        emp_exists = emp_allocate.objects.filter(
            machine=machine,
            date=today,
            status=True   # status = 1 (allocated)
        ).exists()

        if emp_exists:
            raise serializers.ValidationError(
                "An employee is already assigned today; mark them offline to allow transfer"
            )

        return data