"""
6.1010 Spring '23 Lab 4: Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    compound = {}
    for food in recipes:
        if food[0] == "compound":

            if food[1] not in compound:

                food_list = []
                compound[food[1]] = food_list
            compound[food[1]].append(food[2])

    return compound


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic = {}
    for food in recipes:
        if food[0] == "atomic":
            atomic[food[1]] = food[2]

    return atomic


def copy_compound(compound):
    if type(compound)==list:
       
        comp_list=[]
        for dict in compound:
          compound_copy = {}
          for key, val in dict.items():
            compound_copy[key] = val  
        return compound_copy
    else:
        compound_copy = {}
        for key, val in compound.items():
            compound_copy[key] = val

        return compound_copy




def lowest_cost(recipes, food_item, forbidden=[]):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """

    comp_recipes = make_recipe_book(recipes)
    atom_recipes = make_atomic_costs(recipes)

    def lower_helper(food, quantity):

        if food not in comp_recipes and food not in atom_recipes:

            return None

        else:
            if food in atom_recipes and food not in forbidden:
                return atom_recipes[food] * quantity

            elif food in comp_recipes and food not in forbidden:
                food_recipes = comp_recipes[food]
                price_l = []
                for food_list in food_recipes:
                    
                    price_x = 0
                    for i, food_atom in enumerate(food_list):

                        if len(food_recipes) > 1:

                            if lower_helper(food_atom[0], food_atom[1]) != None:
                                price_x += lower_helper(food_atom[0], food_atom[1])
                            else:
                                price_x = float("inf")
                        else:
                            if lower_helper(food_atom[0], food_atom[1]) != None:
                                price_x += lower_helper(food_atom[0], food_atom[1])
                            else:
                                return None
                    price_l.append(price_x)
                    

                if min(price_l) != float("inf"):
                    return min(price_l) * quantity
                else:
                    return None
            elif food in forbidden:
                pass

    return lower_helper(food_item, quantity=1)


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    copy_dict = copy_compound(flat_recipe)
    for key, value in copy_dict.items():
        copy_dict[key] = value * n
    return copy_dict


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    copy_dict = {}
    for dict in flat_recipes:
        
        for key, value in dict.items():
            if key not in copy_dict:
                copy_dict[key] = value
            else:
                copy_dict[key] += value
    return copy_dict


def cheapest_flat_recipe(recipes, food_item, forbidden=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    # Create a dictionary of atomic ingredient costs from the recipes
    comp_recipes = make_recipe_book(recipes)
    atom_recipes = make_atomic_costs(recipes)
    shopping = {}
   
    if food_item not in comp_recipes and food_item not in atom_recipes:
        return None
    elif food_item in forbidden:
        return None

    elif food_item in atom_recipes and food_item not in forbidden:

        if food_item in shopping:
            shopping[food_item] += 1
        else:
            shopping[food_item] = 1

    elif food_item in comp_recipes and food_item not in forbidden:  # compound food
        food_recipe = comp_recipes[food_item]
        cheapest = float("inf")
        cheapest_rec = None
        for food_list in food_recipe:
            recipe_cost = 0
            recipe_dict = {}
            flag = True
            for ingredient, quantity in food_list:
                sub_shop = cheapest_flat_recipe(recipes, ingredient, forbidden)
                if sub_shop != None:
                    print("lol")
                    sub_shop_sc = scale_recipe(sub_shop, quantity)
                    for key, val in sub_shop_sc.items():
                        if key not in atom_recipes:
                            recipe_cost = float("inf")
                        else:
                            recipe_cost += atom_recipes[key] * val
                        if key in recipe_dict:
                            recipe_dict[key] += val
                        else:
                            recipe_dict[key] = val
                else:
                    flag = False
                    break
            if flag:
                if recipe_cost < cheapest:
                    cheapest = recipe_cost
                    cheapest_rec = recipe_dict
        if cheapest_rec is not None:
            for key, val in cheapest_rec.items():
                if key in shopping:
                    shopping[key] += val
                else:
                    shopping[key] = val
        else:
            return None

    return shopping


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes make a certain ingredient as part of a recipe, compute all
    combinations of the flat recipes.
    """
    copy_list=flat_recipes
    if len(flat_recipes)==0:
        return [{}]
    result=[]
    for recipe in copy_list[0]:
        
        for mixed in ingredient_mixes(copy_list[1:]):
            new_dict={}
            for key in recipe.keys():
                if key in mixed:
                    new_dict[key]=recipe[key]+mixed[key]
                else:
                    new_dict[key]=recipe[key]
            for key in mixed.keys():
                if key not in new_dict:
                    new_dict[key]=mixed[key]
           
            result.append(dict(new_dict))
            
    return result

def all_flat_recipes(recipes, food,forbidden=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
  
    if food in forbidden:
            return []
    comp_recipe=make_recipe_book(recipes)
    atom_recipe=make_atomic_costs(recipes)
   
    def all_flat_helper(food_item):
        out=[]
        if food_item in atom_recipe and food_item not in forbidden :
            return [{food_item:1}]
        elif food_item not in comp_recipe and food_item not in atom_recipe:
            return []

        elif food_item in forbidden:
            return []
        
        elif food_item in comp_recipe:

            food_recipe=comp_recipe[food_item]
            
            for food_list in food_recipe:
                mix_list=[]
                for ing, quantity in food_list:
                    ing_recipe=[]
                    if ing in forbidden:
                        pass
                    for sp_recipe in all_flat_helper(ing):
                        scaled_flat=scale_recipe(sp_recipe,quantity)
                        ing_recipe.append(scaled_flat)
                    mix_list.append(ing_recipe) 
                ing_mix=ingredient_mixes(mix_list)
                out.extend(ing_mix)
        print(out)      
        return out   
       
    return all_flat_helper(food)
  

if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!
