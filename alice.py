import networkx
import nltk
import itertools
import codecs

textfile="pg28885.txt"

def delegalese(textfile):
  f=codecs.open(textfile,"r","utf-8")
  tbody=itertools.takewhile(lambda x: not "End of Project Gutenberg" in x,
  itertools.dropwhile(lambda x: not "*** START OF" in x,f))
  text="\n".join(tbody)
  f.close()
  return text
  
def get_text(textfile):
  return nltk.text.Text(nltk.word_tokenize(delegalese(textfile)))

def get_pairs(t):
  tokens=[i for i in t]
  while len(tokens)>=2:
    first=tokens.pop(0)
    second=tokens[0]
    yield (first,second)

def edges(g,et):
  src=et[0]
  dst=et[1]
  if g.edge.get(src):
    if g.edge[src].get(dst):
      g.edge[src][dst]["weight"]+=1
      return g
  g.add_edge(src,dst,weight=1)
  return g

def generate_graph(text):
  g=networkx.DiGraph()
  g=reduce(edges,get_pairs(text),g)
  return g

if __name__=="__main__":
  import sys
  textfile=sys.argv[1]
  outfile=sys.argv[2]
  g=generate_graph(get_text(textfile))
  networkx.gexf.write_gexf(g,outfile)
