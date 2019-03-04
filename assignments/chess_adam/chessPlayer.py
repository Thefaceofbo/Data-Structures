import math as mh
import time
import random as rd

class Queue:

   def __init__(self):
      self.store = []

   def push(self, val):
      self.store = self.store + [val]

   def pop(self):
      if len(self.store) < 1:
         return [False, 0]
      else:
         rt = self.store[0]
         self.store = self.store[1:len(self.store)]
         return [True, rt]

   def length(self):
      return len(self.store)

class Data_Node:

   Bias = 5
   MoveLimit = 7

   def __init__(self, board, playing):
      self.next = [] # of Data_Nodes
      self.move = [-1, -1]
      self.sims = 1
      self.score = 0
      self.board = board
      self.playing = playing
      self.over = False

   def get_value(self, parentVisits):
      return (self.score/self.sims) + self.Bias*mh.sqrt(mh.log(parentVisits)/self.sims)

   def make_move(self, mv):
      self.move = mv
      self.board = move(self.board, mv)
      self.playing = 2 if self.playing == 1 else 1
      return True

   def play(self):
      board = list(self.board)
      for pl in range(self.playing-1, self.MoveLimit+self.playing, 1):
         board = move(board, sample_move(board, (pl % 2) + 1))
      return board

   def simulate_node(self):
      # Generate new possibility
      new = Data_Node(self.board, self.playing)
      self.next = self.next + [new]
      new.make_move(sample_move(new.board, new.playing))
      # Simulate to determine score
      sim = new.play()
      new.score = get_score(new.board, sim)
      return new.score

   def build(self, parSims):
      if len(self.next) > 0:
         self.sims = self.sims + 1
         best = self
         sms = parSims
         bestPar = True
         for n in self.next:
            if n.get_value(self.sims) >= best.get_value(sms):
               bestPar = False
               best = n
               sms = self.sims
         if bestPar:
            return self.simulate_node()
         sc = best.build(self.sims)
         self.score = self.score + sc
         return sc
      else:
         return self.simulate_node()

   def expand(self):
      if self.over:
         return True
      self.build(self.sims)
      return False # Returns game completion state
   
   def traverse(self):
      q = Queue()
      q.push([self, self.sims])
      final = []
      while (q.length() > 0):
         s = q.pop()[1]
         final = final + [[s[0].move, s[0].get_value(s[1])]]
         for n in s[0].next:
            q.push([n, s[0].sims])
      return final

   def select_node(self):
      if len(self.next) < 1:
         return self
      else:
         best = Data_Node([], 1)
         for n in self.next:
            if n.get_value(self.sims) >= best.get_value(self.sims):
               best = n
         return best.select_node()

   def fetch_candidates(self, player):
      mvs = []
      for n in self.next:
         mvs = mvs + [n.move, n.get_value(self.sims)]
      return mvs

   def get_move(self):
      return self.move


def sample_move(board, player):
   pieces = GetPlayerPositions(board, player*10)
   mvs = []
   while len(mvs) < 1:
      pc = pieces[rd.randint(0, len(pieces)-1)]
      mvs = GetPieceLegalMoves(board, pc)
   return [pc, mvs[rd.randint(0, len(mvs)-1)]]

def move(board, move):
   b = list(board)
   if (b[move[1]] != 0):
      print("PIECE TAKEN")
   b[move[1]] = b[move[0]]
   b[move[0]] = 0
   return b

def get_score(original, final):
   return 0

def GetPlayerPositions(board, player):
   s = int(player / 10)
   final = []
   for ind,b in enumerate(board):
      if int(str(b)[0]) == s:
         final += [ind]
   return final

def IsPositionUnderThreat(board, position, player):
   opp = 2 if player == 1 else 1
   mvs = []
   for v in range(0, 64, 1):
      if (int(str(board[position])[0]) == opp):
         mvs += GetPieceLegalMoves(board, v)
   if (position in mvs):
      return True
   return False

def GetPieceLegalMoves(board, position):
   validMove = [pawn, knight, bishop, rook, queen, king]
   pieceType = int(str(board[position])[-1])
   player = int(str(board[position])[0])
   final = []
   for v in range(0, 64, 1):
      if (validMove[pieceType](position, v, player) and positionIsAvailable(board, player, v) and not getCollisions(board, pieceType, position, v)):
         final += [v]
   return final

def get_path_points(f, i):
   if f == i:
      return []
   path = []
   final = [f % 8, int(f / 8)]
   initial = [i % 8, int(i / 8)]
   direction = [0, 0]
   direction[0] = int(abs(final[0] - initial[0])/(final[0] - initial[0])) if final[0] - initial[0] != 0 else 0
   direction[1] = int(abs(final[1] - initial[1])/(final[1] - initial[1])) if final[1] - initial[1] != 0 else 0
   if final[0] == initial[0]:
      for v in range(int(initial[1] + direction[1]), int(final[1]), direction[1]):
         path = path + [final[0] + 8*v]
   elif final[1] == initial[1]:
      for v in range(int(initial[0] + direction[0]), int(final[0]), direction[0]):
         path = path + [v + 8*final[1]]
   else:
      if abs(final[0] - initial[0]) != abs(final[1] - initial[1]):
         return []
      for v in range(1, int(abs(final[0] - initial[0])), 1):
         path = path + [(initial[0] + direction[0]*v) + (initial[1] + direction[1]*v)*8]
   return path

def positionIsAvailable(board, player, pos):
   if int(str(board[pos])[0]) != player:
      return True
   return False

def getCollisions(board, piece, curr, targ):
   if (piece == 1):
      return False
   pts = get_path_points(targ, curr)
   for b in pts:
      if (board[b] != 0):
         return True
   return False

def pawn(final, initial, player):
   if player == 2 and final-initial == 8:
      return True
   if player == 1 and initial-final == 8:
      return True
   return False

def knight(final, initial, player):
   diff = abs(final - initial)
   if diff in [6, 10, 15, 17]:
      return True
   return False

def bishop(final, initial, player):
   f = [final % 8, int(final / 8)]
   i = [initial % 8, int(initial / 8)]
   if abs(i[0] - f[0]) == abs(i[1] - f[1]):
      return True
   return False

def rook(final, initial, player):
   f = [final % 8, int(final / 8)]
   i = [initial % 8, int(initial / 8)]
   diffx = abs(i[0] - f[0])
   diffy = abs(i[1] - f[1])
   if diffx == 0 and diffy != 0:
      return True
   elif diffy == 0 and diffx != 0:
      return True
   return False

def queen(final, initial, player):
   f = [final % 8, int(final / 8)]
   i = [initial % 8, int(initial / 8)]
   diffx = abs(i[0] - f[0])
   diffy = abs(i[1] - f[1])
   if diffx == diffy:
      return True
   elif diffx == 0 and diffy != 0:
      return True
   elif diffy == 0 and diffx != 0:
      return True
   return False

def king(final, initial, player):
   f = [final % 8, int(final / 8)]
   i = [initial % 8, int(initial / 8)]
   diffx = abs(i[0] - f[0])
   diffy = abs(i[1] - f[1])
   if diffx > 1 or diffy > 1:
      return False
   return True

def chessPlayer(board: list, player: int) -> list:
   state = Data_Node(board, player)
   t = time.time()
   while time.time() - t < 6:
      if state.expand():
         break
      break
   # Selection from state
   status = False
   if state.next != []:
      status = True
   return [status, state.select_node().get_move(), state.fetch_candidates(player), state.traverse()] # [ status (bool), move ([piece, move]), candidateMoves (List of [move, weight] values), evalTree (None)]
