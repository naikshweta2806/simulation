
import simpy
import random

class ContainerTerminal:
    def __init__(self, env):
        self.env = env
        self.berths = simpy.Resource(env, capacity=2)
        self.cranes = simpy.Resource(env, capacity=2)
        self.trucks = simpy.Resource(env, capacity=3)

    def discharge_vessel(self, vessel):
        print(f"{self.env.now}: Vessel {vessel} berthing...")
        yield self.env.timeout(2)  

        with self.berths.request() as berth:
            yield berth
            print(f"{self.env.now}: Vessel {vessel} berthed at berth {berth}")
            yield self.env.timeout(1) 

            with self.cranes.request() as crane:
                yield crane
                print(f"{self.env.now}: Quay crane starts unloading vessel {vessel}")

                containers_unloaded = 0
                while containers_unloaded < 150:
                    yield self.env.timeout(3)  
                    print(f"{self.env.now}: Quay crane moves a container from vessel {vessel}")

                    with self.trucks.request() as truck:
                        yield truck
                        print(f"{self.env.now}: Truck transporting container from quay crane to yard block")
                        yield self.env.timeout(6) 
                        containers_unloaded += 1

                print(f"{self.env.now}: Vessel {vessel} completely unloaded, leaving berth")
                yield self.env.timeout(2)  

def vessel_generator(env, terminal):
    vessel_count = 0
    while True:
        yield env.timeout(random.expovariate(1/5)) 
        vessel_count += 1
        env.process(terminal.discharge_vessel(vessel_count))

env = simpy.Environment()
terminal = ContainerTerminal(env)
env.process(vessel_generator(env, terminal))

SIMULATION_TIME = 10  
env.run(until=SIMULATION_TIME)


