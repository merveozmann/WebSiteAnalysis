from tkinter import *
from modules import agent, detectors

model = None
model = agent.train()
agent.save_model(model, "model001")

def ui():
    global window,lbl,txt,btn,lbl2,lbl3
    window.title("Zararlı web sitesi analizi")
    window.geometry("400x200")
    lbl.grid(column=0, row=0)
    txt.grid(column=1, row=0)
    btn.grid(column=2, row=0)
    lbl2.grid(column=0, row=1)
    lbl3.grid(column=0, row=2)
    window.mainloop()
    return 0

def analiz():
    global model
    print("click")

    
    sample = detectors.domain_analysis(txt.get())
    prediction = agent.predict(model,[sample])
    prediction = prediction[0]
    print(prediction)
    if(int(prediction) == 1):
        print("Zararlı")
        lbl2.configure(text= "Tahmin: Zararlı")
    else:
        print("Güvenli")
        lbl2.configure(text= "Tahmin: Güvenli")


window = Tk()
lbl = Label(window, text="Site adresini giriniz:")
txt = Entry(window, width=30)
btn = Button(window, text="Analiz Et", command=analiz)
lbl2 = Label(window, text="")
lbl3 = Label(window, text="")

ui()