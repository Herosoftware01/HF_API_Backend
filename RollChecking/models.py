from django.db import models

class RollEmployee(models.Model):
    code = models.IntegerField(primary_key=True)
    date = models.CharField(db_column='Date', max_length=4000, blank=True, null=True)
    employee = models.CharField(db_column='Employee', max_length=100, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)
    photo = models.CharField(db_column='photo', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coraemp'


class RollEmpDetails(models.Model):
    sl = models.AutoField(primary_key=True)
    machine_id = models.CharField(max_length=5, db_column='Machine_ID', blank=True, null=True)
    c_code = models.CharField(max_length=10, db_column='Checker_Code', blank=True, null=True)
    c_name = models.CharField(max_length=50, db_column='Checker_Name', blank=True, null=True)
    h_code = models.CharField(max_length=10, db_column='Helper_Code', blank=True, null=True)
    h_name = models.CharField(max_length=50, db_column='Helper_Name', blank=True, null=True)
    date =  models.DateTimeField(auto_now_add = True, db_column = 'CreatedDate')


class RollChecking(models.Model):
    rowno = models.BigIntegerField(db_column='RowNo', primary_key=True)
    dt = models.DateTimeField()
    type = models.CharField(max_length=8, db_column='ty')
    dc = models.CharField(max_length=25, blank=True, null=True)
    rlno = models.CharField(max_length=50, blank=True, null=True)
    colour = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    fab = models.CharField(max_length=35)
    dia = models.CharField(max_length=35)
    weight = models.DecimalField(max_digits=18, decimal_places=3)
    mtr = models.DecimalField(max_digits=18, decimal_places=2)
    lotno = models.CharField(max_length=10, blank=True, null=True)
    jobno = models.CharField(max_length=50)
    gsm = models.IntegerField()
    img = models.CharField(max_length=94, blank=True, null=True, db_column='img1')

    class Meta:
        managed = False
        db_table = 'vue_rl001'


class RollCheckingDetails(models.Model):
    sl = models.AutoField(primary_key=True)
    date =  models.DateTimeField(auto_now_add = True)
    
    empid_checker = models.IntegerField(blank=True, null=True)
    checker_name = models.CharField(max_length=50, blank=True, null=True)
    empid_helper = models.IntegerField(blank=True, null=True)
    helper_name = models.CharField(max_length=50, blank=True, null=True)

    mach_id = models.CharField(max_length=5,blank=True, null=True) 
    rlno = models.CharField(max_length=20)
    jobno = models.CharField(max_length=10, blank=True, null=True)
    colour = models.CharField(max_length=50, blank=True, null=True)
    dcno = models.CharField(max_length=30, blank=True, null=True)
    dia = models.CharField(max_length=10, blank=True, null=True)
    lotno = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    fabric = models.CharField(max_length=50, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    meter = models.CharField(max_length=20, blank=True, null=True)
    gsm = models.CharField(max_length=20, blank=True, null=True)
    a_gsm = models.CharField(max_length=20, blank=True, null=True)
    f_dia = models.CharField(max_length=20, blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    timer = models.CharField(db_column='Timer',max_length=50, blank=True, null=True) 
    image = models.CharField(max_length=100, blank=True, null=True)
    c_img = models.CharField(max_length=100, blank=True, null=True)
    submit = models.BooleanField(default=False)
    submit_date =  models.DateTimeField(blank=True, null=True)    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rlno', 'dcno', 'colour'],
                name='unique_rlno_dcno_colour'
            )
        ]


class RollCheckingDefect(models.Model):
    sl = models.AutoField(primary_key=True)
    rlno = models.CharField(max_length=20)
    colour = models.CharField(max_length=50, blank=True, null=True)
    dcno = models.CharField(max_length=30, blank=True, null=True)
    defectcode = models.CharField(max_length=30)
    defectname = models.CharField(max_length=100)
    subname = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    inches = models.IntegerField(blank=True, null=True)
    holes = models.IntegerField(blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)
    tcounts = models.IntegerField(blank=True, null=True)
    tpoints = models.IntegerField(blank=True, null=True)
    entrytype = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


class MasterMistakes(models.Model):
    choice = (
        ('C','Count'),
        ('M','Meter'),
        ('P','Popup'),
        ('CM','C & M')
    )
    sl = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1)
    dt = models.DateTimeField(auto_now_add=True)
    mist1_eng = models.CharField(max_length=50, blank=True, null=True)
    mist2_eng = models.CharField(max_length=50, blank=True, null=True)
    mist3_eng = models.CharField(max_length=50, blank=True, null=True)
    mist4_eng = models.CharField(max_length=50, blank=True, null=True)
    mist5_eng = models.CharField(max_length=50, blank=True, null=True)
    mist6_eng = models.CharField(max_length=50, blank=True, null=True)
    mist7_eng = models.CharField(max_length=50, blank=True, null=True)
    mist8_eng = models.CharField(max_length=50, blank=True, null=True)
    mist9_eng = models.CharField(max_length=50, blank=True, null=True)
    mist10_eng = models.CharField(max_length=50, blank=True, null=True)
    mist11_eng = models.CharField(max_length=50, blank=True, null=True)
    mist12_eng = models.CharField(max_length=50,blank=True, null=True)
    mist13_eng = models.CharField(max_length=50, blank=True, null=True)

    m1_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m2_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m3_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m4_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m5_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m6_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m7_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m8_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m9_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m10_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m11_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m12_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)
    m13_choice = models.CharField(max_length=2, choices=choice, blank=True, null=True)

    mist1_ta = models.CharField(max_length=50, blank=True, null=True)
    mist2_ta = models.CharField(max_length=50, blank=True, null=True)
    mist3_ta = models.CharField(max_length=50, blank=True, null=True)
    mist4_ta = models.CharField(max_length=50, blank=True, null=True)
    mist5_ta = models.CharField(max_length=50, blank=True, null=True)
    mist6_ta = models.CharField(max_length=50, blank=True, null=True)
    mist7_ta = models.CharField(max_length=50,blank=True, null=True)
    mist8_ta = models.CharField(max_length=50, blank=True, null=True)
    mist9_ta = models.CharField(max_length=50,blank=True, null=True)
    mist10_ta = models.CharField(max_length=50,blank=True, null=True)
    mist11_ta = models.CharField(max_length=50,blank=True, null=True)
    mist12_ta = models.CharField( max_length=50,blank=True, null=True)
    mist13_ta = models.CharField( max_length=50,blank=True, null=True)

    mist1_hin = models.CharField( max_length=50,blank=True, null=True)
    mist2_hin = models.CharField(max_length=50,blank=True, null=True)
    mist3_hin = models.CharField(max_length=50,blank=True, null=True)
    mist4_hin = models.CharField( max_length=50,blank=True, null=True)
    mist5_hin = models.CharField(max_length=50,blank=True, null=True)
    mist6_hin = models.CharField(max_length=50, blank=True, null=True)
    mist7_hin = models.CharField(max_length=50,blank=True, null=True)
    mist8_hin = models.CharField(max_length=50,blank=True, null=True)
    mist9_hin = models.CharField(max_length=50,blank=True, null=True)
    mist10_hin = models.CharField(max_length=50,blank=True, null=True)
    mist11_hin = models.CharField(max_length=50,blank=True, null=True)
    mist12_hin = models.CharField(max_length=50,blank=True, null=True)
    mist13_hin = models.CharField(max_length=50,blank=True, null=True)

    mist1_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist2_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist3_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist4_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist5_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist6_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist7_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist8_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist9_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist10_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist11_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist12_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)
    mist13_img = models.ImageField(upload_to='mistake_images/', blank=True, null=True)

    m1 = models.IntegerField(blank=True, null=True)
    m2 = models.IntegerField(blank=True, null=True)
    m3 = models.IntegerField(blank=True, null=True)
    m4 = models.IntegerField(blank=True, null=True)
    m5 = models.IntegerField(blank=True, null=True)
    m6 = models.IntegerField(blank=True, null=True)
    m7 = models.IntegerField(blank=True, null=True)
    m8 = models.IntegerField(blank=True, null=True)
    m9 = models.IntegerField(blank=True, null=True)
    m10 = models.IntegerField(blank=True, null=True)
    m11 = models.IntegerField(blank=True, null=True)
    m12 = models.IntegerField(blank=True, null=True)
    m13 = models.IntegerField(blank=True, null=True)


class DefectCategory(models.Model):
    categoryid = models.AutoField(primary_key=True)
    category_code = models.CharField(max_length=20, unique=True)
    category_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    log = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.category_name

class DefectMaster(models.Model):
    defectid = models.AutoField(primary_key=True)

    categoryid = models.ForeignKey(
        DefectCategory,
        on_delete=models.PROTECT,
        db_column='categoryid',
        related_name='defects'
    )

    defect_code = models.CharField(max_length=30)
    defectname = models.CharField(max_length=100)
    defectserial = models.CharField(max_length=5, blank=True, null=True)
    defect_subname = models.CharField(max_length=100, blank=True, null=True)
    defect_type = models.CharField(max_length=50, blank=True, null=True)
    topbottom = models.CharField(max_length=20, blank=True, null=True)
    tamil = models.CharField(max_length=200, blank=True, null=True)
    hindi = models.CharField(max_length=200, blank=True, null=True)

    image = models.CharField(max_length=255, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    log = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['defect_code', 'defectserial'],
                name='unique_defect_code_serial'
            )
        ]

    def __str__(self):
        return f"{self.defect_code} - {self.defectname}"            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          