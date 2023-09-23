from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://dario:dario@cluster0.uzgr8ww.mongodb.net/?retryWrites=true&w=majority")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]


app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        res.message("Ciao, grazie per aver contattato *Vivenda*. Stiamo costruendo una startup che opera nel settore della nutrizione e della vendita di prodotti alimentari. \nScegli tra le seguenti opzioni: "
                    "\n\n*Digita*\n\n 1️⃣ Per conoscere *I Nostri Prodotti* \n 2️⃣ Per sapere *Chi Siamo*\n 3️⃣  Per scoprire *Come Funziona*\n 4️⃣ "
                    "C'è una *Ricetta per te*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Per favore inserisci una risposta valida")
            return str(res)

        if option == 1:
            res.message("Il nostro catalogo offre due prodotti:")

            msg1 = res.message(
                "*Pronto a Tavola* è un servizio di delivery food. Riceverai a casa, in ufficio o in palestra i piatti pensati e cucinati per te")
            msg1.media("http://vivenda.life/wp-content/uploads/2023/09/ProntoATavola_WhatsApp.png")

            msg2 = res.message("*Cuciniamo!* è una Box contenente tutti i prodotti di cui hai bisogno, con ricette gustose da preparare StepbyStep sulla base del tuo Piano Alimentare")
            msg2.media("http://vivenda.life/wp-content/uploads/2023/09/Cuciniamo_WhatsApp.png")


        elif option == 2:
            res.message("*Chi Siamo* \nSiamo Dario, Alessio e Daniele. Abbiamo percorsi diversi.Dario progetta applicazioni, Daniele è un economista esperto di Database, Alessio è un Biologo.")

        elif option == 3:
            res.message("*Come Funziona* \n Inviando il tuo Piano Alimentare il software Vivenda elaborerà una proposta d’acquisto con tutti i prodotti di cui hai bisogno per rispettare la tua dieta e raggiungere i tuoi obiettivi.")

        elif option == 4:
            res.message("*Una Ricetta per te*")
            res.message("Lorem Ipsum")

        else:
            res.message("Per favore inserisci una risposta valida")
            return str(res)

        users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})

    return str(res)

if __name__ == "__main__":
    app.run()
