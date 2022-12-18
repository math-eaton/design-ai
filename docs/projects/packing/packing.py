import Rhino.Geometry as rh

class Agent:

    def __init__(self, pt, ed, names, adjacencies):

        self.cp = pt
        self.edge = ed
        self.name = names
        self.adjacency = adjacencies
        self.neighbors = []

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):

        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d < self.edge + other.edge:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (self.edge + other.edge - d) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

        return amount

    # method for checking distance to other instance and moving closer if they are not touching
    def cluster(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d > self.edge + other.edge:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (self.edge + other.edge)) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move self
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

            # reverse vector and move other object same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

        return amount

    # def get_circle(self):
    #     return rh.Circle(self.cp, self.edge)

    # replace circle params with rectangle
    def get_rectangle(self):

        # extract layout plane for rectangle draw
         center_xy = self.cp
         plane_vector = rh.Vector3d(0,0,1)
         plane_rect = rh.Plane(center_xy, plane_vector)

         return rh.Rectangle3d(plane_rect, self.edge, self.edge)


# these must match gh python component ins
def run(pts, radii, names, adjacencies, max_iters, alpha):
    
    # print(adjacency)
    # print(adjacencies)
    agents = []


    for i, pt in enumerate(pts):
        my_agent = Agent(pt, radii[i], names[i], adjacencies[i])
        agents.append(my_agent)
        
    # for each agent in the list, add any agent referenced in the adjacency list as neighbor
    for i in range(len(agents)):
        
        for j in range(len(agents)-1):
        
            if agents[j].name in agents[i].adjacency:
                # print(agents[j].name)
                # print(agents[i].adjacency)
                agents[i].add_neighbor(agents[j])
            else:
                continue

    for i in range(max_iters):

        total_amount = 0

        for j, agent_1 in enumerate(agents):

            # cluster to all agent's neighbors
            for agent_2 in agent_1.neighbors:
                total_amount += agent_1.cluster(agent_2, alpha)

            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += agent_1.collide(agent_2, alpha/5)

        if total_amount < .001:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    #init rect + names array
    # circles = []
    rects = []
    names = []

    for agent in agents:
        # circles.append(agent.get_circle())
        rects.append(agent.get_rectangle())
        names.append(agent.adjacency)
        
    print(names)

    return rects, iters, names