from modules import agent
from modules import file_io as io
from modules import detectors

model = agent.train()

blacklist = io.read("blacklist_refined")


whitelist = io.read("whitelist_refined")

blacklist_confirmed = []

max = 500

for i in range(0,max):
    b = blacklist[i].split(',')[1]
    b_analyzed = detectors.domain_analysis(b)
    prediction = model.predict([b_analyzed])

    if(int(prediction) == 1):
        print("b" + str(b))
        blacklist_confirmed.append(b)

#whitelist_confirmed = []
#for i in range(0,max):
    #w = whitelist[i]
    #w_analyzed = detectors.domain_analysis(w)
    #prediction = model.predict([w_analyzed])
    #if(int(prediction) == 0):
        #print("w" + str(w))
        #whitelist_confirmed.append(w)

#io.write(whitelist_confirmed, "whitelist_confirmed")
io.write(blacklist_confirmed, "blacklist_confirmed")