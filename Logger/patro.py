
import pyrebase

config = {

  "apiKey": "AIzaSyBWvkqIHpGH3J12WU44OKGWVKsbpdrj1GI",

  "authDomain": "adfrehasdgfh.firebaseapp.com",

  "databaseURL": "https://adfrehasdgfh-default-rtdb.firebaseio.com",

  "storageBucket": "adfrehasdgfh.appspot.com",
}


firebase = pyrebase.initialize_app(config)

#firebase.database().ref().child('lezha').orderByChild('Kerkimi').equalTo(kerkimi)

db = firebase.database()

le = db.child('tirana').order_by_child('kerkimi').equal_to('gerald').get()

print(le)
