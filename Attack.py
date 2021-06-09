class Attack:
  def __init__(self, origin, target, time, method, pcarga, gcarga, sondaespionaje = 1, crucero = 1):
    self.origin = origin
    self.target = target
    self.time = time
    self.pcarga = pcarga
    self.gcarga = gcarga
    self.sondaespionaje = sondaespionaje
    self.crucero = crucero
    self.method = method