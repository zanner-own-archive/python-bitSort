#!/bin/py

def castMask (mask) :
	'''	castMask ( (string) mask )
		-> [ (int) bit, (int) bit, ... ]
		convert bit-mask to dictionary of bits
	'''
	return map(lambda x : int(x), mask)


def castOrder (order, up = None, down = None) :
	'''	castOrder ( (string) order [, (array) up [, (array) down ] ] )
		-> [ {-1|1}, ... ]
		convert order-mask to dictionary of orders'
	'''
	if up==None : up = ['u', 'U', '1', '+', 1]
	if down==None : down = ['d', 'D', '0', '-', 0]
	return map(lambda x : 1 if x in up else -1 if x in down else 0, order)


def castMaskOrder (mask, order, up = None, down = None) :
	''' castMaskOrder ( (string) mask, (string) order [, (array) up [, (array) down ] ] )
		-> [ ( (int) bit, {-1|1} ), ( (int) bit, {-1|1} ), ... ]
		convert bit-mask and order-mask to dictionary of mask-order cortages 
	'''
	mask = castMask(mask)
	order = castOrder(order, up = up, down = down)
	offset = range(0, len(mask))
	offset.reverse()
	result = zip(mask, offset, order)
	result.sort(lambda x, y : 1 if x[0]>y[0] else -1 if x[0]<y[0] else 0)
	return result


def bitCompare (a, b, maskOrder) :
	'''
	'''
	for num, mask, order in maskOrder :
		aa, bb = (a >> mask) & 1, (b >> mask) & 1
		if aa==bb : continue
		if aa<bb : return True if order>0 else False 
		if aa>bb : return True if order<0 else False
	return False


def bitSort (A, maskOrder) :
	'''
	'''
	for i in xrange(0, len(A)) :
		for j in xrange(i+1, len(A)) :
			if bitCompare(A[i], A[j], maskOrder) : A[i], A[j] = A[j], A[i]
	return A


def bitRun (arg) :
	'''
	'''
	flags = { '-m': '-m', '-mask': '-m', '-o': '-o', '-order': '-o', '-mo': '-mo', '-maskOrder': '-mo', '-v': '-v' }
	flag, array, mask, order = '', [], None, None
	# 
	for a in arg[1:] :
		if a in flags.keys() : flag = flags[a]
		elif flag=='-m' : mask, flag = a, ''
		elif flag=='-o' : order, flag = a, ''
		elif flag=='-mo' : 
			mask, order, flag = '', '', ''
			for i in xrange(0, len(a)/2) :
				mask, order = mask + a[i*2], order + a[i*2 + 1]
		elif flag=='-v' :
			for i in xrange(1, int(a)) : array.append(i)
		elif flag=='' : array.append(int(a))
	#
	if mask!=None and order!=None :
		maskOrder = castMaskOrder(mask, order)
		arraySorted = bitSort(array[:], maskOrder)
		return { 'maskOrder': maskOrder, 'mask': mask, 'order': order, 'array': array, 'arraySorted': arraySorted, 'help': False }
	else :
		return { 'help': True }


def bitNumber (number, length) :
	if length>0 and number>0 :
		result = ''
		while length>0 :
			result = ('1' if number & 1 else '0') + result
			number = number >> 1
			length -= 1
		return result
	elif length>0 : return '_' * length
	else : return '<unknown>'


if __name__=='__main__' :
	from sys import argv as arg
	R = bitRun(arg)
	
	if R['help'] :
		print ''' ./bitSort.py [ -m mask -o order | -mo maskOrder ] numbers
	-m = -mask
	-o = -order
	-mo = -maskOrder
	numbers - array of number separated by space to bit-sort
		'''
	else:
		print 'Mask & order is'
		print R['mask']
		print R['order']
		print
		print 'Array is'
		for r in R['array'] :
			print bitNumber (r, len(R['mask'])), r
		print 
		print 'Mask & order is'
		print R['mask']
		print R['order']
		print
		print 'Sorted array is'
		for r in R['arraySorted'] :
			print bitNumber (r, len(R['mask'])), r
		print 
		print 'buy'

