digits = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
multiples_of_ten = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def to_string(num):
	#accepts a list of single digit positive integers that is not longer than three and converts it to string 
	assert(len(num) <= 3)
	result = ""

	if len(num) == 3: #if hundreds are present
		result += digits[num[2]] + "hundred"
		num =  num[:-1] #append text and trim a digit
	if len(num) == 2: #number is higher or equal to ten
		if num[1] == 1: #teens
			return result + teens[num[0]]
		else:
			result += multiples_of_ten[num[1]]
	return result + digits[num[0]] #append the remaining digit

def tokenize(line):
	#Accepts a string and splits it into tokens valid tokens (digits, teens and so on).
	#Splits from the end to capture the longest possible valid sequence, becuase tokens line
	#sixty would be incorrectly matched as six and ty would screw up the rest of tokenizing
	result = []
	start = len(line) - 1
	end = len(line) 

	while start >= 0:
			candidate = line[start: end] #current token candidate
			if candidate in digits or candidate in teens or candidate in multiples_of_ten or candidate == "hundred" or candidate == "thousand":
				result.append(line[start: end]) #a token was found: append it and move indices
				end = start
			start -= 1
	
	if start != end - 1: #If there is a token in the line's prefix, add it as well
			result.append(line[start: end])
	result.reverse() # Since we have been matchich from the end, reverse the tokens
	return result


		

def validate(tokens):
	#Accepts a list of tokens and makes sure it is a valid number
	assert("thousand" not in tokens)

	if tokens.count("hundred") > 1: #There cannot be multiple 'hundreds'
		return False
	
	if "hundred" in tokens:
		if not tokens[0] in digits or tokens[1] != "hundred":
			return False #'hundred' must be prefixed by a digit
		if len(tokens) == 2:
			return True
		else:
			tokens = tokens[2:]

	if tokens[0] in teens:
		return len(tokens) == 1 #teens mustn't be followed by other tokens
	elif tokens[0] in multiples_of_ten:
		if len(tokens) == 1:
			return True
		else:
			tokens = tokens[1:]
	#finally match the last digit
	return len(tokens) == 1 and tokens[0] in digits






def to_digits(tokens):
	#Accepts a list of tokens to produce a numeric value, whose representation the list denotes
	assert("thousand" not in tokens)

	result = 0
	if len(tokens) > 1 and tokens[1] == "hundred": #hundreds must be prefixed by a digit (guaranteed from the problem specification)
		result = digits.index(tokens[0]) * 100
		tokens = tokens[2:] #Trim both digit and keyword hundred

	if len(tokens) == 0:
		return result
	if tokens[0] in teens: #if there's a teen, return value
		return result + 10 + teens.index(tokens[0])

	elif tokens[0] in multiples_of_ten:
		result += 10 * multiples_of_ten.index(tokens[0])
		tokens = tokens[1:] #trim multiple of ten

	if len(tokens) != 0: #there is a digit remaining
		assert(len(tokens) == 1)
		result += digits.index(tokens[0])
	
	return result





if __name__ == '__main__':
	line = input()
	
	if line.isdigit(): #if we received a numerical input, output strings
		num = [int(d) for d in line]
		num.reverse()
		if len(num) <= 3: #we have a number bigger than a thousand
			print(to_string(num))
		else:
			print( to_string(num[3:])+ "thousand" +to_string(num[0:3]) )
	
	else:
		tokens = tokenize(line)
		if tokens.count("thousand") > 1:
			print("ERROR")
			quit()
	
		if "thousand" not in tokens:
			if not validate(tokens):
				print("ERROR")
				quit()
			print(to_digits(tokens))
	
		else:
			first = tokens[:tokens.index("thousand")]
			second = tokens[tokens.index("thousand") + 1:]
			if not validate(first) or not validate(second):
				print("ERROR")
				quit()
			print(to_digits(first)*1000 + to_digits(second))