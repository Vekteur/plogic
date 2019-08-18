from abc import ABC, abstractmethod

class LayeredDict:

	class Action(ABC):
		@abstractmethod
		def exec(self, d): pass
	class SetAction(Action):
		def __init__(self, key, value): self.key, self.value = key, value
		def exec(self, d): d[self.key] = self.value
	class PopAction(Action):
		def __init__(self, key): self.key = key
		def exec(self, d): d.pop(self.key)

	def __init__(self, d = {}):
		self.d = d
		self._layers = []
		self.pre_init()
		self.add_layer()
	def pre_init(self):
		pass
	def add_layer(self):
		self._layers.append([])
	def pop_layer(self):
		for action in reversed(self._layers[-1]):
			action.exec(self.d)
		self._layers.pop()
	def append_set_action(self, key):
		self._layers[-1].append(LayeredDict.SetAction(key, self.d[key]))
	def append_pop_action(self, key):
		self._layers[-1].append(LayeredDict.PopAction(key))
	def __getitem__(self, key):
		return self.d[key]
	def __setitem__(self, key, value):
		if key in self.d:
			self.append_set_action(key)
		else:
			self.append_pop_action(key)
		self.d[key] = value
	def pop(self, key):
		self.append_set_action(key)
		return self.d.pop(key)
	def popitem(self):
		for key in self.d: break
		return key, self.pop(key)
	def items(self):
		return self.d.items()
	def __len__(self):
		return len(self.d)

class LayeredListOfDict:
	def __init__(self, l):
		self.l = l
		self.l = list(map(LayeredDict, self.l))
		self.updated_indices = []
		self.add_layer()
	def add_layer(self):
		self.updated_indices.append(set())
	def pop_layer(self):
		for index in self.updated_indices[-1]:
			self.l[index].pop_layer()
		self.updated_indices.pop()
	def __getitem__(self, index):
		if index not in self.updated_indices[-1]:
			self.l[index].add_layer()
			self.updated_indices[-1].add(index)
		return self.l[index]

if __name__ == '__main__':
	d = {'a' : 1, 'b' : 2}
	ld = LayeredDict(d.copy())
	assert ld.d == d
	ld.add_layer()
	ld['c'] = 3
	ld['b'] = -2
	ld.pop('a')
	assert ld.d == {'b' : -2, 'c' : 3}
	ld.pop_layer()
	assert ld.d == d

	lld = LayeredListOfDict([d.copy(), {'b' : 2, 'c' : 3}])
	lld.add_layer()
	lld[1]['a'] = 1
	assert lld.l[0].d == d and lld.l[1].d == {'a' : 1, 'b' : 2, 'c' : 3}
	lld.pop_layer()
	assert lld.l[0].d == d and lld.l[1].d == {'b' : 2, 'c' : 3}