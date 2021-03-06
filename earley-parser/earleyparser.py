import argparse
from collections import defaultdict
from nltk.tree import Tree
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
import time

cf = CanvasFrame()

class Rule(object):
	def __init__(self, lhs, rhs):
		self.lhs, self.rhs = lhs, rhs

	def __getitem__(self, i):
		return self.rhs[i]

	def __len__(self):
		return len(self.rhs)

class Grammar(object):
	def __init__(self):
		self.rules = defaultdict(list)

	def add(self, rule):
		self.rules[rule.lhs].append(rule)

	def load_grammar(fpath):
		grammar = Grammar()
		with open(fpath) as f:
			for line in f:
				line = line.strip()
				if len(line) != 0:
					entries = line.split('->')
					for rhs in entries[1].split('|'):
						grammar.add(Rule(entries[0].strip(), rhs.strip().split()))
		return grammar

	def __getitem__(self, i):
		return self.rules[i]

	def is_tag(self, symbol):
		if not len(self.rules[symbol]) == 0: # if not a terminal
			return all(len(self.rules[s]) == 0 for r in self.rules[symbol] for s in r.rhs)
		return False

class State(object):
	def __init__(self, rule=Rule('<GAMMA>', ['S']), dot=0, sent_pos=0, chart_pos=0, back_pointers=[]):
		self.rule = rule
		self.dot = dot
		self.sent_pos = sent_pos
		self.chart_pos = chart_pos
		self.back_pointers = back_pointers

	def __eq__(self, other):
		if type(other) is State:
			return self.rule == other.rule and self.dot == other.dot and self.sent_pos == other.sent_pos
		return False

	def next(self):
		if self.dot < len(self.rule):
			return self.rule[self.dot]

	def is_complete(self):
		return len(self.rule) == self.dot

class ChartEntry(object):
	def __init__(self, states):
		self.states = states

	def __iter__(self):
		return iter(self.states)

	def __getitem__(self, i):
		return self.states[i]
	
	def __len__(self):
		return len(self.states)

	def add(self, state):
		if state not in self.states:
			self.states.append(state)

class EarleyParse(object):
	def __init__(self, sentence, grammar):
		self.words = sentence.split()
		self.grammar = grammar
		# Initalize chart with empty states
		self.chart = [(ChartEntry([]) if i > 0 else ChartEntry([State()])) for i in range(len(self.words) + 1)]

	def predictor(self, state, pos):
		for rule in self.grammar[state.next()]:
			self.chart[pos].add(State(rule, dot=0, sent_pos=state.chart_pos, chart_pos=state.chart_pos))

	def scanner(self, state, pos):
		if state.chart_pos < len(self.words):
			word = self.words[state.chart_pos]
			if any((word in r) for r in self.grammar[state.next()]):
				self.chart[pos + 1].add(State(Rule(state.next(), [word]), dot=1, sent_pos=state.chart_pos, chart_pos=(state.chart_pos + 1)))

	def completer(self, state, pos):
		for prev_state in self.chart[state.sent_pos]:
			if prev_state.next() == state.rule.lhs:
				self.chart[pos].add(State(prev_state.rule, dot=(prev_state.dot + 1), sent_pos=prev_state.sent_pos, chart_pos=pos, back_pointers=(prev_state.back_pointers + [state])))

	def parse(self):
		for i in range(len(self.chart)):
			for state in self.chart[i]:
				if not state.is_complete(): 		# if not complete
					if self.grammar.is_tag(state.next()):
						self.scanner(state, i)
					else:
						self.predictor(state, i)
				else:
					self.completer(state, i)
				
				# Animate parse tree
				if state.is_complete() and state.rule.lhs != '<GAMMA>' and state.chart_pos == i:
					self.make_tree(state).pretty_print()
					tree = self.make_tree(state)
					tc = TreeWidget(cf.canvas(), tree, node_font=('helvetica', -15, 'bold'), leaf_font=('helvetica', -15))
					cf.add_widget(tc)
					cf.canvas().update()
					time.sleep(1.5)
					cf.remove_widget(tc)
					tc.destroy()

	def make_tree(self, state):
		if self.grammar.is_tag(state.rule.lhs):
			return Tree(state.rule.lhs, [state.rule.rhs[0]])
		return Tree(state.rule.lhs, [self.make_tree(s) for s in state.back_pointers])

	def get_tree(self):
		for state in self.chart[-1]:
			if state.is_complete() and state.rule.lhs == 'S' and state.sent_pos == 0 and state.chart_pos == len(self.words):
				return self.make_tree(state)
		return None
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('draw', nargs='?', default=False)
	parser.add_argument('grammar_file', help="Filepath to grammar file")
	args = parser.parse_args()

	grammar = Grammar.load_grammar(args.grammar_file)

	sentence = 'book that flight'
	# sentence = 'does he prefer that flight through Indiana'
	# sentence = 'this meal is the best'

	parse = EarleyParse(sentence, grammar)
	parse.parse()
	parse = parse.get_tree()
	if parse is None:
		print(sentence + '\n')
	else:
		if args.draw:
			tc = TreeWidget(cf.canvas(), parse, node_font=('helvetica', -15, 'bold'), leaf_font=('helvetica', -15))
			cf.add_widget(tc)
			cf.mainloop()
		else:
			parse.pretty_print()