from utils import isGoodChar, text2words
import random as rd
import pickle

class NgramGen:
	N = 2
	distr = dict()

	def __init__(self, N):
		assert(N >= 2)
		self.N = N
		self.distr = dict()

	def gen_next(self, Nword):
		if Nword not in self.distr:
			res = self.choose_seed()[-1]
			return [res, ". " + res]
		assert(Nword in self.distr)
		sum = 0
		for el in self.distr[Nword]:
			sum += self.distr[Nword][el]
		prob = rd.randint(1, sum)
		for el in self.distr[Nword]:
			prob -= self.distr[Nword][el]
			if prob <= 0:
				return [el, el]
		assert(False)

	def fit(self, words):
		assert(len(words) >= self.N)
		queue = []
		qstart = 0
		for el in words[:self.N - 1]:
			queue.append(el)

		for el in words[self.N:]:
			curr_tokens = tuple(queue[qstart:])
			if curr_tokens not in self.distr:
				self.distr[curr_tokens] = dict()
			if el in self.distr[curr_tokens]:
				self.distr[curr_tokens][el] += 1
			else:
				self.distr[curr_tokens][el] = 1
			queue.append(el)
			qstart += 1

	def choose_seed(self):
		return rd.choice(list(self.distr))

	def generate(self, count, seed=None):
		if seed is None:
			seed = self.choose_seed()
		res = list(seed)
		for i in range(count):
			curr = self.gen_next(seed)
			res.append(curr[1])
			seed = seed[1:] + (curr[0], )
		return res


class PunctuationCorr:
	backward = dict()
	total = dict()
	char = ''

	def __init__(self, char):
		self.char = char
		self.backward = dict()
		self.total = dict()

	def fit(self, text):
		words = []
		curr = ""
		text = text.lower()
		was = set()
		for el in text + "#":
			if isGoodChar(el):
				curr += el
			else:
				if len(curr) != 0:
					words.append(curr)
				curr = ""
				was.add(el)
				if self.char == el:
					words.append(el)

		for el in words:
			if el not in self.total:
				self.total[el] = 0
				self.backward[el] = 0
			self.total[el] += 1
		
		for i in range(1, len(words) - 1):
			if words[i] == self.char:
				self.backward[words[i + 1]] += 1


	def correct(self, words):
		res = []
		was = True
		for el in words:
			if was:
				res.append(el)
				was = False
				continue

			if rd.randint(1, self.total[el]) <= self.backward[el]:
				res.append(self.char)
				res.append(el)
			else:
				res.append(el)
		return res

class TextGenerator:
	pcorr = None
	Ngram = None

	def __init__(self, N=2, char=','):
		self.pcorr = PunctuationCorr(char)
		self.Ngram = NgramGen(N)

	def fit(self, text):
		self.Ngram.fit(text2words(text))
		self.pcorr.fit(text)

	def generate(self, N, seed=None):
		return " ".join(self.pcorr.correct(self.Ngram.generate(N, seed))).replace(' ' + self.pcorr.char, self.pcorr.char)

	def __str__(self):
		return str(len(self.pcorr.backward )) + " : " + str(len(self.Ngram.distr))

def save(model, path):
	with open(path, "wb") as file:
		pickle.dump(model, file)

def load(path):
	with open(path, "rb") as file:
		return pickle.load(file)