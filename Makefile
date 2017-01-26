
all: closestPair randData

closestPair: closestPair.py
	cp closestPair.py closestPair
	chmod +rx closestPair

randData: randData.py
	cp randData.py randData
	chmod +rx randData

clean:
		rm -rf __pycache__ *.pyc closestPair randData *pickle*
