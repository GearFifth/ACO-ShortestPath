class Graph:
  """ Reprezentacija jednostavnog grafa"""

  #------------------------- Ugnježdena klasa Vertex -------------------------
  class Vertex:
    """ Struktura koja predstavlja čvor grafa."""
    __slots__ = '_element'

    def __init__(self, x):
      self._element = x
  
    def element(self):
      """Vraća element vezan za čvor grafa."""
      return self._element
  
    def __hash__(self):         # omogućava da Vertex bude ključ mape
      return hash(id(self))

    def __str__(self):
      return str(self._element)
    
  #------------------------- Ugnježdena klasa Edge -------------------------
  class Edge:
    """ Struktura koja predstavlja ivicu grafa """
    __slots__ = '_origin', '_destination', '_element'
  
    def __init__(self, origin, destination, element):
      self._origin = origin
      self._destination = destination
      self._element = element   
  
    def endpoints(self):
      """ Vraća torku (u,v) za čvorove u i v."""
      return (self._origin, self._destination)
  
    def opposite(self, v):
      """ Vraća čvor koji se nalazi sa druge strane čvora v ove ivice."""
      if not isinstance(v, Graph.Vertex):
        raise TypeError('v mora biti instanca klase Vertex')
      if self._destination == v:
        return self._origin
      elif self._origin == v:
        return self._destination
      raise ValueError('v nije čvor ivice')
  
    def __hash__(self):         # omogućava da Edge bude ključ mape
      return hash( (self._origin, self._destination) )

    def __str__(self):
      return '({0},{1})'.format(self._origin,self._destination)
    
  #------------------------- Metode klase Graph -------------------------
  def __init__(self):
    """ Kreira prazan usmeren graf """
    self._outgoing = {}
    self._incoming = {}
    
  def _validate_vertex(self, v):
    """ Proverava da li je v čvor(Vertex) ovog grafa."""
    if not isinstance(v, self.Vertex):
      raise TypeError('Očekivan je objekat klase Vertex')
    if v not in self._outgoing:
      raise ValueError('Vertex ne pripada ovom grafu.')

  def vertex_count(self):
    """ Vraća broj čvorova u grafu."""
    return len(self._outgoing)

  def vertices(self):
    """ Vraća iterator nad svim čvorovima grafa."""
    return self._outgoing.keys()

  def edge_count(self):
    """ Vraća broj ivica u grafu."""
    total = sum(len(self._outgoing[v]) for v in self._outgoing)
    return total

  def edges(self):
    """ Vraća set svih ivica u grafu."""
    result = set()       # pomoću seta osiguravamo da čvorove neusmerenog grafa brojimo samo jednom
    for secondary_map in self._outgoing.values():
      result.update(secondary_map.values())    # dodavanje ivice u rezultujući set
    return result

  def get_edge(self, u, v):
    """ Vraća ivicu između čvorova u i v ili None ako nisu susedni."""
    self._validate_vertex(u)
    self._validate_vertex(v)
    return self._outgoing[u].get(v)

  def degree(self, v, outgoing=True):   
    """ Vraća stepen čvora - broj(odlaznih) ivica iz čvora v u grafu.

    Opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
    """
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    return len(adj[v])

  def incident_edges(self, v, outgoing=True):   
    """ Vraća sve (odlazne) ivice iz čvora v u grafu.

    Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
    """
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    for edge in adj[v].values():
      yield edge

  def insert_vertex(self, x=None):
    """ Ubacuje i vraća novi čvor (Vertex) sa elementom x"""
    v = self.Vertex(x)
    self._outgoing[v] = {}
    self._incoming[v] = {}        # mapa različitih vrednosti za dolazne čvorove
    return v
      
  def insert_edge(self, u, v, elem = None):
    """ Ubacuje i vraća novu ivicu (Edge) od u do v."""

    e = self.Edge(u, v, elem)
    self._outgoing[u][v] = e
    self._incoming[v][u] = e
  




def graph_from_edgelist(E):
  """Kreira graf od ivica.

  Dozvoljeno je dva načina navođenje ivica:
        (origin,destination)
        (origin,destination,element).
  Podrazumeva se da se labele čvorova mogu hešovati.
  """
  g = Graph()
  V = set()
  for e in E:
    V.add(e[0])
    V.add(e[1])

  vertices = {} #izbegavamo ponavljanje labela između čvorova
  for v in V:
    vertices[v] = g.insert_vertex(v)

  for e in E:
    src = e[0]
    dest = e[1]
    elem = e[2]
    g.insert_edge(vertices[src],vertices[dest], elem)

  return g, vertices