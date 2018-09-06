def isGoodChar(char):
	return char.isalpha() or char == "-"

def text2words(text):
	words = []
	curr = ""
	text = text.lower()
	for el in text + "#":
		if isGoodChar(el):
			curr += el
		else:
			if len(curr) != 0:
				words.append(curr)
			curr = ""
	return words

if __name__ == "__main__":
	print(text2words(input()))