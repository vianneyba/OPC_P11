from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def test_index(self):
        self.client.get("/")

    @task
    def test_clubs_list(self):
        self.client.get("/displayBoard")

    @task
    def test_showSummary(self):
        self.client.post("/showSummary", {"email": "vianney@free.fr"})


    @task
    def test_book(self):
        self.client.get('/book/Test%20Competition%20One/vianney%20bailleux')

    @task
    def test_purchase_places(self):
        data = {
            'club': "Raymond Bailleux",
            'competition': "Test Competition One",
            'places': '1'
        }
        self.client.post("/purchasePlaces", data)