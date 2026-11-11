#This script has been written to generate multiple files that have been altered from an original template, for the purpose of making color orthophoto .set files for each Image ID. 
#It will also make a .bat file to be run to generate these color ortho images. 
#This script will take in three inputs the bin size of your DTM, the orthophoto template, and colorlist 
#This script will make these files in the current directory you are in. So make sure you are in the right directory!
#It will take the orthophoto template and read it in line by line 
#once it comes accross ortho.gsd, .output_file,and .image, it will make alterations to these lines in regards to the current image ID
#The 1st loop iterates throught the colorlist and generates the set files at the bin size of your DTM
#2nd loop iterates through the colorlist file and reads the last character, which should be either a 1, 2, or 4.
#The 1, 2, or 4 represent the bin size of each ID, it will then write the appropriate .set file and cmd line call, then append it to the master color orthos file. 
#This will out put one bat file called master_color_orthos.bat, this will have all the calls
#Another crucial step is to run this script by compiling it with your current version of python, i.e:> python ColorOrtho_setFileGen_V2.py


#instructions on how to run this script:
'''
# Open an existing 25 cm (or 50 cm) orthophoto settings file in your batch directory, it will end in a .set, then save as orthophoto_template.set
# In the project data directory, make a list of the color sup files to make into orthophotos
# For example: in cygwin: ls *COLOR*.sup | sed s/.sup// > colorlist
# Next edit the colorlist to specify what bin each ID is. Using a text editor, put at the end of each image ID a 1 or 2 depending on what the bin size is(1 or 2).
# Here is an example of a colorlist with mixed bin:
	ESP_026905_1660_UNFILTERED_COLOR_BG 1
	ESP_026905_1660_UNFILTERED_COLOR_IR 1
	ESP_026905_1660_UNFILTERED_COLOR_RED 1
	ESP_027182_1660_UNFILTERED_COLOR_BG 2
	ESP_027182_1660_UNFILTERED_COLOR_IR 2
# Make sure that there is nothing else but the 1 or 2 at the end of each line.
# If you have just one bin size than the endings will be all 1's or 2's. 
# Move the colorlist into the batchdir directory, where the orthophoto template is
# Bring up a command prompt and cd to the batch directory.
# Then open up a windows explorer and go into the Local Disk C:\scripts. 
# Type python then drag and drop ColorOrtho_setFileGen.py into your command prompt and follow the prompts from the script.
# Should look like this : 
	~\batch_dir> python C:\scripts\ColorOrtho_setFileGen_V2.py
# Note: you can drag and drop the files into the cmd prompt. 
# The script output and input should look like this:  
	Please enter the bin size of your DTM, '1,2':    1
	Enter the orthophoto template file:     orthophoto_template.set
	Enter the color list:   colorlist
# Once the script has finished you will have one .bat file called master_color_orthos.bat, just double click on this file and it will generate your color orthos. 

'''
import csv
import sys
import os

#these ask the user to input the colorlist and color_orthotemplate, and bin size
res=str(raw_input("Please enter the bin size of your DTM, '1,2,4': \t"))
template=raw_input("Enter the orthophoto template file:\t")
colorlist=raw_input("Enter the color list:\t")

batName=colorlist

#this check sees if there is a file already a master_orthos file in your current working directory, if so it will delete it. 
if (os.path.isfile("master_color_orthos.bat")):
	os.remove("master_color_orthos.bat")

#this will check to see if there is a bin size at the end of the Image ID being read in from colorlist
#if there is one line that does not contain any bin size or the proper bin size, then it will not make the lower bin size orthos
for index in (open(colorlist.strip(),"r")):
	index=index.strip()
	if index[-1] =="1" or index[-1]=="2"or index[-1]=="4":
		binResPresent= True 
	else:
		binResPresent=False
		break


if binResPresent:
	for index in (open(colorlist.strip(),"r")):#this will open the colorlist file read it in and assigns the current line to the var index for every pass, 
											   #will iterate through until no more lines in colorlist 
		index=index.strip()#have to strip off all white spaces otherwise open(file) will not recognize index as a suitable file name 
		#this check will strip off the ending of 1 or 2 if it exists on the index string being read in. 
		if index[-1]=="1" or index[-1]=="2"or index[-1]=="4":
			index=index[:-1].strip()
		new_file=open(index+"_"+res+"m.set",'w')#generates a new file for each ortho image
											#plus ads the .set which states what type of file it will be
		
		file=open(template,"r") #have to reopen and close the template file every time in order to be able write into each new generated file
								
		
		for line in file:
			
			
			#These will be cases that individualy check each line in the file
			#to see if they match certain key words, if they do then it alters the line
			
			#after each check you have to write a new line to make sure that the lines dont bunch up
			if "ortho.image" in line:
				new_file.write("ortho.image    \t\t\t\t\t"+index+".sup\n")#also adds on the.sup tag
				
			elif "ortho.output_file" in line:
				new_file.write("ortho.output_file\t\t\t\t "+index+"_"+res+"m_o\n")
			elif "ortho.gsd" in line: 
				new_file.write("ortho.gsd\t\t\t\t\t\t "+res+".0\n")
			else:
				new_file.write(line)
		#This will first create a master_orthos bat folder and then write into it for every index in the colorlist 
		#it will write out a string to call and start each color orthophoto that is in the color list. 
		master_bat_file=open("master_color_orthos.bat","a")
		master_bat_file.write("call start_socet -single orthophoto -batch -s "+index+"_"+res+"m.set \n")
		

		master_bat_file.close()#closes the master_bat file
		file.close()#closes the template file 
		new_file.close()#closes the current image file




	for index in (open(colorlist.strip(),"r")):#this will open the colorlist file read it in and assigns the current line to the var index for every pass, 
												   #will iterate through until no more lines in colorlist 
			index=index.strip()#have to strip off all white spaces otherwise open(file) will not recognize index as a suitable file name 	
			
			#this check will see what bin size each index is and then assign it to the var res. 
			if index[-1]=="1":
				res="25"
			elif index[-1]=="2":
				res="50"
			else:
				res="1"
			
			new_file=open(index[:-1].strip()+"_"+res+"cm.set",'w')#generates a new file for each ortho image
												#plus ads the .set which states what type of file it will be
			
			file=open(template,"r") #have to reopen and close the template file every time in order to be able write into each new generated file
			
			if res =="1":
				for line in file:
				

					#These will be cases that individualy check each line in the file
					#to see if they match certain key words, if they do then it alters the line
				
					#after each check you have to write a new line to make sure that the lines dont bunch up
					if "ortho.image" in line:
						new_file.write("ortho.image    \t\t\t\t\t"+index[:-1].strip()+".sup\n")#also adds on the.sup tag
					
					elif "ortho.output_file" in line:
						new_file.write("ortho.output_file\t\t\t\t "+index[:-1].strip()+"_"+res+"m_o\n")
					elif "ortho.gsd" in line: 
						new_file.write("ortho.gsd\t\t\t\t\t\t "+"."+res+"\n")
					else:
						new_file.write(line)
			else:
				for line in file:
				

					#These will be cases that individualy check each line in the file
					#to see if they match certain key words, if they do then it alters the line
				
					#after each check you have to write a new line to make sure that the lines dont bunch up
					if "ortho.image" in line:
						new_file.write("ortho.image    \t\t\t\t\t"+index[:-1].strip()+".sup\n")#also adds on the.sup tag
					
					elif "ortho.output_file" in line:
						new_file.write("ortho.output_file\t\t\t\t "+index[:-1].strip()+"_"+res+"cm_o\n")
					elif "ortho.gsd" in line: 
						new_file.write("ortho.gsd\t\t\t\t\t\t "+"."+res+"\n")
					else:
						new_file.write(line)
			#This will first create a color_orthos bat folder and then write into it for every index in the colorlist 
			#it will write out a string to call and start each color orthophoto that is in the color list. 

			master_bat_file=open("master_color_orthos.bat","a")
			if res =="1":
				master_bat_file.write("call start_socet -single orthophoto -batch -s "+index[:-1].strip()+"_"+res+"m.set \n")
			else:
				master_bat_file.write("call start_socet -single orthophoto -batch -s "+index[:-1].strip()+"_"+res+"cm.set \n")
			

			master_bat_file.close()
			
			
			
			file.close()#closes the template file 
			new_file.close()#closes the current image file
else:
	print "Could not make lower bin size color orthos. Check your colorlist file!"








