import random
import sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    '''
    Main class that will run the herd immunity simulation program.  Expects initialization
    parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.

    _____Attributes______

    logger: Logger object.  The helper object that will be responsible for writing
    all logs to the simulation.

    population_size: Int.  The size of the population for this simulation.

    population: [Person].  A list of person objects representing all people in
        the population.

    next_person_id: Int.  The next available id value for all created person objects.
        Each person should have a unique _id value.

    virus_name: String.  The name of the virus for the simulation.  This will be passed
    to the Virus object upon instantiation.

    mortality_rate: Float between 0 and 1.  This will be passed
    to the Virus object upon instantiation.

    basic_repro_num: Float between 0 and 1.   This will be passed
    to the Virus object upon instantiation.

    vacc_percentage: Float between 0 and 1.  Represents the total percentage of population
        vaccinated for the given simulation.

    current_infected: Int.  The number of currently people in the population currently
        infected with the disease in the simulation.

    total_infected: Int.  The running total of people that have been infected since the
    simulation began, including any people currently infected.

    total_dead: Int.  The number of people that have died as a result of the infection
        during this simulation.  Starts at zero.


    _____Methods_____

    __init__(population_size, vacc_percentage, virus_name, mortality_rate,
     basic_repro_num, initial_infected=1):
        -- All arguments will be passed as command-line arguments when the file is run.
        -- After setting values for attributes, calls self._create_population() in order
            to create the population array that will be used for this simulation.

    _create_population(self, initial_infected):
        -- Expects initial_infected as an Int.
        -- Should be called only once, at the end of the __init__ method.
        -- Stores all newly created Person objects in a local variable, population.
        -- Creates all infected person objects first.  Each time a new one is created,
            increments infected_count variable by 1.
        -- Once all infected person objects are created, begins creating healthy
            person objects.  To decide if a person is vaccinated or not, generates
            a random number between 0 and 1.  If that number is smaller than
            self.vacc_percentage, new person object will be created with is_vaccinated
            set to True.  Otherwise, is_vaccinated will be set to False.
        -- Once len(population) is the same as self.population_size, returns population.
    '''

    def __init__(self, population_size, vacc_percentage,virus, virus_name,
                 mortality_rate, basic_repro_num, is_alive, initial_infected=1):
        self.pop_size = pop_size
        self.population = []
        self.total_infected = initial_infected
        self.current_infected = 0
        self.next_id = 0
        self.is_alive = is_alive
        self.vacc_percentage = vacc_percentage
        self.virus = virus
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus, pop_size, vacc_percentage, initial_infected)
        self.population = self._create_population(initial_infected)
        self.logger = Logger("./logs/logger.txt")
        # This attribute will be used to keep track of all the people that
        # catch the infection during a given time step. Store each newly
        # infected person's .ID attribute in here.
        self.newly_infected = []

        # TODO: Create a Logger object and bind it to self.logger.  You should use this
        # logger object to log all events of any importance during the simulation.  Don't forget
        # to call these logger methods in the corresponding parts of the simulation!
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num)

        # This attribute will be used to keep track of all the people that catch
        # the infection during a given time step. We'll store each newly infected
        # person's .ID attribute in here.  At the end of each time step, we'll call
        # self._infect_newly_infected() and then reset .newly_infected back to an empty
        # list.
        self.newly_infected = []
        self.population = self._create_population(initial_infected)
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.

    def _create_population(self, initial_infected):
        self.current_infected = initial_infected
        self.population = []
        infected_count = 0
        # Instantiate new instances of Person until population == pop_size
        while len(self.population) != self.pop_size:
            self.next_id += 1
            # Instantiate Person objects with infection=virus
            if infected_count != initial_infected:
                person_sick = Person(self.next_id, False, infected=self.virus)
                self.population.append(person_sick)
                infected_count += 1
            else:
                # Randomly instantiate Person object with vaccination
                if random.uniform(0, 1) < self.vacc_percentage:
                    self.population.append(Person(self.next_id, True))
                else:
                    # Instantiate Person with no vaccination or infection
                    self.population.append(Person(self.next_id, False))
        return self.population

    def _simulation_should_continue(self):
        # TODO: Complete this method!  This method should return True if the simulation
        # should continue, or False if it should not.  The simulation should end under
        # any of the following circumstances:
        #     - The entire population is dead.
        #     - There are no infected people left in the population.
        # In all other instances, the simulation should continue.
        for person in self.population:
            if person.is_alive and person.infected:
                return True
        return False


    def run(self):
        # TODO: Finish this method.  This method should run the simulation until
        # everyone in the simulation is dead, or the disease no longer exists in the
        # population. To simplify the logic here, we will use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # This method should keep track of the number of time steps that
        # have passed using the time_step_counter variable.  Make sure you remember to
        # the logger's log_time_step() method at the end of each time step, pass in the
        # time_step_counter variable!
        self.logger.write_metadata(self.pop_size, self.vacc_percentage,
                                   self.virus, self.mortality_rate,
                                   self.basic_repro_num)
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            self.time_step()
            should_continue = self._simulation_should_continue()
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
        print('The simulation has ended after {} turns.'.format(time_step_counter))


    def time_step(self):
        # TODO: Finish this method!  This method should contain all the basic logic
        # for computing one time step in the simulation.  This includes:
            # - For each infected person in the population:
            #        - Repeat for 100 total interactions:
            #             - Grab a random person from the population.
            #           - If the person is dead, continue and grab another new
            #                 person from the population. Since we don't interact
            #                 with dead people, this does not count as an interaction.
            #           - Else:
            #               - Call simulation.interaction(person, random_person)
            #               - Increment interaction counter by 1.
            for person in self.population:
                if person.infected is not None:
                    counter = 0
                while counter < 100:
                    random_id = random.randint(1, len(self.population)-1)
                    random_person = self.population[random_id]
                    if person.is_alive is True and random_person.is_alive is True:
                        print("Random dude: " + str(random_person._id))
                        self.interaction(person, random_person)
                    counter += 1
            person.did_survive_infection(self.mortality_rate)
            self.total_infected += len(self.newly_infected)
            print("Update infection")
            self.update_infection_state()
            print("Update infection happened")

    def interaction(self, person, random_person):
        # TODO: Finish this method! This method should be called any time two living
        # people are selected for an interaction.  That means that only living people
        # should be passed into this method.  Assert statements are included to make sure
        # that this doesn't happen.
        assert person.infected is not None
        assert person.is_alive is True
        assert random_person.is_alive is True
        # both people are vaccinated, then both people cant be infected
        # random_person is infected, nothing happens
        if random_person.infected:
            # print("HERE")
            self.logger.log_interaction(person, random_person, False, random_person.is_vaccinated,
            random_person.infected)
        # random_person is vaccinated, nothing happens
        elif random_person.is_vaccinated:
            # print("NOT HERE")
            self.logger.log_interaction(person, random_person, False, random_person.is_vaccinated,
            random_person.infected)
        # random_person not vaccinated or infected
        else:
            rand_num = random.uniform(0, 1)
            if rand_num < self.basic_repro_num:
                if not random_person.infected:
                    print("YES HERE")
                    random_person.infect_person(self.virus)
                    self.newly_infected.append(random_person._id)
                else:
                    # print("HERE?")
                    # print(self.newly_infected)
                    self.logger.log_interaction(person, random_person, "Did infect",
                    random_person.is_vaccinated, random_person.infected)

    def _infect_newly_infected(self):
        # TODO: Finish this method! This method should be called at the end of
        # every time step.  This method should iterate through the list stored in
        # self.newly_infected, which should be filled with the IDs of every person
        # created.  Iterate though this list.
        # For every person id in self.newly_infected:
        #   - Find the Person object in self.population that has this corresponding ID.
        #   - Set this Person's .infected attribute to True.
        # NOTE: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list!
        print("Here: " + str(self.newly_infected))
        self.newly_infected.sort()
        if len(self.newly_infected) < 1:
            return
        for person in self.population:
            if self.newly_infected[0] == person._id:
                person.infect_person(self.virus)
                del self.newly_infected[0]
            if len(self.newly_infected) == 0:
                break
        print("Here2: " + str(self.newly_infected))

if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected, is_alive)
simulation.run()
