#------------------------
#!/usr/bin/env python   
# qm_minimizer.py       -
# Marc Yassin           -
# EE26 Professor Chang  -
#                       ----------------------------------------------------------------
# A program that implements the Quine Mcluskey method of reducing boolean functions   --
##--------------------------------------------------------------------------------------
import math
import itertools
import sys
import re

#########################################################################################
###################**   Function Definitions   ##########################################
#########################################################################################

def __findnuminputs(some_list) : # Finds number of literals

	temp = sorted(some_list)
	value = temp[-1]
	value = value.bit_length()
	return value

def occurs_once(a, item): # determines whether an index occurs one (helps with petricks)
    return a.count(item) == 1

def convert_to_characters(solution): # converts list of digits to Alphabetic representation
	n = solution[0]
	name = [0] * numliterals
	j=1
	while n > 0:
		name[-1*j]=n%2
		n=n/2
		j+=1
	removeNum = int(math.log(len(solution))/math.log(2))
	for i in range(0,len(name)):
		if name[i]==1:
			name[i]=chr(ord("A")+i)
		else:
			name[i]=chr(ord("A")+i)+"'"
	rm = []
	j = 1
	while len(rm) < removeNum:
		x = solution[0]^solution[j]
		if (bin(x).count("1") == 1):
			rm.append(int(math.log(x)/math.log(2)))
		j+=1
	strname=""
	for i in range(0,len(name)):
		if (numliterals-(i+1)) not in rm:
			strname+=name[i]
	return strname
	
def convert_to_charactersPOS(solution): # converts POS numbers to alphabetic representation
	n = solution[0]
	name = [0] * numliterals
	j=1
	while n > 0:
		name[-1*j]=n%2
		n=n/2
		j+=1
	removeNum = int(math.log(len(solution))/math.log(2))
	for i in range(0,len(name)):
		if name[i]==1:
			name[i]=chr(ord("A")+i)+"'"
		else:
			name[i]=chr(ord("A")+i)
	rm = []
	j = 1
	while len(rm) < removeNum:
		x = solution[0]^solution[j]
		if (bin(x).count("1") == 1):
			rm.append(int(math.log(x)/math.log(2)))
		j+=1
	strname=""
	for i in range(0,len(name)):
		if ((numliterals-(i+1)) not in rm):
			strname+="+"+name[i]
	return strname
	
def chunks(l, n): # Separates a list into smaller lists. l = list, n = amount to pair
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]
	
def rmdupes(x) : # removes any duplicates from a list
	nomodupes = list()
	for i in range(0, len(x)) :
		x[i] = sorted(x[i])
	temp = sorted(x)
	for i in range(len(temp)) :
		if (i == 0 or ((temp[i] != temp[i-1]))) : 
			nomodupes.append(temp[i])
	return nomodupes
	
	
def arrangebyones(terms) : # takes a list of numbers and arranges them by number of ones
	if len(terms) == 0 :
		return None
	groups = [[] for i in range(0, numliterals + 1)]
	for i in range(0, len(terms)) :
		number_of_ones = bin(terms[i]).count("1")
		groups[number_of_ones].append(terms[i])
	return groups
	
def get_onecubes(ones) : # grabs the onecubes that can be formed from a list of one. If none made
	onecubes_o = [[] for i in range(0, numliterals)] # then PI is updated and finished
	tempPI = []; onecubes_PI_check = []

	for i in range(0, len(ones)-1) : 
		if not ones[i] :
			if (not ones[i+1] == False) and (ones[i+1] == ones[-1]) :
				for m in range(0, len(ones[i+1])) :
					PrimeImplicants[0].append(ones[i+1][m])
			else : 
				continue
		for j in range(0, len(ones[i])) :
			if not ones[i+1] :
				tempPI.append(ones[i][j])
				continue
			for k in range(0, len(ones[i+1])) :
				checkdc = ones[i][j]^ones[i+1][k]
				does_it_combine = bin(checkdc).count("1")
				and_check = (ones[i][j])&(ones[i+1][k])
				and_check = bin(and_check).count("1")
				if (does_it_combine == 1) :
					onecubes_o[and_check].append(ones[i][j]) 
					onecubes_o[and_check].append(ones[i+1][k])
					onecubes_PI_check.append(ones[i][j]) 
					onecubes_PI_check.append(ones[i+1][k])
				else :
					tempPI.append(ones[i][j]); tempPI.append(ones[i+1][k])
	for x in range(0, len(onecubes_o)) : 
		onecubes_o[x] = chunks(onecubes_o[x],2)					
	if not tempPI :
		return onecubes_o
		
	for item in range(0, len(tempPI)) :
		if tempPI[item] not in onecubes_PI_check :
			PrimeImplicants[0].append(tempPI[item])
		
	PrimeImplicants[0] = list(set(PrimeImplicants[0])); PrimeImplicants[0] = sorted(PrimeImplicants[0]) # remove duplicates
	
	
	cubes[1] = onecubes_o 
	
	return onecubes_o 
	
	
def get_ncubes(ncubes, n) :	# Function gets passed onecubes and then minimizes it continuously
							# Until no longer reducable
	
	# Arguments :
	# ncubes -- corresponds to current cubegroup that will be minimized
	# 			example : onecubes,
	 
	# n      -- corresponds to the number of the cubegroup to help with storing/recursion	
	
	tempPrimes = []		# Placeholder for first round of Prime Implicant searching. Re-initializes every iteration		
	tempcubes = []		# Placeholder for the new cubes that are combined from what is in ncubes. Re-initializes every iteration
	tempcubesPIcheck = [] # Contains the elements from ncubes that do combine, however does not merge them yet. 
							# This is needed for the next round of PI checking
	newPrimes = []			# Placeholder for all the actual Prime Implicants than can be made on this iteration..Is sent to PI



	# Searches through ncubes list....or cube groups within ncubes
	for i in range(0, len(ncubes)-1) :	
		if not ncubes[i] : # if a cubegroup according to its number is empty, move on..
			continue		
		for j in range(0, len(ncubes[i])) : # searches through the contents of each cube group within ncubes 
			if not ncubes[i+1] : # if next cube group is empty, move on.... a.k.a no need to compare
				continue
			for k in range(0, len(ncubes[i+1])) : # searches through  contents of the next cube group
				for l in range(0, (2**(n))) :  # For each individual item within a cube, inside of a cubegroup...execute the following
					
					x1 = ncubes[i][j][0]; x2 = ncubes[i][j][-1] 
					y1 = ncubes[i+1][k][0]; y2 = ncubes[i+1][k][-1] 
					diffx = abs(x1-x2) # Find difference between first entry and last entry of a cube within a cubegroup
					diffy = abs(y1-y2) # Find difference between first entry and last entry of a cube within next cubegroup
					xorbit = x1^y1 # Perform bitwise xor for first entry of cube and first entry of next cubegroup cube
					
					if (bin(xorbit).count("1") == 1) and (diffx ==diffy) : # If those things true, 
						merge_n_cubes = ncubes[i][j] + ncubes[i+1][k]
						tempcubes.append(merge_n_cubes)					# tempcubes gets the combination
						tempcubesPIcheck.append(ncubes[i][j]); tempcubesPIcheck.append(ncubes[i+1][k])  
						# tempcubesPIcheck does not combine them but appends them so that primes can be found
					
					else :
						tempPrimes.append(ncubes[i][j]); tempPrimes.append(ncubes[i+1][k])
						# If the two cubes cannot combine, the cubes are added to tempPrimes placeholder
						# to be compared with tempcubesPIcheck
	
	tempPrimes = rmdupes(tempPrimes) # removes duplicates, faster for searching	
	tempcubes = rmdupes(tempcubes) # removes duplicates, order doesnt matter
	
	newcubes = [[] for i in range(0, numliterals)] # Readies next cube group for recursive iteration
		# Since, tempcubes as of right now cannot be passed to next iteration because it is not arranged by number of ones
		
	for i in range(0, len(tempcubes)) :
		andbit = tempcubes[i][0]
		for j in tempcubes[i]:
			andbit &= j
		andbit = bin(andbit).count("1")		
		newcubes[andbit].append(tempcubes[i])
		
	# Now, newcubes contains all the new cube combinations and has arranged them by number of ones

	cubes[n+1] = newcubes # To keep track of all cubes being made, I append newcubes to global cubes[n+1]
					# to correspond to the size of the cube that its holding
	
	
	# Prime Implicant Evaluation :
	# for each entry in tempPrimes, if one is not found within tempcubesPIcheck, this 
	# signifies that it is indeed a Prime Implicant. We store to newPrimes 
	for i in range(0, len(tempPrimes)) :
		if tempPrimes[i] not in tempcubesPIcheck :
			newPrimes.append(tempPrimes[i])          # Return newPrimes to PI[n]
	
	PrimeImplicants[n] = newPrimes

	# newPrimes contains all, if any, Prime Implicants that were made in this iteration 
	
	# Check for additional Iterations 
	if (len(tempcubes) == 1) : # if only one combination has been made, we are DONE
		PrimeImplicants[n+1] = tempcubes  # global PI gets that cube according to its cubenumber
	elif (len(tempcubes) == 0) : # if no new combinations were made, we are DONE 
		PrimeImplicants[n] = cubes[n] # global PI gets the cubes that were made in the last iteration as PI's
	else :
		return get_ncubes(newcubes, n+1) # Else, repeat method for next cubegroup 
		
def getfinalPIs(PrimeImplicants) : # Checks through list of all implicants by ones
	finalPIs = []                  # puts all implicants into a single order list
	for i in range(0, len(PrimeImplicants)) :
		if (i == 0) and (len(PrimeImplicants[i]) != 0) :
			for items in range(0,len(PrimeImplicants[i])) :
				finalPIs.append(PrimeImplicants[i][items])
		for j in range(0, len(PrimeImplicants[i])) :
			if not PrimeImplicants[i][j] :
				continue 
			try :
				for k in range(0,len(PrimeImplicants[i][j])) :
					if ((not PrimeImplicants[i][j][k]) == False) :
						try : 
							for l in range(0, len(PrimeImplicants[i][j][k])) :
								if ((not PrimeImplicants[i][j][k][l]) == False) :
									if PrimeImplicants[i][j][k] not in finalPIs : 
										finalPIs.append(PrimeImplicants[i][j][k])
						except TypeError :
							if PrimeImplicants[i][j] not in finalPIs : 
								finalPIs.append(PrimeImplicants[i][j])
												
			except TypeError :
				if ((not PrimeImplicants[i][j]) == False) :
					if PrimeImplicants[i][j] not in finalPIs :  
						finalPIs.append(PrimeImplicants[i][j])
						
	for imp in range(0, len(finalPIs)) :
		try :
			noneed = len(finalPIs[imp])
		except TypeError :
			finalPIs[imp] = [finalPIs[imp]]
			
	return finalPIs # returns the final PIs all arranged in a single list within a list structure
	
def writesolution(Essentials) : # Prints SOP solution
	sol = []
	for i in range(0, len(Essentials)) :
		#if Essentials[i] != Essentials[-1] :
		sol.append(convert_to_characters(Essentials[i]))
		#else :
		#	print convert_to_characters(Essentials[i])
	sorted(sol)
	expression = "+".join(sol)
	print "SOP Minimization: ",expression # Print SOP 
	
def writesolutionPOS(Essentials) : # Prints POS solution
	sol = []
	for i in range(0, len(Essentials)) :
		sol.append(convert_to_charactersPOS(Essentials[i]))
	sorted(sol)
	for k in range(0, len(sol)) :
		sol[k] = sol[k][1:]
	expression = ")(".join(sol)
	print "POS Minimization:  "+"("+expression+")" # Print SOP 
	
def dopetriks(be,a) : # Executes petricks method to get cheapest secondary EPI	   

	PIcontainercheck = []
	cheapest = []

	for L in range(0, len(a)+1):
		for subset in itertools.combinations(a, L):
			PIcontainer = []
			check = list(subset)
			for i in range(0, len(check)) :
				for j in range(0, len(check[i])) :
					PIcontainer.append(check[i][j])		
			if (set(be) <= set(PIcontainer)) :
				
				PIcontainercheck.append(check)
			
	thoseineed_length = min(map(len,PIcontainercheck))

	for i in range(0, len(PIcontainercheck)) :
		if (len(PIcontainercheck[i]) == thoseineed_length) :
			cheapest.append(PIcontainercheck[i])
		

	return cheapest[0]
	
def get_EPIs(mterms, PrimeImps) : # gets Primary EPIs from first round of minterms and PIs
	
	PrimaryEssentialPIs = []
	petrikPIs_check = []
	petrikPIs = []
	checkpetrikPI = []
	petrikmterms = [] 
	EPIs = []
	checkEPIs = []

	for term in range(0, len(mterms)) : 
		iscovered = [False] * len(PrimeImps)
		for item in range(0, len(PrimeImps)) : 
			if (mterms[term] in PrimeImps[item]) :
				iscovered[item] = True
	
		if (occurs_once(iscovered, True)) :
			for item in range(0, len(iscovered)) :
				if iscovered[item] == True :
					PrimaryEssentialPIs.append(PrimeImps[item])
	
	for a in range(0, len(PrimaryEssentialPIs)) :
		for b in range(0, len(PrimaryEssentialPIs[a])) :
			petrikPIs_check.append(PrimaryEssentialPIs[a][b])
		
	for term2 in range(0, len(mterms)) :
		if mterms[term2] not in petrikPIs_check :
			petrikmterms.append(mterms[term2])
		
	for imp in range(0, len(PrimeImps)) :
		if PrimeImps[imp] not in PrimaryEssentialPIs :
			petrikPIs.append(PrimeImps[imp])

	PrimaryEssentialPIs = rmdupes(PrimaryEssentialPIs)		

	for epi in range(0, len(PrimaryEssentialPIs)) :
		EPIs.append(PrimaryEssentialPIs[epi])
		
	# Check if Petricks method is needed, if not return EPIs
	for i in range(0, len(EPIs)) :
		for j in range(0, len(EPIs[i])) :
			checkEPIs.append(EPIs[i][j]) 
	
		
	if (set(Minterms) <= set(checkEPIs)) :
		return EPIs 
	
	
	# If above condition not satisfied...prepare for petriks method : 
	
	for prime in range(0, len(petrikPIs)) : 
		if (set(petrikmterms) < set(petrikPIs[prime])) :
			checkpetrikPI.append(petrikPIs[prime])

	
	if len(checkpetrikPI) > 1 : 
		# Now choose which one is cheaper
		EPIs.append(min(checkpetrikPI))
		return EPIs
		
	lastEPIs = dopetriks(petrikmterms,petrikPIs)
	
	EPIs = EPIs + lastEPIs
	
	return EPIs 
	
def getinput(): # UI for getting minterms and dontcares...

	s = raw_input("Boolean Expression to minimize: ")
	if "m" and "(" and ")" not in s :
		print "Minterms not spcified. Expression must be of form : "
		print "m(1,2,3)  m(4,5,6)+d(7,8)  m(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)"
		return getinput()	
		
	if "+" in s :
		index = s.find("+")
		mtermpart = s[0:index+1]
		dcpart = s[index+1:len(s)]

		mtermpart = mtermpart[mtermpart.find("(")+1:mtermpart.find(")")]
		mtermpart = mtermpart.split(',')
		dcpart = dcpart[dcpart.find("(")+1:dcpart.find(")")]
		dcpart = dcpart.split(',')

		mtermpart = map(int,mtermpart)
		dcpart = map(int,dcpart)

		return mtermpart,dcpart 
	
	else: 
		mtermpart = s[s.find("(")+1:s.find(")")]
		mtermpart = mtermpart.split(',')
		mtermpart = map(int,mtermpart)
		dcpart = []	
		return mtermpart,dcpart

def getmaxterms(mterms, dcterms, numinputs) :
	getmissing = range(0, (2**numinputs))
	maxterms = []
	for i in range(0, len(getmissing)) :
		if ((getmissing[i] not in mterms) and (getmissing[i] not in dcterms)) :
			maxterms.append(getmissing[i])
	return maxterms
	
again = ["yes","yup","Y","y","yea","yeah","yess"] # i was lazy...could make reg expression to grab
													# yes, no indicators
	
####################################################################################
###################**   Initialize data, variables   ###############################
####################################################################################	

print "----------------------------------------------"
print "----   Quine Mccluskey Minimizer   -----------"
print "------               by               --------"
print "---------               Marc Yassin      -----"
print "----------------------------------------------" 
print "---   INSTRUCTIONS   -------------------------" 
print "----------------------------------------------"
print "| Enter minterms and any dontcare values of  |"
print "| the form: m(1,2,3)+d(0,6) or m(3.7).       |"
print "| POS & SOP expressions will then be solved  |"
print "----------------------------------------------"          

while True : # sets up repeated use of program in one exuction

	Minterms, Dontcares = getinput() # gets Minterms, Dontcares to analyze
	terms = Minterms+Dontcares
	terms.sort()
	numliterals = __findnuminputs(terms) # number of inputs that are given
	Maxterms = getmaxterms(Minterms, Dontcares, numliterals) # gets maxterms to repeat
									# minimization and print solution
	
	range_of = range(0, (2**numliterals))
	
	if terms == range_of :
		if terms == [0] :
			print "Minimal Reduction = A'B'"
		else:
			print "Minimal Reduction = 1"
	elif (Minterms == [0,1]) and (numliterals <= 2) :
		print "Minimal Reduction = A'"
		
	elif (Minterms == [0,2,3]) and (numliterals <= 2) :
		print "Minimal Reduction = A+B'"

	elif (Minterms == [0,1,3]) and (numliterals <= 2) :
		print "Minimal Reduction = A'+B" 
	elif (Minterms == [1,3]) and (numliterals <= 2) :
		print "Minimal Reduction = B"
	elif (Minterms == [0]) and (numliterals <= 2) :
		print "Minimal Reduction = A'B'"
	elif (Minterms == [0,2]) and (numliterals <= 2) :
		print "Minimal Reduction = B'"
		

	else:
	
		# Initialize for SOP solution
		cubes = [[] for i in range(0, numliterals+1)]# to be used inside function
		PrimeImplicants = [[] for i in range(0, numliterals)] # PI's so far

		ones = arrangebyones(terms)
		onecubes = get_onecubes(ones)
		get_ncubes(onecubes, 1)
		PrimeImplicants = getfinalPIs(PrimeImplicants)
		EssentialPIs = get_EPIs(Minterms, PrimeImplicants)
		writesolution(EssentialPIs)
	
		################################################################################
		################################################################################
		
		# Initialize and execute for POS solution
		Minterms = Maxterms # Load Maxterm values into Minterms to begin POS
		terms = Minterms+Dontcares # Then repeat rest of it
		terms.sort() 
		cubes = [[] for i in range(0, numliterals+1)]# to be used inside function
		PrimeImplicants = [[] for i in range(0, numliterals)] # PI's so far

		ones = arrangebyones(terms)
		onecubes = get_onecubes(ones)
		get_ncubes(onecubes, 1)
		PrimeImplicants = getfinalPIs(PrimeImplicants)
		EssentialPIs = get_EPIs(Minterms, PrimeImplicants)
		writesolutionPOS(EssentialPIs)
		print
	
	askuser = raw_input("Minimize again? (y/n) ")
	if askuser not in again : 
		break
	print "" 
    




	
	





				
  				
















