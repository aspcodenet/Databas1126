from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/flasktest'
db = SQLAlchemy(app)


class Skotare(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Namn = db.Column(db.String(30), unique=False, nullable=False)
    Animals =  db.relationship('Animal', backref='Skotare', lazy=True)


class Animal(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Typ = db.Column(db.String(20), unique=False, nullable=False)
    Namn = db.Column(db.String(30), unique=False, nullable=False)
    Vikt = db.Column(db.Integer, unique=False, nullable=True)
    Skotare_Id=db.Column(db.Integer, db.ForeignKey('skotare.Id'),    nullable=False)



db.create_all()

while True:
    print("11. Skapa skötare")
    print("12. Lista skötare")

    print("1. Skapa djur")
    print("2. Lista alla")
    print("4. Sök")
    print("3. Uppdatera djur")
    sel = input("Val:")
    if sel == "11":
        s = Skotare()
        s.Namn = input("Ange namn:")
        db.session.add(s)
        db.session.commit()        

    if sel == "12":
        for s in Skotare.query.all():
            print(f"{s.Namn}...sköter:")
            for a in s.Animals:
                print(f"       {a.Namn}")

    if sel == "1":
        a = Animal()
        a.Namn = input("Ange namn")
        a.Typ = input("Ange typ")
        a.Vikt = int(input("Ange vikt"))
        for skot in Skotare.query.all():
            print(f"Id:{skot.Id} {skot.Namn}")

        a.Skotare_Id = int(input("Ange ID för djurets skötare:"))
        db.session.add(a)
        db.session.commit()        
    
    if sel == "2":
        for a in Animal.query.all():
            print(f"{a.Typ} {a.Namn}")

    if sel == "4":
        search = input("Sök efter:")
        print("Sökresultat")
        for m in Animal.query.filter(Animal.Namn.contains(search)).all():
            print(f"{m.Id} {m.Namn}")
        print("Slut sök")

    if sel == "3":
        for a in Animal.query.all():
            print(f"{a.Id} {a.Namn}")
        selectedId = int(input("Ange id på djuret du vill uppdatera:"))

        djurAttUppdatera = Animal.query.filter_by(Id=selectedId).first()
        djurAttUppdatera.Namn = input("Ange nytt namn:")
        djurAttUppdatera.Typ = input("Ange ny typ:")
        db.session.commit()
        

