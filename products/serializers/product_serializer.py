from rest_framework import serializers

from products.models.attribute import Attribute
from products.models.brand import Brand
from products.models.category import Category
from products.models.product import Product
from products.models.type import Type


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


#  Brend serializeri
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


#  Turi serializeri
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


# Atribut serializeri
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"


#  Asosiy mahsulot serializeri
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())
    attributes = serializers.PrimaryKeyRelatedField(
        queryset=Attribute.objects.all(), many=True
    )

    category_detail = CategorySerializer(source="category", read_only=True)
    brand_detail = BrandSerializer(source="brand", read_only=True)
    type_detail = TypeSerializer(source="type", read_only=True)
    attributes_detail = AttributeSerializer(
        source="attributes", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
