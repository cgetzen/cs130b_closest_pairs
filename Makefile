
all: closestPair randData

closestPair: closestPair.py
	cp closestPair.py closestPair
	chmod +x closestPair

randData: randData.py
	cp randData.py randData
	chmod +=x randData

clean:
		rm -rf __pycache__ *.pyc closestPair randData
