from runProg import RunProg


tache = RunProg("config.txt")

cmd = ""

while cmd != "quit":

    cmd = input(">")

    if cmd == "status":
        print("status : ",tache.status())

    elif cmd == "run":
        tache.run()
        print("status : ",tache.status())

    elif cmd == "reset":
        tache.reset()
        print("status : ",tache.status())

    elif cmd == "view":
        print("Liste des fichiers :", tache.view())#file list

    elif cmd == "read":# File content
        print("Contenu du fichier :", tache.read(input("fichier a afficher:")))# File to display

    else:
        print("status : ",tache.status())
