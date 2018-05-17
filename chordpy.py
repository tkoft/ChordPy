import sys, re

scale = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
section_titles = ["intro", "verse", "chorus", "bridge", "tag", "instrumental"]

def transpose(note, step):
	noteNum = scale.index(note)
	noteNum = (noteNum+step) % 12
	return scale[noteNum]

filename = sys.argv[1]
name_parts = re.split('-', filename[:-4])
title = name_parts[0].strip()
if len(name_parts) < 2:
	name_parts.append("")
artist = name_parts[1].strip()

# Get transposition amt
while True:	
	transText = input("Transpose (+# or -#): ")
	if transText == "" or transText == None:
		transText = 0
		break	
	else:
		try:		
			transValue = int(transText)
			break
		except ValueError:
			print("Invalid transposition.")		
			
f = open(filename, "r")
outFilename = title + ("-"+artist, "")[artist == ""] + "_trans-"+str(transValue)+".html"
out = open(outFilename, "w+")

out.write('''<html>
	<head>
		<title>''' + title + " - " + artist + '''</title>
		<style> code {white-space: pre-wrap;} </style>
	</head>
<body>
	<h1>''' + title + "</h1>"
	+ ("<h2>" + artist + "</h2>", "")[artist == ""] + '''

	<code>''')	

skip_next_newline = False

for line in f:
	outputChords = ""
	outputLyrics = ""

	inBracket = False
	for i in range(len(line)):
		if line[i] == '[':
			inBracket = True
			outputChords = outputChords + " "*(max(0, len(outputLyrics)-len(outputChords)))
		elif inBracket and line[i] == ']':
			inBracket = False
		elif inBracket and line[i] =='#':
			pass
		elif inBracket and str.isupper(line[i]):
			if line[i+1] == '#':
				outputChords += transpose(line[i]+"#", transValue)
			else:
				outputChords += transpose(line[i], transValue)
		elif inBracket:
			#DONT TRANSPOSE AND PUT IN OUTPUTCHORDS
			outputChords = outputChords + line[i]
		else:
			outputLyrics = outputLyrics + line[i]
	
	outputChords = outputChords.strip()
	outputLyrics = outputLyrics.strip()

	isTitle = False;
	for t in section_titles:
		if t in line.lower():
			isTitle = True;
			break

	if isTitle:
		outputLyrics = ("<h3>" + outputLyrics.strip() + "</h3>")
		out.write(outputLyrics)
		skip_next_newline = True
	else:
		if not outputChords == "":
			if not skip_next_newline:
				outputChords = "\n" + outputChords
			out.write(outputChords)
			skip_next_newline = False

		if not outputLyrics == "":
			if not skip_next_newline:
				outputLyrics = "\n" + outputLyrics.strip()
			out.write(outputLyrics)
			skip_next_newline = False

out.write("</code></body></html>")
out.close()
f.close()

print("Transposed " + str(transValue) + " steps.")