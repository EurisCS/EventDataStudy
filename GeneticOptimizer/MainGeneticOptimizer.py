import random

class Mutation:

    def __init__(self, max_mutation_factor, probability_of_mutation):
        self.max_mutation_factor = max_mutation_factor
        self.probability_of_mutation = probability_of_mutation

    #
    # adjust the weight mutation
    def adjust_mutation_weight(self, step_mutation_factor):

        self.max_mutation_factor = round(self.max_mutation_factor - step_mutation_factor, 3)

        if self.max_mutation_factor <= 0.001:
            self.max_mutation_factor = round(step_mutation_factor / 2, 3)

    #
    # adjust the probability of the mutation
    def adjust_probability_of_mutation(self, step_probability_of_mutation, reduce=True):
        if reduce:
            self.probability_of_mutation -= self.probability_of_mutation * step_probability_of_mutation
            if self.probability_of_mutation <= 0:
                self.probability_of_mutation = 0.001
        else:
            self.probability_of_mutation += self.probability_of_mutation * step_probability_of_mutation

            if self.probability_of_mutation > 1:
                self.probability_of_mutation = 1

    #
    # apply mutation of list conditioned list
    def apply_mutation_on_list_of_conditioned_list(self, list_conditioned_list):

        list_of_muted_list = []
        for list_conditioned in list_conditioned_list:
            list_of_muted_list.append(self.apply_mutation_on_list(list_conditioned))

        return list_of_muted_list

    #
    #  apply mutation on conditioned list
    def apply_mutation_on_list(self, list_conditioned):

        # delete duplicates values
        list_conditioned.delete_duplicates_values()

        new_list_values = []

        # create mutation foreach value in list
        for index_value in range(len(list_conditioned.list_values)):

            random_number = random.uniform(0, 1)

            if random_number <= self.probability_of_mutation:
                mutation_lower, mutation_upper = self.apply_mutation_value(list_conditioned.list_values[index_value])

                new_list_values.append(mutation_lower)
                new_list_values.append(mutation_upper)

        new_list_conditioned = list_conditioned.copy_with_new_list(new_list_values)
        new_list_conditioned.delete_duplicates_values()

        return new_list_conditioned

    #
    # apply two mutation on a value
    def apply_mutation_value(self, value):

        return value - value * random.uniform(0, self.max_mutation_factor), \
               value + value * random.uniform(0, self.max_mutation_factor)
