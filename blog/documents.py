from elasticsearch_dsl import Index
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Post, Category

posts = Index('posts')
posts.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
@posts.document
class PostDocument(Document):
    class Django:
        model = Post
        fields = [
            'titre',
            'id',
            'slug',
            'image',
        ]


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'category'
        settings = {
            'number_of_shards':1,
            'number_of_replicas':0,
        }

    class Django:
        model = Category
        fields = [
            'name',
            'slug',
        ]
