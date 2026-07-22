from django.db import models

# FashionR Master Table
class FashionrResult(models.Model):
    slno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    result = models.JSONField(default=list)
    created_datetime = models.DateTimeField(blank=True, null=True)
    jobno = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Fashionr_result'


# FashionR Cutplan Master Table
class FrCutplanMas(models.Model):
    cutplanid = models.AutoField(db_column='CutPlanId', primary_key=True)
    orderno = models.CharField(db_column='OrderNo', max_length=50, blank=True, null=True)
    customer = models.CharField(db_column='Customer', max_length=100, blank=True, null=True)
    fabrictype = models.CharField(db_column='FabricType', max_length=100, blank=True, null=True)
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)
    date = models.DateField(db_column='Date', blank=True, null=True)
    time = models.TimeField(db_column='Time', blank=True, null=True)
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)
    classification = models.CharField(db_column='Classification', max_length=50, blank=True, null=True)
    
    slno = models.ForeignKey('FashionrResult', models.DO_NOTHING, db_column='slno', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Fr_Cutplan_Mas'

# CutPlan Child Table: SizeAndQuantityList
class FrCutplanSizeandQuantityList(models.Model):
    cutplanid = models.ForeignKey('FrCutplanMas', models.DO_NOTHING, db_column='CutPlanId', primary_key=True)
    sizename = models.CharField(db_column='SizeName', max_length=50, blank=True, null=True) 
    qty = models.IntegerField(db_column='Qty', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'FR_CutPlan_SizeAndQuantityList'


# CutPlan Child Table: TotalMarkerList
class FrCutplanTotalMarkerList(models.Model):
    cutplanid = models.ForeignKey('FrCutplanMas', models.DO_NOTHING, db_column='CutPlanId', primary_key=True)
    orderinformationfabric = models.CharField(db_column='OrderInformationFabric', max_length=100, blank=True, null=True)
    fabricname = models.CharField(db_column='FabricName', max_length=100, blank=True, null=True)
    gsm = models.IntegerField(db_column='Gsm', blank=True, null=True)
    totalnumberofplys = models.IntegerField(db_column='TotalNumberOfPlys', blank=True, null=True)
    totalnumberofpieces = models.IntegerField(db_column='TotalNumberOfPieces', blank=True, null=True)
    totalcuttingperimeter = models.DecimalField(db_column='TotalCuttingPerimeter', max_digits=18, decimal_places=3, blank=True, null=True)
    averageefficiencywithselvage = models.DecimalField(db_column='AverageEfficiencyWithSelvage', max_digits=18, decimal_places=3, blank=True, null=True)
    averageefficiencywithoutselvage = models.DecimalField(db_column='AverageEfficiencyWithoutSelvage', max_digits=18, decimal_places=3, blank=True, null=True)
    numberofmarkers = models.IntegerField(db_column='NumberOfMarkers', blank=True, null=True)
    gap = models.DecimalField(db_column='Gap', max_digits=18, decimal_places=3, blank=True, null=True)
    numberofpanel = models.IntegerField(db_column='NumberOfPanel', blank=True, null=True)
    recommendedspreadinglength = models.IntegerField(db_column='RecommendedSpreadingLength', blank=True, null=True)
    spreadingoption = models.CharField(db_column='SpreadingOption', max_length=50, blank=True, null=True)
    avgproductwtingm = models.DecimalField(db_column='AvgProductWtInGm', max_digits=18, decimal_places=3, blank=True, null=True)
    avgfabricwtconsumptioningm = models.DecimalField(db_column='AvgFabricWtConsumptionInGm', max_digits=18, decimal_places=3, blank=True, null=True)
    avgfabricconsumptioninmetre = models.DecimalField(db_column='AvgFabricConsumptionInMetre', max_digits=18, decimal_places=3, blank=True, null=True)
    totalfabricconsumptioninmetre = models.DecimalField(db_column='TotalFabricConsumptionInMetre', max_digits=18, decimal_places=3, blank=True, null=True)
    totalfabricconsumptioningm = models.DecimalField(db_column='TotalFabricConsumptionInGm', max_digits=18, decimal_places=3, blank=True, null=True)
    selvagewidthincm = models.DecimalField(db_column='SelvageWidthInCM', max_digits=18, decimal_places=3, blank=True, null=True)
    selvagelengthincm = models.DecimalField(db_column='SelvageLengthInCM', max_digits=18, decimal_places=3, blank=True, null=True)
    totalfabricconsumptioninkg = models.DecimalField(db_column='TotalFabricConsumptionInKg', max_digits=18, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FR_CutPlan_TotalMarkerList'


# CutPlan Child Table: TotalMarkerListDet
class FrCutplanTotalmarkerlistdet(models.Model):
    markerid = models.AutoField(db_column='MarkerId', primary_key=True)
    cutplanid = models.ForeignKey('FrCutplanMas', models.DO_NOTHING, db_column='CutPlanId', blank=True, null=True)
    entry = models.CharField(db_column='Entry', max_length=100, blank=True, null=True)
    colorway = models.CharField(db_column='Colorway', max_length=100, blank=True, null=True)
    sizesonmarker = models.CharField(db_column='SizesOnMarker', max_length=100, blank=True, null=True)
    noofpiece = models.IntegerField(db_column='NoOfPiece', blank=True, null=True)
    numberofplys = models.IntegerField(db_column='NumberOfPlys', blank=True, null=True)
    edgetoedgeincm = models.DecimalField(db_column='EdgeToEdgeInCM', max_digits=18, decimal_places=3, blank=True, null=True)
    cuttablewidthincm = models.DecimalField(db_column='CuttableWidthInCM', max_digits=18, decimal_places=3, blank=True, null=True)
    length = models.DecimalField(db_column='Length', max_digits=18, decimal_places=3, blank=True, null=True)
    cuttingperimeter = models.DecimalField(db_column='CuttingPerimeter', max_digits=18, decimal_places=3, blank=True, null=True)
    efficiencywithoutselvage = models.DecimalField(db_column='EfficiencyWithoutSelvage', max_digits=18, decimal_places=3, blank=True, null=True)
    efficiencywithselvage = models.DecimalField(db_column='EfficiencyWithSelvage', max_digits=18, decimal_places=3, blank=True, null=True)
    totalpieces = models.IntegerField(db_column='TotalPieces', blank=True, null=True)
    splicemarker = models.TextField(db_column='SpliceMarker', blank=True, null=True)
    cutpercentage = models.DecimalField(db_column='CutPercentage', max_digits=18, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FR_CutPlan_TotalMarkerListDet'


# CutPlan Child Table: TotalMarkerListImages
class FrCutplanTotalmarkerlistimages(models.Model):
    cutplanid = models.ForeignKey('FrCutplanMas', models.DO_NOTHING, db_column='CutPlanId', primary_key=True)
    markerid = models.ForeignKey('FrCutplanTotalmarkerlistdet', models.DO_NOTHING, db_column='MarkerId', blank=True, null=True)
    markerimage = models.TextField(db_column='MarkerImage', blank=True, null=True)
    fabricwidth = models.DecimalField(db_column='FabricWidth', max_digits=18, decimal_places=3, blank=True, null=True)
    cuttablewidth = models.DecimalField(db_column='CuttableWidth', max_digits=18, decimal_places=3, blank=True, null=True)
    laylength = models.DecimalField(db_column='LayLength', max_digits=18, decimal_places=3, blank=True, null=True)
    averageconsumption = models.DecimalField(db_column='AverageConsumption', max_digits=18, decimal_places=9, blank=True, null=True)
    numberofpieces = models.IntegerField(db_column='NumberOfPieces', blank=True, null=True)
    total = models.IntegerField(db_column='Total', blank=True, null=True)
    placed = models.IntegerField(db_column='Placed', blank=True, null=True)
    averagearea = models.DecimalField(db_column='AverageArea', max_digits=18, decimal_places=3, blank=True, null=True)
    fabricarea = models.DecimalField(db_column='FabricArea', max_digits=18, decimal_places=3, blank=True, null=True)
    patternarea = models.DecimalField(db_column='PatternArea', max_digits=18, decimal_places=3, blank=True, null=True)
    wastage = models.DecimalField(db_column='Wastage', max_digits=18, decimal_places=3, blank=True, null=True)
    warpshrinkage = models.IntegerField(db_column='WarpShrinkage', blank=True, null=True)
    weftshrinkage = models.IntegerField(db_column='WeftShrinkage', blank=True, null=True)
    avgwt = models.DecimalField(db_column='AvgWt', max_digits=18, decimal_places=3, blank=True, null=True)
    selvagelengthincm = models.DecimalField(db_column='SelvageLengthInCM', max_digits=18, decimal_places=3, blank=True, null=True)
    totalweightofmarkers = models.DecimalField(db_column='TotalWeightOfMarkers', max_digits=18, decimal_places=3, blank=True, null=True)
    patternweight = models.DecimalField(db_column='PatternWeight', max_digits=18, decimal_places=3, blank=True, null=True)
    wastageweight = models.DecimalField(db_column='WastageWeight', max_digits=18, decimal_places=3, blank=True, null=True)
    gsm = models.IntegerField(db_column='GSM', blank=True, null=True)
    style = models.CharField(db_column='Style', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FR_CutPlan_TotalMarkerListImages'
