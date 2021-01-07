import redis
from .models import Product
from django.conf import settings

class Recommander:

    def __init__(self):
        self.r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def create_redis_key(self, product_id):
        key = f"product:{product_id}:purchased_with"
        return key
    
    def create_recommandation(self, product):
        product_ids = [p.id for p in product]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    key = self.create_redis_key(product_id)
                    self.r.zincrby(key, 1, with_id)
        return self


    def suggest_products(self, product, max_result):
        product_ids = [p.id for p in product]
        if len(product_ids) == 1:
            # If want suggestion for only one product then directly get suggestion from redis
            suggestions = self.r.zrange(self.create_redis_key(product_ids[0]), 0, -1, desc=True)[:max_result]
        else:
            # else create a temp key to save aggregate of all product score
            combine_ids = "".join(str(id) for id in product_ids)
            # Get redis key for all products that we want suggestion
            product_keys = [self.create_redis_key(id) for id in product_ids]
            temp_key = f"temp:{combine_ids}"
            # Use zunionstore to aggregate the score of all product to new key
            self.r.zunionstore(temp_key, product_keys)
            # Remove product_if of product for which we are getting recommandation so that they are not recommanded for themself
            self.r.zrem(temp_key, *product_ids)
            # get suggestion id from new key which we created to store using zrange
            suggestions = self.r.zrange(temp_key, 0, -1, desc=True)[:max_result]
            # delete the temp_key because we already got the data 
            self.r.delete(temp_key)
        # convert all id to int bcoz redis return them as str
        suggestions_id = [int(id) for id in suggestions]
        # Get product object for each id in suggestions list
        suggestion_obj = list(Product.objects.filter(id__in=suggestions_id))
        # sort the product objects based on the order we received the id from redis using lambda
        suggestion_obj.sort(key=lambda x: suggestions_id.index(x.id))
        return suggestion_obj

