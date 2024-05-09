from cnwheat import model, parameters


class Collar:
    def calculate_Unloading_Sucrose(self, sucrose_roots, sucrose_phloem, mstruct_axis, T_effect_conductivity):
        """Rate of sucrose Unloading from phloem to roots (µmol` C sucrose unloaded g-1 mstruct h-1).


        :param float sucrose_roots: Amount of sucrose in roots (µmol` C)
        :param float sucrose_phloem: Sucrose concentration in phloem (µmol` C g-1 mstruct)
        :param float mstruct_axis: The structural dry mass of the axis (g)
        :param float T_effect_conductivity: Effect of the temperature on the conductivity rate at 20µC (AU)

        :return: Rate of Sucrose Unloading from shoot homogeneous phloem to root homogeneous phloem (µmol` C g-1 mstruct h-1)
        :rtype: float
        """
        # We compute the flow necessary to mean the concentrations between shoot and root phloem, as they are considered as homogeneous.
        conc_sucrose_whole_phloem = ((sucrose_roots + sucrose_phloem)
                / (self.mstruct * self.__class__.PARAMETERS.ALPHA + (mstruct_axis - self.mstruct) * parameters.AXIS_PARAMETERS.ALPHA))

        return (conc_sucrose_whole_phloem * self.mstruct * self.__class__.PARAMETERS.ALPHA) - sucrose_roots


model.Roots.calculate_Unloading_Sucrose = Collar.calculate_Unloading_Sucrose
