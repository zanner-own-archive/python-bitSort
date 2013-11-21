#!/bin/py

class bitSort :
	def __init__ (self, mask, order, up = None, down = None) :
		''' '''
		self.maskInput, self.orderInput = mask, order
		if up==None : up = ['u', 'U', '1', '+', 1]
		if down==None : down = ['d', 'D', '0', '-', 0]
		mask = map(lambda x : int(x), mask)
		offset = range(0, len(mask))
		offset.reverse()
		order = map(lambda x : 1 if x in up else -1 if x in down else 0, order)
		#
		result = zip(mask, offset, order)
		result.sort(lambda x, y : 1 if x[0]>y[0] else -1 if x[0]<y[0] else 0)
		mask, offset, order = zip(*result)
		self.mask = zip(offset, order)

	def compare (self, valueA, valueB) :
		'''compare return True if "a" and "b" should swap'''
		for offset, direction in self.mask :
			a, b = (valueA >> offset) & 1, (valueB >> offset) & 1
			if a==b : continue
			return False if (a-b)*direction>0 else True
		return False

	def sort (self, array) :
		'''sort'''
		a, r = array[:], 1
		a.sort(lambda x, y: r if self.compare(x, y) else -r)
		return a

class bitOut :
	def __init__ (self, bitSort, bitSeparator = " ", arraySeparator = ", ", delimiter = "\t") :
		self.bitSort = bitSort
		self.bitSeparator, self.arraySeparator = bitSeparator, arraySeparator
		self.delimiter = delimiter

	def binary (self, value) :
		if value<0 : return "-"
		result = []
		for i in xrange(0, len(self.bitSort.mask)) :
			result.insert(0, value & 1)
			value >>= 1
		return self.bitSeparator.join(map(lambda x: str(x), result))

	def binaryArray (self, array) :
		for a in array :
			print self.binary(a), self.delimiter, a

	def lineArray (self, array) :
		print self.bitSeparator.join(map(lambda x: str(x), array))

	def mask (self) :
		print self.bitSeparator.join(map(None, self.bitSort.maskInput))
		print self.bitSeparator.join(map(None, self.bitSort.orderInput))


if __name__!='__main__' : exit(0);

from argparse import ArgumentParser
from sys import argv

p = ArgumentParser(add_help=True, prefix_chars='-', prog='bitSort', description='...', epilog='buy')
#p.add_argument('-n', dest='mo', help='bit-mask & bit-order, like: 8u1d7d2u6u3d5d4u')
p.add_argument('-m', '--mask', dest='m', help='bit-mask, like: 81726354')
p.add_argument('-o', '--order', dest='o', help='bit-order, like: udduuddu')
p.add_argument('-v', '--value', dest='v', nargs='*', default='1-10', help='values, like: 1,2 3 7-10, 20-30+3')
p.add_argument('-b', '--binary', dest='b', action='store_true', default=None, help='binary input & output')
p.add_argument('-bi', '--binary-input', dest='bi', action='store_true', default=None, help='binary input')
p.add_argument('-bo', '--binary-ouput', dest='bo', action='store_true', default=None, help='binary output')
run, runUnknown = p.parse_known_args(argv)

if run.m==None or run.o==None or run.v==None : exit(0)

import re
RE = ('^ ([\d]+) $', '^ ([ud\-\+01]+) $', '^ ([\d]+) [\-] ([\d]+) $', '^ ([\d]+) [\-] ([\d]+) [\+] ([\d]+) $')

mask = re.match('[\s]*'.join(RE[0].split(' ')), run.m)
mask = None if mask==None else mask.group(0)
order = re.match('[\s]*'.join(RE[1].split(' ')), run.o, re.I)
order = None if order==None else order.group(0)
values = []
for vv in run.v :
	for v in vv.split(',') :
		v1 = re.match('[\s]*'.join(RE[0].split(' ')), v)
		v2 = re.match('[\s]*'.join(RE[2].split(' ')), v)
		v3 = re.match('[\s]*'.join(RE[3].split(' ')), v)
		if v1!=None : values.append(int(v1.group(0)))
		elif v2!=None :
			for i in xrange(int(v2.group(1)), int(v2.group(2))+1) : values.append(i)
		elif v3!=None :
			for i in xrange(int(v3.group(1)), int(v3.group(2))+1, int(v3.group(3))) : values.append(i)

binaryInput = run.bi if run.bi!=None else run.b if run.b!=None else False
binaryOutput = run.bo if run.bo!=None else run.b if run.b!=None else False

if mask==None or order==None or values==[] : exit(0)

x = bitSort(mask, order)
xx = bitOut(x)

#print run, runUnknown
#print
if binaryInput : xx.binaryArray(values)
else: xx.lineArray(values)
print
xx.mask()
print
if binaryOutput : xx.binaryArray(x.sort(values))
else: xx.lineArray(x.sort(values))
print
