# Arquivo: locustfile.py
# Para executar: locust -f locustfile.py --host=https://fakestoreapi.com

from locust import HttpUser, task, between
import random

class ECommerceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_product(self):
        product_id = random.randint(1, 20)
        self.client.get(f"/products/{product_id}", name="/products/[id]")

    @task(1)
    def list_all_products(self):
        self.client.get("/products", name="/products")