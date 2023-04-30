from subprocess import *
import os

class RunProg:
    def __init__(self, paramsFile):
        # The constructor takes as parameter a configuration file
        # indicating the parameters for the execution of the Seqgen program.
        self.__paramsFile = paramsFile
        self.__list_params = self.paramsFileTolist()
        self.__cmd = self.cmd_line()
        self.__p = None

    def paramsFileTolist(self):
        #copy the parameters file provided to the constructor into a list and return the list
        list_params = []
        try:
            with open(self.__paramsFile, "r+") as params:
                list_params = params.read().strip().splitlines()
        except Exception as e:
            print(e)
        list_params = list(filter(None, list_params))
        return list_params

    def cmd_line(self):
        # constructs the command line from the list_params and returns it
        (options, infile, outfile) = ('', '', 'output.txt')  # if the outfile=output.txt does not exist in
                                                             # the paramsFile it will be added to the cmd.
        if (len(self.__list_params)) != 0:
            for param in (self.__list_params):
                if 'infile' in param:
                    infile = param.split('=')[1]
                elif 'outfile' in param:
                    outfile = param.split('=')[1]
                elif '=' in param:
                    options = options + '-' + param.split('=')[0] + param.split('=')[1] + ' '
                else:
                    options = options + '-' + param + ' '
            cmd = './seq-gen ' + options + '<' + infile + '> ' + outfile
        else:
            cmd = ''
        return cmd

    def run(self):
        # Starts the execution of Seqgen with the parameters provided to the constructor and returns the Popen -> p process.
        self.removeFiles()
        try:
            with open("stdout.txt", "w") as out, open("stderr.txt", "w") as err:
                p = Popen(self.__cmd, shell=True, stdout=out, stderr=err)
        except Exception as e:
            print("une erreur s'est produite : " + str(e))
        self.__p = p

    def view(self):
        # returns a list of generated files if they exist
        outfile = 'output.txt'
        files_list=[]
        if (len(self.__list_params)) != 0:  # to look up the name of the outfile in case
                                                # it is different from 'output.txt
            for param in (self.__list_params):
                if 'outfile' in param:
                    outfile = param.split('=')[1]
                    print(outfile)
        if os.path.exists(outfile):         # The os.path.exists(outfile) can return false if the process is still
                                          # running (p.poll() = None) even though the file already exists
            files_list.append(outfile)
        if os.path.exists("stdout.txt"):    # in the run() function the "stdout.txt" files
                                             # and "stderr.txt" are always generated
            files_list.append("stdout.txt")
        if os.path.exists("stderr.txt"):
            files_list.append("stderr.txt")

        return files_list

    def removeFiles(self):
        #deletes files that are blocked at runtime
        for file in self.view():
            if os.path.exists(file):
                os.remove(file)

    def reset(self):
        #Allows you to interrupt the execution and erase all traces of it.
        if self.__p is not None:
            self.__p.kill()
            self.__p.communicate()
            self.removeFiles()
        else:
            print("il n'y a pas de processus a interrompre")

    def read(self, fichier):
        # returns the content of the file (if it exists).
        if os.path.exists(fichier):
            with open(fichier, 'r') as f:
                f.content = f.read()
            return f.content
        else:
            return "Le fichier n'existe pas"

    def status(self):
        # returns the execution status:
        # (0) not started / (1) in progress / (2) successfully completed / (3) completed with a failure
        if self.__p == None:
            statut = 0
        else:
            #self.__p.communicate()             #<- solves several problems but blocks the process until the end
            #if self.__p.poll() == None:         # -> p.poll() to see if the process is running, can act as a
                                                 # unexpectedly
                                                # always remains = None because the process is categorized by file.
                                                # this error has been raised several times stackoverflow.com and
                                                # on https://bugs.python.org/issue1336.
                                                # can be fixed if you use self.__p.communicate() but it will block the
                                                # the process until the end of the task
            if self.__p.returncode == None:  #<- same thing happens with p.returncode
                                             # I hope it will work on your computer ;)

                statut = '1'
            elif self.__p.returncode == 0:     # -> p.process is finished with success
                statut = '2'
            elif self.__p.returncode != 0:  # -> p.process is terminated with failure
                statut = '3'
        return statut

    def options_list(self):
        # function to extract the options provided in the paramsFile
        list_params = self.paramsFileTolist()
        optionsList = []
        for param in list_params:
            if '=' in param:
                optionsList.append(param.split('=')[0])
            else:
                optionsList.append(param)
        return optionsList

    def optionsValid(self):
        # 1st validation step :
        # returns False if one of the options provided in the configuration file is not valid
        # according to the seq-gen documentation only the options ['m', 'l', 'n', 'p', 's', 'd', 'c', 'a', 'g', 'i', 'f',
        # fe', 't', 'r', 'kz', 'op', 'or', 'on', 'x', 'wa', 'wr', 'q', 'h'] are valided

        optionsList = self.options_list()
        if 'infile' not in optionsList:
            return False
            print('le parametre infile est obligatoire pour executer seq-gen')
        if 'm' not in optionsList:
            return False
            print('le parametre m <MODELE> est obligatoire pour executer seq-gen')
        for option in optionsList:
            if option not in ['infile', 'outfile', 'm', 'l', 'n', 'p', 's', 'd', 'c', 'a', 'g', 'i', 'f', 'fe', 't',
                              'r', 'kz', 'op', 'or', 'on', 'x', 'wa', 'wr', 'q', 'h']:
                print("l'option", option, "n'est pas valise")
                return False
            else:
                estValide = True
        return estValide

    def parametresValides(self):
        # after the validation of the options this function validates the parameters associated to some options
        # returns False if there is at least one bad parameter in the configuration file.
        if self.optionsValid(): # If optionsValid(parmsFile) is True
            for param in self.__list_params:
                if '=' in param:
                    # validation of mandatory parameters
                    if param.split('=')[0] == 'infile':
                        if os.path.exists(param.split('=')[1]):
                            estValide = True
                        else:
                            return False

                    elif param.split('=')[0] == 'm':  # validate the <MODEL>
                        if param.split('=')[1] in ['HKY', 'F84', 'GTR', 'JTT', 'WAG', 'PAM', 'BLOSUM', 'MTREV', 'CPREV',
                                                   'GENERAL', 'REV', 'CPREV45', 'MTART', 'LG']:
                            estValide = True
                        else:
                            print(param.split('=')[1], "n'est pas un <MODEL> valide")
                            return False
                    # validation of other options in the list
                    elif param.split('=')[0] == 'z':  # validate the parameter is an int()
                        try:
                            int(param.split('=')[1])
                            estValide = True
                        except ValueError:
                            print(param.split('=')[1], "n'est pas un parametre valide pour l'option ", param.split('=')[0])
                            return False
                    elif param.split('=')[0] in ['l', 'k', 'n', 'p']:  # validate parameters int()>0
                        try:
                            int(param.split('=')[1])
                            if (int(param.split('=')[1])) > 0:
                                estValide = True
                            else:
                                print(param.split('=')[1], "n'est pas un parametre valide pour l'option ", param.split('=')[0])
                                return False
                        except ValueError:
                            print(param.split('=')[1], "n'est pas un parametre valide pour l'option ", param.split('=')[0])
                            return False
                    elif param.split('=')[0] == 'g': # g <NUM_CATEGORIES> must be between 2 and 32
                        try:
                            int(param.split('=')[1])
                            if 32 > int(param.split('=')[1]) and int(param.split('=')[1]) > 2:
                                estValide = True
                            else:
                                print(param.split('=')[1], "n'est pas un parametre valide pour l'option ", param.split('=')[0])
                                return False
                        except ValueError:
                            print(param.split('=')[1], "n'est pas un parametre valide pour l'option ", param.split('=')[0])
                            return False
                    elif param.split('=')[0] in ['s', 'd', 't', 'c', 'a', 'i']:
                    # validate the parameters with a name with comma (decimal or real)
                        try:
                            float(param.split('=')[1])
                            estValide = True
                        except ValueError:
                            print(param.split('=')[1], "n'est pas un parametre valide pour l'option ", param.split('=')[0])
                            return False
                    # else: # validation of parameters associated with options ['f','x','r']
                    # if we want to go further in the validation
                    # else: # validation of options that don't take parameters ['op' , 'or' , 'on', 'fe', 'wa', 'wr', 'q', 'h']
                    # if we want to go even further...
        else:
            return False
        return estValide
