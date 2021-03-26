from collections import deque

class message_database:

  def __init__(self):
    self.db = dict()
  
  def insert(self,guild, channel, message):

    if(guild in self.db.keys()):

      if(channel in self.db[guild].keys()):

        if(len(self.db[guild][channel]) <= 5):
          self.db[guild][channel].append(message)
        else:
          self.db[guild][channel].popleft()
          self.db[guild][channel].append(message)

      else:

        self.db[guild][channel] = deque([message])

    else:

      self.db[guild] = {channel : deque([message])}
    

  def get(self,guild, channel, depth):
    # self.db[guild][channel].pop()
    messages_out = deque()
    try:
      for i in range(depth, 0 , -1) :
        messages_out.append(self.db[guild][channel][-(i)])
    finally:
      return messages_out