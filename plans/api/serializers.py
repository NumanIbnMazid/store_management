from rest_framework import serializers
from plans.models import Category, Option, Product


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("slug",)

class CategoryUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("slug","category_number", "store",)



class OptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug",)

class OptionUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug","category","option_number",)


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug",)

class ProductUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug","store","space","option", "category","reservation",)