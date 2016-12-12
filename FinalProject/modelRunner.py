'''
	Execution of this file will run all of the .pred files contained within the models folder
'''

import os
import glob
import zipfile
import fnmatch
import sys

if len(sys.argv) > 1:
	pythonexecutable = sys.argv[1]
else:
	pythonexecutable = "python"


try:
	os.chdir('./models')
	filenames = []
	for file in glob.glob('*.pred'):
		filenames.append(file)

	print('''

#####################################################


This file will execute the MAP scorer on the .pred files
contained within the models folder. To proceed through 
the files, please press enter on this console window 
when you are ready to view the next set of results. 


Getting ready to run experiments....



Here we go....

		''')
	os.chdir('..')
	for file in filenames:
		print('###################################')
		print('Running MAP for : ' + file)
		print('Press enter when ready or Ctrl+C to exit')
		if 'subtaskA' in file:
			os.system("gnome-terminal -e 'bash -c \"" + pythonexecutable + " ./scorer/MAP_scripts/ev.py ./scorer/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml.subtaskA.relevancy ./models/" + file +";exec bash\"'")
			raw_input()
		else:
			os.system("gnome-terminal -e 'bash -c \"" + pythonexecutable + " ./scorer/MAP_scripts/ev.py ./scorer/SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ./models/" + file +";exec bash\"'")
			raw_input()


	os.system("gnome-terminal -e 'bash -c \"sl; exec bash\"'")
	
	print('All prediction files executed')

except:
	Exception("""
	 There seems to be an error. Please ensure that the current Directory is
	 the FinalProject directory and that the models directory is a direct child of that 
	 directory. 
	  """)

print('''

Extracting crawler data for easy viewing...

Crawler data stored in ./Data/QTLCrawlerData

''')

rootPath = './Data/QTLCrawlerData'
pattern = '*.zip'
for root, dirs, files in os.walk(rootPath):
	for filename in fnmatch.filter(files, pattern):
		print(os.path.join(root, filename))
		zipfile.ZipFile(os.path.join(root, filename)).extractall(root)

print('''

All scripts executed.
Have a nice day.


         _nnnn_
        dGGGGMMb
       @p~qp~~qMb
       M|@||@) M|
       @,----.JM|
      JS^\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\dS"qML
 |    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMP|   .'
     `-'       `--' hjm



          .. ..oooo.....ooo...
    .odSS4PYYYSSOOXXXXXXXXXOodbgooo.
   /SSYod$$$$SSOIIPXXXXXXXXXYYP.oo.*b.
  ($$Yd$$$$SSSOII:XXXXXXXX:IIoSSS$$b.Y,
   \Yd$$$$SSSOII:XXXXXXXXXX:IIOOSSS$$$b
    d$$$$SSSOOI:XP"YXXXXXXXX:IIOOSSSS$$$
    Y$$$SSSOOII:XbdXXXXXP"YX:IIOOOSS$$$$)
    'Y$$$SSSOI:XXXXXXXXXbodX:IIOOSS$$$$$/
     "Y$$$SSSOI(PoTXXXXXTo)XXIIOOOSS$$$*'
       ""*Y$S(((PXXXXXXXY))dIIOSSS$$dP'
          "*'()P;XXXXXXXXY)IIOSSS$P".oS,
          (S'(P;XXXXXXXP;Y)XXYOP".oSSSSb
         (S'(P;'XXXXXXX';Y).ooooSSSSSSSS)
         (S'(P;'XXXXXXP';Y).oSSSSSSSSSSSP
         (SS'Y);YXXXXX';(Y.oSSSSSSSSSSSSP
          YSS'Y)'YXXX".(Y.oSSP.SSSSSSSSY
           YSS'"" XXX""oooSSP.SSSSSSSSY
           SSSSSS YXXX:SSSSP.SSSSSSSSY
           SSSSSP  YXb:SSSP.S"SSSSSSP
           S(OO)S   YXb:SY    )SSSSS
           SSSSO    )YXb.I    ISSSSP
           YSSSY    I."YXXb   Y(SS)I
           )SSS(    dSSo.""*b  YSSSY
           OooSb   dSSSSP      )SSS(
                   dSSSY       OooSS
                   OooSP             

''')

