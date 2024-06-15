import json
import pyaudio
import requests
import vosk
import cv2

counter = 1
model = vosk.Model("vosk-model-small-ru-0.4")
response = requests.get("https://dog.ceo/api/breeds/image/random")
data = json.loads(response.content)

record = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=16000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer["text"]:
                yield answer["text"]


def save_image(counter):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    image_url = response.json()["message"]
    p = requests.get(image_url)
    out = open("img"+str(counter)+".jpg", "wb")
    out.write(p.content)
    out.close()
    print('Сохранено')


def dog_image():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    image_url = response.json()["message"]
    print(image_url)
    p = requests.get(image_url)
    out = open("img.jpg", "wb")
    out.write(p.content)
    out.close()
    print("Ваш собакен")
    img = cv2.imread("img.jpg")
    cv2.imshow("Dog", img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()


def dog_breed():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    breeds = data["message"]
    breeds = breeds.split("/")
    print("Порода собаки:", breeds[-2])


def resolution():
    img = cv2.imread("img.jpg")
    width, height, _ = img.shape
    resolution = str(width) + " x " + str(height)
    print(resolution)


for text in listen():
    if "показать" in text:
        dog_image()
    elif "сохранить" in text:
        save_image(counter)
        counter+=1
    elif "следующая" in text:
        dog_image()
    elif "порода" in text:
        dog_breed()
    elif "разрешения" in text:
        resolution()
    elif "выход" in text:
        break
    else:
        print("Команда не распознана")