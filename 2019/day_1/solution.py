import math


def calculate_fuel_requirements(mass):
    """
    Calculate the fuel requirements based on ``mass``.

    The formula is: floor((mass / 3)) - 2.
    """
    return math.floor(mass / 3) - 2


def calculate_fuel_requirements_for_module(module_mass):
    """
    Calculate the fuel requirements for a module, including the fuel
    needed for the fuel.
    """
    module_fuel_requirements = calculate_fuel_requirements(module_mass)
    fuel_fuel_requirements = calculate_fuel_requirements(module_fuel_requirements)
    while fuel_fuel_requirements > 0:
        module_fuel_requirements += fuel_fuel_requirements
        fuel_fuel_requirements = calculate_fuel_requirements(fuel_fuel_requirements)
    return module_fuel_requirements


def main():
    with open('./input') as fh:
        print(sum(calculate_fuel_requirements_for_module(int(_m.strip())) for _m in fh.readlines()))


if __name__ == '__main__':
    main()
