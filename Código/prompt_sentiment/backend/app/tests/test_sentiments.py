import json
import pytest
from datetime import datetime

def test_add_sentiment(test_app, test_database, add_dataset, add_user, add_review):
    user1 = add_user("justatest1234", "test_sentiment1@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config1", owner = user1.id)
    review1 = add_review(dataset_id = dataset1.id,  
                        review_text="review_text",
                        review_time = datetime.now().isoformat(),
                        original_stars=0)
    
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        
        data=json.dumps(
            {
                "review_id": review1.id,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "process_time": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    data1 = json.loads(resp.data.decode())
    assert resp.status_code == 201
    print(data1)
    assert "Se ha añadido el sentimiento para la reseña 1." in data1["message"]

def test_add_sentiment_duplicado(test_app, test_database, add_dataset, add_user, add_review):
    user1 = add_user("justatest1234", "test_sentiment21@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config2", owner = user1.id)
    review1 = add_review(dataset_id = dataset1.id,  
                        review_text="review_text",
                        review_time = datetime.now().isoformat(),
                        original_stars=0)
    
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "review_id": 2,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "process_time": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "review_id": 2,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "process_time": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    data1 = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "El sentimiento ya existe." in data1["message"]

def test_add_sentiment_faltan_datos(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "review_id": "review1",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_add_sentiment_correcto(test_app, test_database, add_dataset, add_user, add_review):
    user1 = add_user("justatest1234", "test_sentiment3@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config2", owner = user1.id)
    review1 = add_review(dataset_id = dataset1.id,  
                        review_text="review_text",
                        review_time = datetime.now().isoformat(),
                        original_stars=0)
    
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "review_id": review1.id,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "process_time": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el sentimiento para la reseña " + str(review1.id) in data["message"]
    
    
def test_get_sentiment_no_existe(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/sentiments/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El sentimiento 9990000 no existe" in data["message"]


def test_delete_sentiment(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/sentiments/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "El sentimiento 1 se ha borrado." in data["message"]

def test_delete_sentiment_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/sentiments/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El sentimiento 9990000 no existe" in data["message"]

def test_update_sentiment_correct(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(f"/sentiments/2", data=json.dumps({
                "correct": False,
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Sentimiento 2 actualizado' in data["message"]

@pytest.mark.parametrize(
    "id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [
            9990000,
            {
                "correct": False
            },
            404,
            "El sentimiento 9990000 no existe",
        ],
    ],
)

def test_update_sentiment_incorrect_request(test_app, test_database, id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/sentiments/{id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
