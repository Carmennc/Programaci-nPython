
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import plantaItem

# Create your views here.
@api_view(['GET'])
def get_plantas(request):
    Irrigation = request.GET.get("Irrigation",0)
    materas  = list(plantaItem.objects(Irrigation__gte=Irrigation).order_by('-creation_date'))
    materas_seriazable = list(map(lambda f_item: f_item.as_dic(),materas))
    return Response(materas_seriazable, status=200)


@api_view(['POST'])
def post_planta(request):
    body = request.data
    new_planta = plantaItem(
        name = body['name'],
        Irrigation = body['Irrigation'],
        Size = body['Size'],
        Price = body['Price'],
        material = body['material'])
    new_planta.save()    
    return Response(new_planta.as_dic(), status=201)


def get_planta(_,id):
    try:
        planta =  plantaItem.objects.get(id=id)
        return Response(planta.as_dic(), status= 200)
    except plantaItem.DoesNotExist:
        return Response({"message": f"planta {id} not exist"}, status= 404)
    

def delete_planta(_,id):
    try:
        planta =  plantaItem.objects.get(id=id)
        data = planta.as_dic()
        planta.delete()
        return Response(data, status= 200)
    except plantaItem.DoesNotExist:
        return Response({"message": f"planta {id} not exist"}, status= 204)

 
def patch_planta(_, id, body):
    Price = body.get("price")
    name = body.get("name")
    found = plantaItem.objects(id=id).first()
    if found is not None:
        if Price is not None:
            found.Price = Price
        if name is not None:
            found.name = name
        found.save()
        return Response(found.as_dic(), status=200)
    else:
        return Response({"message": "planta with " + id + " not found"}, status=404)

    
@api_view(["GET","DELETE","PATCH"])
def handle_one_planta(request,id):
    if request.method== "GET":
        return get_planta(request,id)
    elif request.method== "PATCH":
        return patch_planta(request,id, request.data)
    else:
        return delete_planta(request,id)
    

@api_view(["GET"])
def v2(_,id):
    planta =  plantaItem.objects.get(id=id)
    data = planta.as_dic()
    data["version"] = "V2"
    return Response(data, status= 200)