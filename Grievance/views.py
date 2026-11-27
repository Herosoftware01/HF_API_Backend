import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CategoryMaster, SubCategoryMaster


@require_http_methods(["GET", "POST"])
def Category_API(request):

    if request.method == "GET":
        data = list(CategoryMaster.objects.all().values())
        return JsonResponse({"data": data})

    data = json.loads(request.body)

    category = CategoryMaster.objects.create(
        category_name=data.get("category_name"),
        role=data.get("role"),
        active=data.get("active", True)
    )

    return JsonResponse({"message": "Category saved", "id": category.category_id})


@require_http_methods(["PUT", "DELETE"])
def Category_Detail_API(request, pk):

    category = CategoryMaster.objects.get(category_id=pk)

    if request.method == "DELETE":
        category.delete()
        return JsonResponse({"message": "Category deleted"})

    data = json.loads(request.body)

    category.category_name = data.get("category_name", category.category_name)
    category.role = data.get("role", category.role)
    category.active = data.get("active", category.active)
    category.save()

    return JsonResponse({"message": "Category updated"})


@require_http_methods(["GET", "POST"])
def SubCategory_API(request):

    if request.method == "GET":
        data = list(
            SubCategoryMaster.objects.select_related("category").values(
                "subcategory_id",
                "subcategory_name",
                "category_id",
                "category__category_name",
                "active"
            )
        )
        return JsonResponse({"data": data})

    data = json.loads(request.body)

    sub = SubCategoryMaster.objects.create(
        category_id=data.get("category_id"),
        subcategory_name=data.get("subcategory_name"),
        active=data.get("active", True)
    )

    return JsonResponse({"message": "Subcategory saved", "id": sub.subcategory_id})


@require_http_methods(["PUT", "DELETE"])
def SubCategory_Detail_API(request, pk):

    sub = SubCategoryMaster.objects.get(subcategory_id=pk)

    if request.method == "DELETE":
        sub.delete()
        return JsonResponse({"message": "Subcategory deleted"})

    data = json.loads(request.body)

    sub.category_id = data.get("category_id", sub.category_id)
    sub.subcategory_name = data.get("subcategory_name", sub.subcategory_name)
    sub.active = data.get("active", sub.active)
    sub.save()

    return JsonResponse({"message": "Subcategory updated"})