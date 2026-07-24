import json
from django.http import JsonResponse
from ..models import FrCutplanMas, FrCutplanSizeandQuantityList, FrCutplanTotalMarkerList, FrCutplanTotalmarkerlistdet, FrCutplanTotalmarkerlistimages
from .utils import parse_date, parse_time, safe_decimal


def save_cutplan(fashion):
    try:
        # Duplicate Check
        if FrCutplanMas.objects.using("demo1").filter(
            slno=fashion
        ).exists():
            return JsonResponse({
                "success": True,
                "message": "CutPlan Already Saved."
            }, status=201)

        # Result JSON
        result = fashion.result
        if isinstance(result, str):
            result = json.loads(result)

        # Save Master
        master = FrCutplanMas.objects.using("demo1").create(
            slno=fashion,
            orderno=result.get("OrderNo"),
            customer=result.get("Customer"),
            fabrictype=result.get("FabricType"),
            projectname=result.get("ProjectName"),
            classification=result.get("Classification"),
            username=result.get("User"),
            date=parse_date(result.get("Date")),
            time=parse_time(result.get("Time")),
        )

        # Save Size and Quantity List
        size_list = result.get("SizeAndQuantityList", [])
        if len(size_list) >= 2:
            headers = size_list[0]
            values = size_list[1]
            # Skip first column (Sizes / Default)
            for i in range(1, len(headers)):
                FrCutplanSizeandQuantityList.objects.using("demo1").create(
                    cutplanid=master,
                    sizename=headers[i],
                    qty=int(values[i]) if values[i] else 0
                )

        # Save Total Marker List
        total_marker_list = result.get("TotalMarkerList", [])
        for item in total_marker_list:
            item1 = item.get("Item1", {})
            FrCutplanTotalMarkerList.objects.using("demo1").create(
                cutplanid=master,
                orderinformationfabric=item1.get("OrderInformationFabric"),
                fabricname=item1.get("FabricName"),
                gsm=int(item1.get("Gsm") or 0),
                totalnumberofplys=int(item1.get("TotalNumberOfPlys") or 0),
                totalnumberofpieces=int(item1.get("TotalNumberOfPieces") or 0),
                totalcuttingperimeter=safe_decimal(item1.get("TotalCuttingPerimeter")),
                averageefficiencywithselvage=safe_decimal(item1.get("AverageEfficiencyWithSelvage")),
                averageefficiencywithoutselvage=safe_decimal(item1.get("AverageEfficiencyWithoutSelvage")),
                numberofmarkers=int(item1.get("NumberOfMarkers") or 0),
                gap=safe_decimal(item1.get("Gap")),
                numberofpanel=int(item1.get("NumberOfPanel") or 0),
                recommendedspreadinglength=int(item1.get("RecommendedSpreadingLength") or 0),
                spreadingoption=item1.get("SpreadingOption"),
                avgproductwtingm=safe_decimal(item1.get("AvgProductWtInGm")),
                avgfabricwtconsumptioningm=safe_decimal(item1.get("AvgFabricWtConsumptionInGm")),
                avgfabricconsumptioninmetre=safe_decimal(item1.get("AvgFabricConsumptionInMetre")),
                totalfabricconsumptioninmetre=safe_decimal(item1.get("TotalFabricConsumptionInMetre")),
                totalfabricconsumptioningm=safe_decimal(item1.get("TotalFabricConsumptionInGm")),
                selvagewidthincm=safe_decimal(item1.get("SelvageWidthInCM")),
                selvagelengthincm=safe_decimal(item1.get("SelvageLengthInCM")),
                totalfabricconsumptioninkg=safe_decimal(item1.get("TotalFabricConsumptionInKg")),
            )

            marker_details = []
            for detail in item.get("Item2", []):
                marker = FrCutplanTotalmarkerlistdet.objects.using("demo1").create(
                    cutplanid=master,
                    entry=detail.get("Entry"),
                    colorway=detail.get("Colorway"),
                    sizesonmarker=detail.get("SizesOnMarker"),
                    noofpiece=int(detail.get("NoOfPiece") or 0),
                    numberofplys=int(detail.get("NumberOfPlys") or 0),
                    edgetoedgeincm=safe_decimal(detail.get("EdgeToEdgeInCM")),
                    cuttablewidthincm=safe_decimal(detail.get("CuttableWidthInCM")),
                    length=safe_decimal(detail.get("Length")),
                    cuttingperimeter=safe_decimal(detail.get("CuttingPerimeter")),
                    efficiencywithoutselvage=safe_decimal(detail.get("EfficiencyWithoutSelvage")),
                    efficiencywithselvage=safe_decimal(detail.get("EfficiencyWithSelvage")),
                    totalpieces=int(detail.get("TotalPieces") or 0),
                    splicemarker=detail.get("SpliceMarker"),
                    cutpercentage=safe_decimal(detail.get("CutPercentage"))
                )

                marker_details.append(marker)

        images = result.get("MarkerImagesWithAdditionalInfoList", [])
        for i, image in enumerate(images):
            if i >= len(marker_details):
                break

            FrCutplanTotalmarkerlistimages.objects.using("demo1").create(
                cutplanid=master,
                markerid=marker_details[i],
                markerimage=image.get("MarkerImage"),
                fabricwidth=safe_decimal(image.get("FabricWidth")),
                cuttablewidth=safe_decimal(image.get("CuttableWidth")),
                laylength=safe_decimal(image.get("LayLength")),
                averageconsumption=safe_decimal(image.get("AverageConsumption")),
                numberofpieces=int(image.get("NumberOfPieces") or 0),
                total=int(image.get("Total") or 0),
                placed=int(image.get("Placed") or 0),
                averagearea=safe_decimal(image.get("AverageArea")),
                fabricarea=safe_decimal(image.get("FabricArea")),
                patternarea=safe_decimal(image.get("PatternArea")),
                wastage=safe_decimal(image.get("Wastage")),
                warpshrinkage=int(image.get("WarpShrinkage") or 0),
                weftshrinkage=int(image.get("WeftShrinkage") or 0),
                avgwt=safe_decimal(image.get("AvgWt")),
                selvagelengthincm=safe_decimal(image.get("SelvageLengthInCM")),
                totalweightofmarkers=safe_decimal(image.get("TotalWeightOfMarkers")),
                patternweight=safe_decimal(image.get("PatternWeight")),
                wastageweight=safe_decimal(image.get("WastageWeight")),
                gsm=int(image.get("GSM") or 0),
                style=image.get("Style"),
            )

        return JsonResponse({
            "success": True,
            "message": "CutPlan Saved Successfully.",
            "cutplanid": master.cutplanid,
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e) }, status=400 )
    
