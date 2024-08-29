import json
from owlready2 import *
import types


def json2owl(name):

    # Reading input data
    with open(f'{name}.json') as f:
        data = json.load(f)

    onto_name = name.split('\\')[-1]
    onto = get_ontology(f'{onto_name}.owl')
    with onto:

        # Asserting attacks relation
        class attacks(ObjectProperty):
            pass

        class isAttackedBy(ObjectProperty):
            inverse_property = attacks

        class text(AnnotationProperty, FunctionalProperty):
            pass

        class round(AnnotationProperty, FunctionalProperty):
            pass

        class text(AnnotationProperty, FunctionalProperty):
            pass

        class number(AnnotationProperty, FunctionalProperty):
            pass
        
        # Creating argument sets
        argument_sets = data['argument_sets']
        for argument_set, arguments in argument_sets.items():
            Cl = types.new_class(argument_set, (Thing,))
            Cl.label = argument_set
            for argument, text in arguments.items():
                inst = Cl()
                inst.label = argument
                argument = argument.split('.')
                inst.text = text
                inst.round = argument[1]
                inst.number = argument[2]

        attack_pairs = data['attack_pairs']
        for pair in attack_pairs:
            #print(pair)
            argument1 = pair[0].split('.')
            argument1 = onto.search_one(is_a = onto[argument1[0]],
                                        round = argument1[1],
                                        number = argument1[2])
            argument2 = pair[1].split('.')
            argument2 = onto.search_one(is_a = onto[argument2[0]],
                                        round = argument2[1],
                                        number = argument2[2])
            argument1.attacks.append(argument2)
            argument2.isAttackedBy.append(argument1)

        # Starting reasoning to derive inverse attacks
        #sync_reasoner_pellet(infer_property_values = True,
        #                     debug = 2)

        # Closing world
        for inst in onto.individuals():
            if inst.attacks:
                inst.is_a.append(attacks.only(OneOf(inst.attacks)))
            else:
                inst.is_a.append(attacks.only(Nothing))
            if inst.isAttackedBy:
                inst.is_a.append(isAttackedBy.only(OneOf(inst.isAttackedBy)))
            else:
                inst.is_a.append(isAttackedBy.only(Nothing))

        # Defining conflict free sets
        for argument_set1 in argument_sets.keys():
            Cl = onto[argument_set1]
            Cl_cf = types.new_class(f'{argument_set1}ConflictFree', (Cl,))
            complement = []
            for argument_set2 in argument_sets.keys():
                if argument_set1 != argument_set2:
                    complement.append(onto[argument_set2])
            Cl_cf.equivalent_to.append(Cl & attacks.only(Or(complement)))

        # Defining admissible sets
        for argument_set1 in argument_sets.keys():
            Cl_cf = onto[f'{argument_set1}ConflictFree']
            Cl_adm = types.new_class(f'{argument_set1}Admissible', (Cl_cf,))
            Cl_adm.equivalent_to.append(Cl_cf & isAttackedBy.only(isAttackedBy.some(Cl_cf)))
            

    onto.save(f'{name}.owl', format = 'ntriples')
    with onto:
        sync_reasoner_pellet(infer_property_values = True,
                             debug = 0)
    onto.save(f'{name}_inferred.owl', format = 'ntriples')
    onto.destroy()
