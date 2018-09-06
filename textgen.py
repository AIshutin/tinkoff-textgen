from model import TextGenerator
from model import save, load
from optparse import OptionParser as ArgumentParser
import pickle

if __name__ == "__main__":
	parser = ArgumentParser(description='Generate some text')
	parser.add_option('-t', "--train", help="Specifying text for training.", type="string")
	parser.add_option('-s', '-S', '--save', help="Specifying destination of saved weights.", type="string")
	parser.add_option('-g', '-G', '--generate', help="Specifying the length of desired sample", type="int")
	parser.add_option('-l', '-L', '--load', help="Specifying file with weights to load", type="string")
	args = parser.parse_args()[0]
	model = TextGenerator()

	if args.load is not None:
		model = load(args.load)

	if args.train is not None:
		with open(args.train, encoding="utf-8") as file:
			model.fit(file.read())

	if args.save is not None:
		save(model, args.save)

	if args.generate is not None:
		 print(model.generate(args.generate))
